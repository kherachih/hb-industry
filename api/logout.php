<?php
require_once __DIR__ . '/db.php';

$headers = getallheaders();
$auth = $headers['Authorization'] ?? $headers['authorization'] ?? $_SERVER['HTTP_AUTHORIZATION'] ?? '';
if (preg_match('/Bearer\s+(\S+)/i', $auth, $m)) {
    $token = $m[1];
    $pdo = get_db();
    $del = $pdo->prepare("DELETE FROM sessions WHERE token = ?");
    $del->execute([$token]);
}

json_response(['success' => true]);
