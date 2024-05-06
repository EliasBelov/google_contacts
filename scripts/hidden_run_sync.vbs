Set WshShell = CreateObject("WScript.Shell")
WshShell.Run ".\run_sync.bat", 0, True
Set WshShell = Nothing
