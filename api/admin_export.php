<?php
require_once __DIR__ . '/db.php';

$user = authenticate_request();
if (!$user) {
    json_response(['success' => false, 'error' => 'Non autorisé'], 401);
}

$pdo = get_db();
$rows = $pdo->query("
    SELECT id, created_at, name, phone, email, company, equipment, status, notes
    FROM leads
    ORDER BY id DESC
")->fetchAll();

$today_str = date('Ymd');
header('Content-Type: text/csv; charset=UTF-8');
header('Content-Disposition: attachment; filename="leads_hbig_' . $today_str . '.csv"');
header('Pragma: no-cache');
header('Expires: 0');

// UTF-8 BOM
echo "\xEF\xBB\xBF";

$fp = fopen('php://output', 'w');
fputcsv($fp, ['ID', 'Date & Heure', 'Nom et Prénom', 'Téléphone', 'Email', 'Entreprise / Organisme', 'Équipement Souhaité', 'Statut', 'Notes'], ';');

foreach ($rows as $r) {
    fputcsv($fp, [
        $r['id'],
        $r['created_at'],
        $r['name'],
        $r['phone'],
        $r['email'] ?? '',
        $r['company'],
        $r['equipment'] ?? '',
        $r['status'] ?? 'Nouveau',
        $r['notes'] ?? ''
    ], ';');
}

fclose($fp);
exit;
