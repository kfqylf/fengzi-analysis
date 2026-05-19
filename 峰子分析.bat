@echo off
chcp 65001 >nul
title 峰子分析 Fengzi Analysis
cd /d "%~dp0"

:: Auto-detect Python
set "PY="
where python >nul 2>&1 && set "PY=python"
if not defined PY (
    where python3 >nul 2>&1 && set "PY=python3"
)
if not defined PY (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    )
)
if not defined PY (
    if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
        set "PY=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    )
)
if not defined PY (
    echo.
    echo  [错误] 未找到 Python，请先安装 Python 3.10+
    echo  下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\streamlit.exe" (
    echo.
    echo  [峰子分析] 首次运行，正在创建虚拟环境并安装依赖...
    echo  这可能需要 1-2 分钟，请耐心等待...
    echo.
    %PY% -m venv .venv
    if errorlevel 1 (
        echo  [错误] 创建虚拟环境失败，请检查 Python 安装
        pause
        exit /b 1
    )
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt -q
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo  ╔══════════════════════════════════════╗
echo  ║   峰子分析 · Fengzi Analysis          ║
echo  ║   浏览器即将打开 http://localhost:8501  ║
echo  ║   关闭此窗口即可停止程序               ║
echo  ╚══════════════════════════════════════╝
echo.
start "" "http://localhost:8501"
streamlit run app.py --server.headless true
pause
