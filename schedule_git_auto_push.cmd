@echo off
echo Scheduling Git auto-push script...
schtasks /create /tn "GitAutoPush" /tr "C:\Users\coryd\ScraperBot\git_auto_push.bat" /sc minute /mo 5 /f
echo Git auto-push script scheduled.
pause
