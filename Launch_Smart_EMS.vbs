Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strCurrentDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strCurrentDir

' Detect python binary
strPython = "python"
If fso.FileExists(WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python312\python.exe") Then
    strPython = WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python312\python.exe"
End If

' Check if port 8000 is listening
Set objExec = WshShell.Exec("cmd /c netstat -ano | findstr :8000 | findstr LISTENING")
strOutput = objExec.StdOut.ReadAll()

If InStr(strOutput, "LISTENING") = 0 Then
    ' Start the Django server in the background
    WshShell.Run "cmd /c """ & strPython & """ manage.py runserver 127.0.0.1:8000", 0, False
    WScript.Sleep 3000
End If

' Open the default browser to the application
WshShell.Run "cmd /c start http://127.0.0.1:8000/", 0, False
