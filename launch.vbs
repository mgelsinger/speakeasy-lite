Dim fso, dir, shell
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
Set shell = CreateObject("WScript.Shell")
shell.Run Chr(34) & dir & "\.venv\Scripts\pythonw.exe" & Chr(34) & " " & Chr(34) & dir & "\app\main.py" & Chr(34), 0, False
