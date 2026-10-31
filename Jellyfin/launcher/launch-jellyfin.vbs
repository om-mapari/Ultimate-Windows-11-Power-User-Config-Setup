Set WshShell = CreateObject("WScript.Shell")
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")

' Check if jellyfin.exe is already running
Set colProcesses = objWMIService.ExecQuery("Select * from Win32_Process Where Name = 'jellyfin.exe'")
If colProcesses.Count = 0 Then
    ' Start the Jellyfin tray app which launches and manages the server
    WshShell.Run """C:\Program Files\Jellyfin\Server\jellyfin-windows-tray\Jellyfin.Windows.Tray.exe""", 0, False
    
    ' Wait until Jellyfin web server is responding (up to 15 seconds)
    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    For i = 1 To 30
        On Error Resume Next
        http.open "GET", "http://127.0.0.1:8096/web/index.html", False
        http.send
        If Err.Number = 0 Then
            If http.status = 200 Then
                On Error Goto 0
                Exit For
            End If
        End If
        On Error Goto 0
        WScript.Sleep 500
    Next
End If

' Launch Brave in app mode
WshShell.Run """C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"" --app=""http://jellyfin.local:8096""", 1, False
