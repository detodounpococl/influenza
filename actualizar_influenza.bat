@echo off
echo ==============================
echo ACTUALIZANDO DASHBOARD INFLUENZA
echo ==============================

cd /d "C:\Users\14538348-k\Desktop\DASHBOARD (html)\Nuevos\INFL\influenza"

echo.
echo [1] Verificando archivos...
if not exist "datos.json" (
    echo ERROR: No existe datos.json en esta carpeta
    pause
    exit /b 1
)

if not exist "index.html" (
    echo ERROR: No existe index.html en esta carpeta
    pause
    exit /b 1
)

echo.
echo [2] Estado Git...
git status

echo.
echo [3] Agregando cambios...
git add .

echo.
echo [4] Verificando cambios preparados...
git diff --staged --quiet
IF %ERRORLEVEL%==0 (
    echo No hay cambios para subir.
) ELSE (
    echo [5] Haciendo commit...
    git commit -m "update influenza (index + json)"

    echo [6] Subiendo a GitHub...
    git push
)

echo.
echo ==============================
echo PROCESO FINALIZADO
echo ==============================
pause