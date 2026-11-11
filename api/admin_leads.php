<?php
require_once __DIR__ . '/db.php';

$user = authenticate_request();
if (!$user) {
    json_response(['success' => false, 'error' => 'Non autorisé'], 401);
}

$pdo = get_db();
$rows = $pdo->query("
    SELECT id, created_at, name, phone, email, company, equipment, status, notes, ip
    FROM leads
    ORDER BY id DESC
")->fetchAll();

$leads = array_map(function($r) {
    return [
        'id' => (int)$r['id'],
        'created_at' => $r['created_at'],
        'name' => $r['name'],
        'phone' => $r['phone'],
        'email' => $r['email'] ?? '',
        'company' => $r['company'],
        'equipment' => $r['equipment'] ?? '',
        'status' => $r['status'] ?? 'Nouveau',
        'notes' => $r['notes'] ?? '',
        'ip' => $r['ip'] ?? ''
    ];
}, $rows);

json_response([
    'success' => true,
    'leads' => $leads
]);
