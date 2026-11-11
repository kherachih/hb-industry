<?php
error_reporting(0);
ini_set('display_errors', 0);

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if (!function_exists('getallheaders')) {
    function getallheaders() {
        $headers = [];
        foreach ($_SERVER as $name => $value) {
            if (substr($name, 0, 5) === 'HTTP_') {
                $header_key = str_replace(' ', '-', ucwords(strtolower(str_replace('_', ' ', substr($name, 5)))));
                $headers[$header_key] = $value;
            }
        }
        return $headers;
    }
}

$db_dir = __DIR__ . '/../data';
if (!is_dir($db_dir)) {
    @mkdir($db_dir, 0755, true);
}
$db_file = $db_dir . '/hbig.db';

function get_db() {
    global $db_file;
    static $pdo = null;
    if ($pdo === null) {
        $pdo = new PDO('sqlite:' . $db_file);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        init_db($pdo);
    }
    return $pdo;
}

function init_db($pdo) {
    $pdo->exec("
        CREATE TABLE IF NOT EXISTS admin_users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
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
        );
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip TEXT,
            user_agent TEXT,
            device TEXT,
            path TEXT,
            referrer TEXT
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            expires_at DATETIME NOT NULL
        );
    ");

    $stmt = $pdo->prepare("SELECT * FROM admin_users WHERE username = ?");
    $stmt->execute(['admin']);
    if (!$stmt->fetch()) {
        $hash = hash_password('hbig2026');
        $ins = $pdo->prepare("INSERT INTO admin_users (username, password_hash) VALUES (?, ?)");
        $ins->execute(['admin', $hash]);
    }
}

function hash_password($pw) {
    return hash('sha256', $pw);
}

function json_response($data, $code = 200) {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

function get_json_input() {
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);
    if (!is_array($data)) {
        $data = $_POST;
    }
    return $data ?? [];
}

function get_client_ip() {
    if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $parts = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        return trim($parts[0]);
    }
    return $_SERVER['REMOTE_ADDR'] ?? '';
}

function authenticate_request() {
    $token = null;
    $headers = getallheaders();
    
    // Check various auth header variants
    $auth = $headers['Authorization'] ?? $headers['authorization'] ?? $_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '';
    if (preg_match('/Bearer\s+(\S+)/i', $auth, $m)) {
        $token = $m[1];
    } elseif (!empty($_GET['token'])) {
        $token = $_GET['token'];
    } elseif (!empty($_POST['token'])) {
        $token = $_POST['token'];
    }

    if (!$token) {
        return null;
    }

    $pdo = get_db();
    $stmt = $pdo->prepare("SELECT username, expires_at FROM sessions WHERE token = ?");
    $stmt->execute([$token]);
    $row = $stmt->fetch();
    if (!$row) {
        return null;
    }

    if (strtotime($row['expires_at']) < time()) {
        $del = $pdo->prepare("DELETE FROM sessions WHERE token = ?");
        $del->execute([$token]);
        return null;
    }

    return $row['username'];
}
