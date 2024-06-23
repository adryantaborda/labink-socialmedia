# Define variables
$NAME = "myproject"  # Name of the application
$DJANGODIR = "C:\authentication-django\nginxserver"  # Django project directory
$SOCKFILE = "C:\authentication-django\nginxserver\run\gunicorn.sock"  # Unix socket path
$VIRTUAL_ENV = "C:\authentication-django\nginxserver\env"  # Path to your virtual environment
$NUM_WORKERS = 3  # How many worker processes should Gunicorn spawn
$DJANGO_SETTINGS_MODULE = "authdjango.settings"  # Which settings file should Django use
$DJANGO_WSGI_MODULE = "authdjango.wsgi"  # WSGI module name

# Start the application
Write-Output "Starting $NAME as $(whoami)"

# Activate the virtual environment
Set-Location $DJANGODIR
& $VIRTUAL_ENV\Scripts\Activate

# Create the run directory if it doesn't exist
$RUNDIR = [System.IO.Path]::GetDirectoryName($SOCKFILE)
If (-Not (Test-Path $RUNDIR)) {
    New-Item -ItemType Directory -Force -Path $RUNDIR
}

# Start Gunicorn
& "$VIRTUAL_ENV\Scripts\gunicorn.exe" "$DJANGO_WSGI_MODULE`:application" `
  --name $NAME `
  --workers $NUM_WORKERS `
  --bind "unix:$SOCKFILE" `
  --log-level debug `
  --log-file -
