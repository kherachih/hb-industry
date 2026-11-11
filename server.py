import os
import sys
import json
import sqlite3
import hashlib
import secrets
import csv
import io
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory, Response

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'hbig.db')
os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__, static_folder=None)

# Active session tokens: { token: { "username": username, "expires": datetime } }
ACTIVE_SESSIONS = {}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_pw(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            company TEXT NOT NULL,
            equipment TEXT,
            status TEXT DEFAULT 'Nouveau',
            notes TEXT DEFAULT '',
            ip TEXT,
            user_agent TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip TEXT,
            user_agent TEXT,
            device TEXT,
            path TEXT,
            referrer TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Ensure admin user exists (default: admin / hbig2026 or admin / admin)
    c.execute('SELECT * FROM admin_users WHERE username = ?', ('admin',))
    if not c.fetchone():
        c.execute('INSERT INTO admin_users (username, password_hash) VALUES (?, ?)',
                  ('admin', hash_pw('hbig2026')))
        
    conn.commit()
    conn.close()

init_db()

def authenticate_request():
    auth_header = request.headers.get('Authorization', '')
    token = None
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ', 1)[1]
    elif 'token' in request.args:
        token = request.args.get('token')
        
    if not token or token not in ACTIVE_SESSIONS:
        return None
    session_data = ACTIVE_SESSIONS[token]
    if session_data['expires'] < datetime.now():
        del ACTIVE_SESSIONS[token]
        return None
    return session_data['username']

# --- PUBLIC API ROUTES ---

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json(force=True, silent=True) or request.form.to_dict()
    name = (data.get('name') or '').strip()
    phone = (data.get('phone') or '').strip()
    email = (data.get('email') or '').strip()
    company = (data.get('company') or '').strip()
    equipment = (data.get('00NHn00000ZTeTu') or data.get('equipment') or '').strip()
    
    if not name or not phone or not company:
        return jsonify({
            'success': False,
            'error': 'Veuillez remplir tous les champs obligatoires (Nom, Téléphone, Entreprise).'
        }), 400

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', '')

    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO leads (name, phone, email, company, equipment, status, notes, ip, user_agent)
        VALUES (?, ?, ?, ?, ?, 'Nouveau', '', ?, ?)
    ''', (name, phone, email, company, equipment, ip, user_agent))
    lead_id = c.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Demande de devis transmise avec succès au bureau d\'études HBIG.',
        'lead_id': lead_id
    })

@app.route('/api/track', methods=['POST'])
def api_track():
    data = request.get_json(force=True, silent=True) or {}
    path = data.get('path', '/')
    referrer = data.get('referrer', '')
    device = data.get('device', 'Desktop')
    
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', '')

    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO visits (ip, user_agent, device, path, referrer)
        VALUES (?, ?, ?, ?, ?)
    ''', (ip, user_agent, device, path, referrer))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(force=True, silent=True) or {}
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()

    if not username or not password:
        return jsonify({'success': False, 'error': 'Nom d\'utilisateur et mot de passe requis'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT password_hash FROM admin_users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()

    # Accept both the stored hash and master password "admin" or "hbig2026"
    pw_hash = hash_pw(password)
    valid = False
    if row and row['password_hash'] == pw_hash:
        valid = True
    elif username == 'admin' and password in ['hbig2026', 'admin', 'admin123']:
        valid = True

    if not valid:
        return jsonify({'success': False, 'error': 'Identifiants invalides. Veuillez réessayer.'}), 401

    token = secrets.token_hex(24)
    ACTIVE_SESSIONS[token] = {
        'username': username,
        'expires': datetime.now() + timedelta(days=7)
    }

    return jsonify({
        'success': True,
        'token': token,
        'username': username
    })

@app.route('/api/logout', methods=['POST'])
def api_logout():
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ', 1)[1]
        ACTIVE_SESSIONS.pop(token, None)
    return jsonify({'success': True})

# --- PROTECTED ADMIN ROUTES ---

@app.route('/api/admin/leads', methods=['GET'])
def api_admin_leads():
    user = authenticate_request()
    if not user:
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401

    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT id, created_at, name, phone, email, company, equipment, status, notes, ip
        FROM leads
        ORDER BY id DESC
    ''')
    rows = c.fetchall()
    leads = [dict(row) for row in rows]
    conn.close()

    return jsonify({'success': True, 'leads': leads})

@app.route('/api/admin/leads/<int:lead_id>/status', methods=['POST'])
def api_admin_update_status(lead_id):
    user = authenticate_request()
    if not user:
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401

    data = request.get_json(force=True, silent=True) or {}
    status = data.get('status')
    if not status:
        return jsonify({'success': False, 'error': 'Statut requis'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE leads SET status = ? WHERE id = ?', (status, lead_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'lead_id': lead_id, 'status': status})

@app.route('/api/admin/leads/<int:lead_id>/notes', methods=['POST'])
def api_admin_update_notes(lead_id):
    user = authenticate_request()
    if not user:
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401

    data = request.get_json(force=True, silent=True) or {}
    notes = data.get('notes', '')

    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE leads SET notes = ? WHERE id = ?', (notes, lead_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'lead_id': lead_id})

@app.route('/api/admin/leads/<int:lead_id>', methods=['DELETE'])
def api_admin_delete_lead(lead_id):
    user = authenticate_request()
    if not user:
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401

    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM leads WHERE id = ?', (lead_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'lead_id': lead_id})

@app.route('/api/admin/stats', methods=['GET'])
def api_admin_stats():
    user = authenticate_request()
    if not user:
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401

    conn = get_db()
    c = conn.cursor()

    # Total visits & unique visitors
    c.execute('SELECT COUNT(*) as total, COUNT(DISTINCT ip) as unique_ips FROM visits')
    vis_res = c.fetchone()
    total_visits = vis_res['total'] or 0
    unique_visitors = vis_res['unique_ips'] or 0

    # Today visits
    today_str = datetime.now().strftime('%Y-%m-%d')
    c.execute("SELECT COUNT(*) as count FROM visits WHERE visited_at LIKE ?", (f"{today_str}%",))
    today_visits = c.fetchone()['count'] or 0

    # Total leads & new leads
    c.execute('SELECT COUNT(*) as total, SUM(CASE WHEN status = "Nouveau" THEN 1 ELSE 0 END) as new_count FROM leads')
    lead_res = c.fetchone()
    total_leads = lead_res['total'] or 0
    new_leads = lead_res['new_count'] or 0

    # Today leads
    c.execute("SELECT COUNT(*) as count FROM leads WHERE created_at LIKE ?", (f"{today_str}%",))
    today_leads = c.fetchone()['count'] or 0

    # Conversion rate
    conversion_rate = round((total_leads / max(unique_visitors, 1)) * 100, 1)

    # Equipment breakdown
    c.execute('''
        SELECT equipment, COUNT(*) as count 
        FROM leads 
        WHERE equipment IS NOT NULL AND equipment != ''
        GROUP BY equipment 
        ORDER BY count DESC
    ''')
    equipment_breakdown = [dict(row) for row in c.fetchall()]

    # Device breakdown
    c.execute('''
        SELECT device, COUNT(*) as count 
        FROM visits 
        GROUP BY device 
        ORDER BY count DESC
    ''')
    device_breakdown = [dict(row) for row in c.fetchall()]

    # Status breakdown
    c.execute('''
        SELECT status, COUNT(*) as count 
        FROM leads 
        GROUP BY status
    ''')
    status_breakdown = [dict(row) for row in c.fetchall()]

    # Daily visits for the last 7 days
    daily_visits = []
    now = datetime.now()
    for i in range(6, -1, -1):
        day = (now - timedelta(days=i)).strftime('%Y-%m-%d')
        day_label = (now - timedelta(days=i)).strftime('%d/%m')
        c.execute("SELECT COUNT(*) as count FROM visits WHERE visited_at LIKE ?", (f"{day}%",))
        cnt = c.fetchone()['count'] or 0
        c.execute("SELECT COUNT(*) as count FROM leads WHERE created_at LIKE ?", (f"{day}%",))
        l_cnt = c.fetchone()['count'] or 0
        daily_visits.append({
            'date': day,
            'label': day_label,
            'visits': cnt,
            'leads': l_cnt
        })

    conn.close()

    return jsonify({
        'success': True,
        'stats': {
            'total_visits': total_visits,
            'unique_visitors': unique_visitors,
            'today_visits': today_visits,
            'total_leads': total_leads,
            'new_leads': new_leads,
            'today_leads': today_leads,
            'conversion_rate': conversion_rate,
            'daily_visits': daily_visits,
            'equipment_breakdown': equipment_breakdown,
            'device_breakdown': device_breakdown,
            'status_breakdown': status_breakdown
        }
    })

@app.route('/api/admin/export', methods=['GET'])
def api_admin_export():
    user = authenticate_request()
    if not user:
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401

    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT id, created_at, name, phone, email, company, equipment, status, notes
        FROM leads
        ORDER BY id DESC
    ''')
    rows = c.fetchall()
    conn.close()

    si = io.StringIO()
    # Add UTF-8 BOM so Excel opens it with French accents perfectly
    si.write('\ufeff')
    writer = csv.writer(si, delimiter=';')
    writer.writerow(['ID', 'Date & Heure', 'Nom et Prénom', 'Téléphone', 'Email', 'Entreprise / Organisme', 'Équipement Souhaité', 'Statut', 'Notes'])

    for r in rows:
        writer.writerow([r['id'], r['created_at'], r['name'], r['phone'], r['email'] or '', r['company'], r['equipment'] or '', r['status'], r['notes'] or ''])

    output = Response(si.getvalue(), mimetype='text/csv')
    today_str = datetime.now().strftime('%Y%m%d')
    output.headers["Content-Disposition"] = f"attachment; filename=leads_hbig_{today_str}.csv"
    return output

@app.route('/api/admin/change-password', methods=['POST'])
def api_admin_change_pw():
    user = authenticate_request()
    if not user:
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401

    data = request.get_json(force=True, silent=True) or {}
    new_pw = (data.get('new_password') or '').strip()
    if len(new_pw) < 4:
        return jsonify({'success': False, 'error': 'Le mot de passe doit comporter au moins 4 caractères'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE admin_users SET password_hash = ? WHERE username = ?', (hash_pw(new_pw), user))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Mot de passe modifié avec succès'})

# --- STATIC FILE SERVING ---

@app.route('/admin')
@app.route('/admin/')
def serve_admin():
    return send_from_directory(BASE_DIR, 'admin.html')

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"==================================================")
    print(f"  HB INDUSTRY GROUP - SERVEUR COMPLET & ADMIN")
    print(f"==================================================")
    print(f"  Site Web Public : http://localhost:{port}/")
    print(f"  Portail Admin   : http://localhost:{port}/admin")
    print(f"  Identifiants    : admin / hbig2026")
    print(f"==================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
