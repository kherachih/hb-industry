<?php
$uri = $_SERVER['REQUEST_URI'] ?? '';
$path = parse_url($uri, PHP_URL_PATH);

// Normalize path: strip prefix up to /api/
$route = '';
if (preg_match('#/api/(.+)$#', $path, $m)) {
    $route = $m[1];
}

if ($route === 'contact' || $route === 'contact.php') {
    require __DIR__ . '/contact.php';
    exit;
}
if ($route === 'track' || $route === 'track.php') {
    require __DIR__ . '/track.php';
    exit;
}
if ($route === 'login' || $route === 'login.php') {
    require __DIR__ . '/login.php';
    exit;
}
if ($route === 'logout' || $route === 'logout.php') {
    require __DIR__ . '/logout.php';
    exit;
}
if ($route === 'admin/stats' || $route === 'admin_stats.php') {
    require __DIR__ . '/admin_stats.php';
    exit;
}
if ($route === 'admin/leads' || $route === 'admin_leads.php') {
    require __DIR__ . '/admin_leads.php';
    exit;
}
if ($route === 'admin/export' || $route === 'admin_export.php') {
    require __DIR__ . '/admin_export.php';
    exit;
}
if ($route === 'admin/change-password' || $route === 'admin_change_password.php') {
    require __DIR__ . '/admin_change_password.php';
    exit;
}

if (preg_match('#^admin/leads/(\d+)/status#', $route, $m)) {
    $_GET['id'] = $m[1];
    $_GET['action'] = 'status';
    require __DIR__ . '/lead_action.php';
    exit;
}
if (preg_match('#^admin/leads/(\d+)/notes#', $route, $m)) {
    $_GET['id'] = $m[1];
    $_GET['action'] = 'notes';
    require __DIR__ . '/lead_action.php';
    exit;
}
if (preg_match('#^admin/leads/(\d+)#', $route, $m)) {
    $_GET['id'] = $m[1];
    $_GET['action'] = 'delete';
    require __DIR__ . '/lead_action.php';
    exit;
}

http_response_code(404);
header('Content-Type: application/json');
echo json_encode(['error' => 'API route not found', 'route' => $route]);
