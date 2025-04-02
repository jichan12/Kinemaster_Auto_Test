#!/bin/bash
# 프로젝트 실행 스크립트

# 1. 가상 환경 활성화
PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "가상 환경이 존재하지 않습니다. 먼저 배포 스크립트를 실행해 주세요."
    exit 1
fi

echo "가상 환경을 활성화합니다."
source "$VENV_DIR/bin/activate"

# 2. Redis 서버 실행 확인
if ! pgrep redis-server > /dev/null 2>&1; then
    echo "Redis 서버를 시작합니다."
    redis-server --daemonize yes
else
    echo "Redis 서버가 이미 실행 중입니다."
fi

# 3. Appium 서버 실행 확인
if ! pgrep appium > /dev/null 2>&1; then
    echo "Appium 서버를 새 터미널 창에서 실행합니다."
    osascript <<EOF
tell application "Terminal"
    do script "appium"
end tell
EOF
else
    echo "Appium 서버가 이미 실행 중입니다."
fi

# 4. Celery 워커 실행
echo "Celery 워커를 새 터미널 창에서 실행합니다."
osascript <<EOF
tell application "Terminal"
    do script "cd $PROJECT_DIR && source $VENV_DIR/bin/activate && celery -A autotest_server.celery worker --loglevel=info"
end tell
EOF

# 5. Flask 서버 실행
echo "Flask 서버를 시작합니다."
python3 autotest_server.py