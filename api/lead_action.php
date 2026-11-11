<?php
require_once __DIR__ . '/db.php';

$user = authenticate_request();
if (!$user) {
    json_response(['success' => false, 'error' => 'Non autorisé'], 401);
}

$lead_id = (int)($_GET['id'] ?? 0);
$action = $_GET['action'] ?? '';
$method = $_SERVER['REQUEST_METHOD'];

// Also support action determination from method
if ($method === 'DELETE' || $action === 'delete') {
    if (!$lead_id) {
        json_response(['success' => false, 'error' => 'ID requis'], 400);
    }
    $pdo = get_db();
    $stmt = $pdo->prepare("DELETE FROM leads WHERE id = ?");
    $stmt->execute([$lead_id]);
    json_response(['success' => true, 'lead_id' => $lead_id]);
}

$data = get_json_input();

if ($action === 'status') {
    $status = trim($data['status'] ?? '');
    if (!$status || !$lead_id) {
        json_response(['success' => false, 'error' => 'Statut et ID requis'], 400);
    }
    $pdo = get_db();
    $stmt = $pdo->prepare("UPDATE leads SET status = ? WHERE id = ?");
    $stmt->execute([$status, $lead_id]);
    json_response(['success' => true, 'lead_id' => $lead_id, 'status' => $status]);
}

if ($action === 'notes') {
    $notes = $data['notes'] ?? '';
    if (!$lead_id) {
        json_response(['success' => false, 'error' => 'ID requis'], 400);
    }
    $pdo = get_db();
    $stmt = $pdo->prepare("UPDATE leads SET notes = ? WHERE id = ?");
    $stmt->execute([$notes, $lead_id]);
    json_response(['success' => true, 'lead_id' => $lead_id]);
}

json_response(['success' => false, 'error' => 'Action inconnue'], 400);
