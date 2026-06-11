<?php
session_start();
header('Content-Type: application/json');

function fail(string $msg, int $code = 400): void {
    http_response_code($code);
    echo json_encode(['success' => false, 'error' => $msg]);
    exit;
}

if (empty($_SESSION['vibe_auth'])) fail('Unauthorized.', 401);

$allowed  = ['repo1', 'repo2'];
$project  = trim($_POST['project'] ?? '');
$prompt   = trim($_POST['prompt']  ?? '');

if (!in_array($project, $allowed, true)) fail('Invalid project.');
if (!$prompt)                            fail('Prompt is required.');

$ntfy = json_encode([
    'topic'    => 'your-private-topic',
    'title'    => "Vibe | {$project}",
    'message'  => json_encode([
        'project' => $project,
        'prompt'  => $prompt,
        'ts'      => date('Y-m-d H:i:s'),
    ]),
    'priority' => 3,
    'tags'     => ['zap'],
]);

$ch = curl_init('https://ntfy.sh');
curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => $ntfy,
    CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 5,
]);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_exec($ch);
curl_close($ch);

if ($http_code >= 400) fail("ntfy.sh returned HTTP {$http_code}.");

echo json_encode(['success' => true]);
