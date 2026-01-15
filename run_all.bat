@echo off
echo ============================================
echo  Systeme de Planification des Examens
echo ============================================
echo.

echo 1. Installation des dependances...
pip install -r requirements.txt

echo.
echo 2. Demarrage de l'application...
streamlit run app.py

pause