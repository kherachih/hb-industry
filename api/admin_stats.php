<?php
require_once __DIR__ . '/db.php';

$user = authenticate_request();
if (!$user) {
    json_response(['success' => false, 'error' => 'Non autorisé'], 401);
}

$pdo = get_db();

// Total visits & unique visitors
$vis_res = $pdo->query("SELECT COUNT(*) as total, COUNT(DISTINCT ip) as unique_ips FROM visits")->fetch();
$total_visits = (int)($vis_res['total'] ?? 0);
$unique_visitors = (int)($vis_res['unique_ips'] ?? 0);

// Today visits
$today_str = date('Y-m-d');
$st = $pdo->prepare("SELECT COUNT(*) as count FROM visits WHERE visited_at LIKE ?");
$st->execute([$today_str . '%']);
$today_visits = (int)($st->fetch()['count'] ?? 0);

// Total leads & new leads
$lead_res = $pdo->query("SELECT COUNT(*) as total, SUM(CASE WHEN status = 'Nouveau' THEN 1 ELSE 0 END) as new_count FROM leads")->fetch();
$total_leads = (int)($lead_res['total'] ?? 0);
$new_leads = (int)($lead_res['new_count'] ?? 0);

// Today leads
$st2 = $pdo->prepare("SELECT COUNT(*) as count FROM leads WHERE created_at LIKE ?");
$st2->execute([$today_str . '%']);
$today_leads = (int)($st2->fetch()['count'] ?? 0);

// Conversion rate
$denom = max($unique_visitors, 1);
$conversion_rate = round(($total_leads / $denom) * 100, 1);

// Equipment breakdown
$eq_rows = $pdo->query("
    SELECT equipment, COUNT(*) as count 
    FROM leads 
    WHERE equipment IS NOT NULL AND equipment != ''
    GROUP BY equipment 
    ORDER BY count DESC
")->fetchAll();
$equipment_breakdown = array_map(function($r) {
    return ['equipment' => $r['equipment'], 'count' => (int)$r['count']];
}, $eq_rows);

// Device breakdown
$dev_rows = $pdo->query("
    SELECT device, COUNT(*) as count 
    FROM visits 
    GROUP BY device 
    ORDER BY count DESC
")->fetchAll();
$device_breakdown = array_map(function($r) {
    return ['device' => $r['device'], 'count' => (int)$r['count']];
}, $dev_rows);

// Status breakdown
$st_rows = $pdo->query("
    SELECT status, COUNT(*) as count 
    FROM leads 
    GROUP BY status
")->fetchAll();
$status_breakdown = array_map(function($r) {
    return ['status' => $r['status'], 'count' => (int)$r['count']];
}, $st_rows);

// Daily visits for last 7 days
$daily_visits = [];
for ($i = 6; $i >= 0; $i--) {
    $ts = strtotime("-$i days");
    $day = date('Y-m-d', $ts);
    $day_label = date('d/m', $ts);

    $s_v = $pdo->prepare("SELECT COUNT(*) as count FROM visits WHERE visited_at LIKE ?");
    $s_v->execute([$day . '%']);
    $cnt_v = (int)($s_v->fetch()['count'] ?? 0);

    $s_l = $pdo->prepare("SELECT COUNT(*) as count FROM leads WHERE created_at LIKE ?");
    $s_l->execute([$day . '%']);
    $cnt_l = (int)($s_l->fetch()['count'] ?? 0);

    $daily_visits[] = [
        'date' => $day,
        'label' => $day_label,
        'visits' => $cnt_v,
        'leads' => $cnt_l
    ];
}

json_response([
    'success' => true,
    'stats' => [
        'total_visits' => $total_visits,
        'unique_visitors' => $unique_visitors,
        'today_visits' => $today_visits,
        'total_leads' => $total_leads,
        'new_leads' => $new_leads,
        'today_leads' => $today_leads,
        'conversion_rate' => $conversion_rate,
        'daily_visits' => $daily_visits,
        'equipment_breakdown' => $equipment_breakdown,
        'device_breakdown' => $device_breakdown,
        'status_breakdown' => $status_breakdown
    ]
]);
