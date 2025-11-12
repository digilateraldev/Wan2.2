#!/bin/bash
set -eo pipefail

# Activate virtual environment
. /venv/main/bin/activate

# Ensure logs and supervisor config dirs exist
mkdir -p /workspace/logs /etc/supervisor/conf.d

# Navigate to your app directory
cd /workspace/Wan-2.2 || exit 1

# Write Supervisor program config for FastAPI
cat >/etc/supervisor/conf.d/fastapi.conf <<'EOF'
[program:fastapi]
directory=/workspace/Wan-2.2
command=/venv/main/bin/uvicorn api:app --host 0.0.0.0 --port 8000
autostart=true
autorestart=true
startsecs=3
stopasgroup=true
killasgroup=true
stderr_logfile=/workspace/logs/fastapi_err.log
stdout_logfile=/workspace/logs/fastapi_out.log
EOF

# Update environment variables globally (optional)
env | grep _ >> /etc/environment || true

# Start Supervisor and ensure it's running our app
supervisord -c /etc/supervisord.conf
supervisorctl reread
supervisorctl update
supervisorctl start fastapi
