@echo off
chcp 65001 >nul
echo 🍅 Micro Tomato - 学术论文图解助手
echo ==========================================
echo.
echo 🚀 正在启动应用...
echo 🌐 将在浏览器中打开应用界面
echo.

cd /d "%~dp0"

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查Streamlit
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 📦 安装Streamlit...
    pip install streamlit requests
)

REM 创建必要的目录
if not exist "temp_uploads" mkdir temp_uploads
if not exist ".streamlit" mkdir .streamlit

echo ✅ 环境检查完成，正在启动应用...
echo 🌐 应用地址: http://localhost:8501
echo 📄 文件: paper_demo.py
echo.

REM 启动主应用
python -m streamlit run paper_demo.py --server.port 8501

if errorlevel 1 (
    echo ❌ 启动失败
    pause
)