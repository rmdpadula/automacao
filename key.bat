@echo off
:: Verificar se está sendo executado como administrador
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Este script deve ser executado como administrador.
    pause
    exit /b
)

:: Nome da variável de ambiente
set VARIAVEL=Netlogic_Intersistemas

:: Chave de criptografia (substitua pela chave gerada)
set VALOR=X01d0zqSzxmTpnfNcL15Qh-lpAyxWe_dL87SrKyHAG0=

:: Configurando a variável de ambiente no sistema
echo Configurando a variável de ambiente...
setx %VARIAVEL% "%VALOR%" /M

:: Confirmando a configuração
if %ERRORLEVEL% EQU 0 (
    echo Variavel de ambiente "%VARIAVEL%" configurada com sucesso!
) else (
    echo Erro ao configurar a variavel de ambiente.
    pause
    exit /b
)

:: Excluindo o arquivo BAT após execução
del "%~f0"

:: Finalizando
pause
