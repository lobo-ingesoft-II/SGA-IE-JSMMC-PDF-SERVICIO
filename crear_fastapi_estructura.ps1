# Solicita el nombre del proyecto
$projectName = Read-Host "Nombre del proyecto"

# Crea carpetas principales
New-Item -Path $projectName\app\backend -ItemType Directory -Force
New-Item -Path $projectName\app\models -ItemType Directory -Force
New-Item -Path $projectName\app\routers -ItemType Directory -Force
New-Item -Path $projectName\app\schemas -ItemType Directory -Force
New-Item -Path $projectName\app\services -ItemType Directory -Force

# Archivos __init__.py en cada paquete
New-Item -Path "$projectName\app\__init__.py" -ItemType File -Force
New-Item -Path "$projectName\app\backend\__init__.py" -ItemType File -Force
New-Item -Path "$projectName\app\models\__init__.py" -ItemType File -Force
New-Item -Path "$projectName\app\routers\__init__.py" -ItemType File -Force
New-Item -Path "$projectName\app\schemas\__init__.py" -ItemType File -Force
New-Item -Path "$projectName\app\services\__init__.py" -ItemType File -Force

# Archivos principales
$mainFiles = "cli.py","const.py","exc.py","main.py"
foreach ($file in $mainFiles) {
    New-Item -Path "$projectName\app\$file" -ItemType File -Force
}

# Backend
New-Item -Path "$projectName\app\backend\config.py" -ItemType File -Force
New-Item -Path "$projectName\app\backend\session.py" -ItemType File -Force

# Models
New-Item -Path "$projectName\app\models\auth.py" -ItemType File -Force
New-Item -Path "$projectName\app\models\base.py" -ItemType File -Force

# Routers
New-Item -Path "$projectName\app\routers\auth.py" -ItemType File -Force

# Schemas
New-Item -Path "$projectName\app\schemas\auth.py" -ItemType File -Force

# Services
New-Item -Path "$projectName\app\services\auth.py" -ItemType File -Force
New-Item -Path "$projectName\app\services\base.py" -ItemType File -Force

# Otros archivos raíz
New-Item -Path "$projectName\requirements.txt" -ItemType File -Force
New-Item -Path "$projectName\.gitignore" -ItemType File -Force
New-Item -Path "$projectName\README.md" -ItemType File -Force

Write-Host "✅ Proyecto '$projectName' creado exitosamente"