@echo off
chcp 65001 >nul
title 峰子分析 Fengzi Analysis
cd /d "%~dp0"

if not exist ".venv\Scripts\streamlit.exe" (
    echo [峰子分析] 首次运行，正在安装依赖...
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -m venv .venv 2>nul
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt -q
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo  峰子分析 · Fengzi Analysis
echo  浏览器将打开 http://localhost:8501
echo.
start "" "http://localhost:8501"
streamlit run app.py --server.headless true
pause
