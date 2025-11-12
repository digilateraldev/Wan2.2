mkdir -p /workspace/logs /etc/supervisor/conf.d
cat >/etc/supervisor/conf.d/fastapi.conf <<'EOF'
[program:fastapi]
command=bash -c '
  for i in {1..30}; do
    if [ -d "/workspace/Wan-2.2" ]; then
      echo "✅ /workspace/Wan-2.2 mounted."
      cd /workspace/Wan-2.2
      exec /venv/main/bin/uvicorn api:app --host 0.0.0.0 --port 8000
    fi
    echo "⏳ Waiting for /workspace/Wan-2.2... ($i/30)"
    sleep 2
  done
  echo "❌ Mount not found after 60s. Exiting."
  exit 1
'
autostart=true
autorestart=true
startsecs=3
startretries=10
stopasgroup=true
killasgroup=true
stopwaitsecs=15
stderr_logfile=/workspace/logs/fastapi_err.log
stdout_logfile=/workspace/logs/fastapi_out.log
EOF
supervisord -c /etc/supervisord.conf
supervisorctl reread
supervisorctl update
supervisorctl start fastapi
