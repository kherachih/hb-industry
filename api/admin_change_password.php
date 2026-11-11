<?php
require_once __DIR__ . '/db.php';

$user = authenticate_request();
if (!$user) {
    json_response(['success' => false, 'error' => 'Non autorisé'], 401);
}

$data = get_json_input();
$new_pw = trim($data['new_password'] ?? '');

if (strlen($new_pw) < 4) {
    json_response(['success' => false, 'error' => 'Le mot de passe doit comporter au moins 4 caractères'], 400);
}

$pdo = get_db();
$hash = hash_password($new_pw);
$stmt = $pdo->prepare("UPDATE admin_users SET password_hash = ? WHERE username = ?");
$stmt->execute([$hash, $user]);

json_response(['success' => true, 'message' => 'Mot de passe modifié avec succès']);
