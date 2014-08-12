@echo off
start "server" /min cmd.exe /c server.cmd
sleep 1
C:\Users\liux\AppData\Local\Google\Chrome\Application\chrome.exe 127.0.0.1:8080 --new-window 