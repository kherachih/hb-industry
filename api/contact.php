<?php
require_once __DIR__ . '/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    json_response(['success' => false, 'error' => 'Méthode non autorisée'], 405);
}

$data = get_json_input();
$name = trim($data['name'] ?? '');
$phone = trim($data['phone'] ?? '');
$email = trim($data['email'] ?? '');
$company = trim($data['company'] ?? '');
$equipment = trim($data['00NHn00000ZTeTu'] ?? $data['equipment'] ?? '');

if (empty($name) || empty($phone) || empty($company)) {
    json_response([
        'success' => false,
        'error' => 'Veuillez remplir tous les champs obligatoires (Nom, Téléphone, Entreprise).'
    ], 400);
}

$ip = get_client_ip();
$ua = $_SERVER['HTTP_USER_AGENT'] ?? '';

try {
    $pdo = get_db();
    $stmt = $pdo->prepare("
        INSERT INTO leads (name, phone, email, company, equipment, status, notes, ip, user_agent)
        VALUES (?, ?, ?, ?, ?, 'Nouveau', '', ?, ?)
    ");
    $stmt->execute([$name, $phone, $email, $company, $equipment, $ip, $ua]);
    $lead_id = (int)$pdo->lastInsertId();

    json_response([
        'success' => true,
        'message' => "Demande de devis transmise avec succès au bureau d'études HBIG.",
        'lead_id' => $lead_id
    ]);
} catch (Exception $e) {
    json_response(['success' => false, 'error' => 'Erreur de base de données'], 500);
}
