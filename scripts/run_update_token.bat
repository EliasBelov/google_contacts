@echo off
echo ZennoPoster directory = %ZennoPosterCurrentPath%
echo Starting task... (-names "[self-sufficient] - [PY] - Sync Google Contacts - Update token")
"%ZennoPosterCurrentPath%\TasksRunner.exe" -o StartTask -names "[self-sufficient] - [PY] - Sync Google Contacts - Update token"
timeout /t 1
echo Add 1 tries count... (-names "[self-sufficient] - [PY] - Sync Google Contacts - Update token")
"%ZennoPosterCurrentPath%\TasksRunner.exe" -o AddTries 1 -names "[self-sufficient] - [PY] - Sync Google Contacts - Update token"