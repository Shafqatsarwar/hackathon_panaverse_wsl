# Quick Odoo Setup with Docker
# This script helps you set up Odoo locally using Docker

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Odoo CRM - Quick Docker Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "[1/5] Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "  Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Docker is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Docker Desktop from:" -ForegroundColor Yellow
    Write-Host "  https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# Check if Odoo container already exists
Write-Host ""
Write-Host "[2/5] Checking for existing Odoo container..." -ForegroundColor Yellow
$existingContainer = docker ps -a --filter "name=odoo" --format "{{.Names}}"

if ($existingContainer -eq "odoo") {
    Write-Host "  Found existing Odoo container" -ForegroundColor Yellow
    $response = Read-Host "  Do you want to remove it and start fresh? (y/n)"
    if ($response -eq "y") {
        Write-Host "  Removing existing container..." -ForegroundColor Yellow
        docker stop odoo 2>$null
        docker rm odoo 2>$null
        Write-Host "  Container removed" -ForegroundColor Green
    } else {
        Write-Host "  Keeping existing container" -ForegroundColor Green
        Write-Host ""
        Write-Host "To start existing container:" -ForegroundColor Cyan
        Write-Host "  docker start odoo" -ForegroundColor White
        exit 0
    }
}

# Start PostgreSQL database
Write-Host ""
Write-Host "[3/5] Starting PostgreSQL database..." -ForegroundColor Yellow
$existingDb = docker ps -a --filter "name=odoo-db" --format "{{.Names}}"

if ($existingDb -eq "odoo-db") {
    Write-Host "  Found existing database container" -ForegroundColor Yellow
    docker start odoo-db 2>$null
} else {
    docker run -d `
        -e POSTGRES_USER=odoo `
        -e POSTGRES_PASSWORD=odoo `
        -e POSTGRES_DB=postgres `
        --name odoo-db `
        postgres:13
}
Write-Host "  Database started" -ForegroundColor Green

# Wait for database to be ready
Write-Host "  Waiting for database to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start Odoo container
Write-Host ""
Write-Host "[4/5] Starting Odoo container..." -ForegroundColor Yellow
docker run -d `
    -p 8069:8069 `
    --name odoo `
    --link odoo-db:db `
    -e HOST=db `
    -e USER=odoo `
    -e PASSWORD=odoo `
    odoo:latest

Write-Host "  Odoo container started" -ForegroundColor Green

# Wait for Odoo to start
Write-Host ""
Write-Host "[5/5] Waiting for Odoo to start (this may take 30-60 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

$maxAttempts = 12
$attempt = 0
$odooReady = $false

while ($attempt -lt $maxAttempts -and -not $odooReady) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8069" -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $odooReady = $true
        }
    } catch {
        $attempt++
        Write-Host "  Attempt $attempt/$maxAttempts..." -ForegroundColor Gray
        Start-Sleep -Seconds 5
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Odoo Setup Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Open Odoo in your browser:" -ForegroundColor Yellow
Write-Host "   http://localhost:8069" -ForegroundColor White
Write-Host ""
Write-Host "2. Create a database:" -ForegroundColor Yellow
Write-Host "   - Master Password: admin" -ForegroundColor White
Write-Host "   - Database Name: odoo_crm" -ForegroundColor White
Write-Host "   - Email: admin@example.com" -ForegroundColor White
Write-Host "   - Password: admin" -ForegroundColor White
Write-Host "   - Select 'CRM' app" -ForegroundColor White
Write-Host ""
Write-Host "3. Update your .env file:" -ForegroundColor Yellow
Write-Host "   ODOO_URL=http://localhost:8069" -ForegroundColor White
Write-Host "   ODOO_DB=odoo_crm" -ForegroundColor White
Write-Host "   ODOO_USERNAME=admin@example.com" -ForegroundColor White
Write-Host "   ODOO_PASSWORD=admin" -ForegroundColor White
Write-Host ""
Write-Host "4. Test the connection:" -ForegroundColor Yellow
Write-Host "   python tests/test_odoo_connection.py" -ForegroundColor White
Write-Host ""
Write-Host "Useful Docker Commands:" -ForegroundColor Cyan
Write-Host "  Stop Odoo:    docker stop odoo odoo-db" -ForegroundColor Gray
Write-Host "  Start Odoo:   docker start odoo-db odoo" -ForegroundColor Gray
Write-Host "  View logs:    docker logs odoo" -ForegroundColor Gray
Write-Host "  Remove all:   docker rm -f odoo odoo-db" -ForegroundColor Gray
Write-Host ""

# Open browser
$openBrowser = Read-Host "Open Odoo in browser now? (y/n)"
if ($openBrowser -eq "y") {
    Start-Process "http://localhost:8069"
}
