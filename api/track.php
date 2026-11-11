<?php
require_once __DIR__ . '/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    json_response(['success' => false, 'error' => 'Méthode non autorisée'], 405);
}

$data = get_json_input();
$path = $data['path'] ?? '/';
$referrer = $data['referrer'] ?? '';
$device = $data['device'] ?? 'Desktop';

$ip = get_client_ip();
$ua = $_SERVER['HTTP_USER_AGENT'] ?? '';

try {
    $pdo = get_db();
    $stmt = $pdo->prepare("
        INSERT INTO visits (ip, user_agent, device, path, referrer)
        VALUES (?, ?, ?, ?, ?)
    ");
    $stmt->execute([$ip, $ua, $device, $path, $referrer]);
    json_response(['success' => true]);
} catch (Exception $e) {
    json_response(['success' => false], 500);
}
