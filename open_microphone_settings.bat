@echo off
echo Opening Windows Sound Settings...
echo.
echo Please:
echo 1. Select your microphone (Microphone Array on SoundWire D)
echo 2. Set volume to 100%%
echo 3. Enable Microphone Boost (+20dB or +30dB)
echo 4. Disable noise suppression (temporarily)
echo.
echo After adjusting settings, close this window and run:
echo    python -m test.test_simple_wake_word
echo.
pause

REM Open Sound Settings
start ms-settings:sound

REM Alternative: Open classic Sound Control Panel
REM control mmsys.cpl,,1
