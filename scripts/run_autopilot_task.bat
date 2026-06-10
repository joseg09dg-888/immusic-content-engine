@echo off
REM Wrapper para Windows Task Scheduler — IM Music Autopilot Diario
REM Corre L/M/V 8:00 AM COT. Genera contenido + beat del dia (NO publica).
cd /d "C:\Users\jose-\immusic-content-engine"
set PYTHONPATH=C:\Users\jose-\immusic-content-engine
"C:\Users\jose-\AppData\Local\Programs\Python\Python312\python.exe" scripts\autopilot_diario.py >> "C:\Users\jose-\immusic-content-engine\logs\autopilot_diario.log" 2>&1
