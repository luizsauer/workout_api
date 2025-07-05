Clear-Host

function Show-Menu {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "           GERENCIADOR DO PROJETO       " -ForegroundColor Green
    Write-Host "========================================"
    Write-Host "1 - Rodar API (Uvicorn)"
    Write-Host "2 - Criar migration (Alembic)"
    Write-Host "3 - Executar migrations (Alembic)"
    Write-Host "0 - Sair"
}

function Enable-Venv {
    .\venv\Scripts\Activate.ps1
}

do {
    Show-Menu
    $opcao = Read-Host "Escolha uma opcao"

    switch ($opcao) {
        "1" {
            Enable-Venv
            uvicorn workout_api.main:app --reload
        }
        "2" {
            Enable-Venv
            $desc = Read-Host "Digite a descricao da migration"
            $env:PYTHONPATH = Get-Location
            alembic revision --autogenerate -m "$desc"
            Read-Host "Pressione Enter para continuar"
        }
        "3" {
            Enable-Venv
            $env:PYTHONPATH = Get-Location
            try {
                alembic upgrade head
            } catch {
                Write-Host "Erro ao executar migrations:" -ForegroundColor Red
                Write-Host $_.Exception.Message -ForegroundColor Red
                Write-Host "Tentando resolver com stamp head..."
                alembic stamp head
                alembic upgrade head
            }
            Read-Host "Pressione Enter para continuar"
        }
        "0" {
            Write-Host "Saindo..." -ForegroundColor Yellow
        }
        default {
            Write-Host "Opcao invalida!" -ForegroundColor Red
        }
    }

} while ($opcao -ne "0")
