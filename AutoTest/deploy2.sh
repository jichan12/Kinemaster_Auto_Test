#!/bin/bash
# MacOS용 배포 스크립트

#####
#!/bin/bash
# Android SDK 및 Appium 설정 스크립트




#######


# 1. Homebrew 설치 (필요 시)
if ! command -v brew &> /dev/null
then
    echo "Homebrew가 설치되어 있지 않습니다. Homebrew를 설치합니다."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew가 이미 설치되어 있습니다."
fi

# 2. Node.js 및 npm 설치 (필요 시)
if ! command -v node &> /dev/null
then
    echo "Node.js가 설치되어 있지 않습니다. Node.js와 npm을 설치합니다."
    brew install node
else
    echo "Node.js 및 npm이 이미 설치되어 있습니다."
fi


# 3. FFmpeg 설치 및 경로 설정
if ! command -v ffmpeg &> /dev/null
then
    echo "FFmpeg가 설치되어 있지 않습니다. FFmpeg를 설치합니다."
    brew install ffmpeg
else
    echo "FFmpeg가 이미 설치되어 있습니다."
fi

# FFmpeg 경로 추가
FFMPEG_PATH=$(brew --prefix ffmpeg)/bin
if ! grep -q "$FFMPEG_PATH" <<< "$PATH"; then
    echo "export PATH=\$PATH:$FFMPEG_PATH" >> ~/.zshrc
    echo "export PATH=\$PATH:$FFMPEG_PATH" >> ~/.bash_profile
    source ~/.zshrc
    source ~/.bash_profile
    echo "FFmpeg 경로가 PATH에 추가되었습니다."
else
    echo "FFmpeg 경로가 이미 PATH에 추가되어 있습니다."
fi

# 2. Android SDK 설치
if ! command -v sdkmanager &> /dev/null
then
    echo "Android SDK가 설치되어 있지 않습니다. Android SDK를 설치합니다."
    brew install --cask android-sdk
else
    echo "Android SDK가 이미 설치되어 있습니다."
fi

# 3. Android SDK 환경 변수 설정
ANDROID_HOME="$HOME/Library/Android/sdk"
echo "Setting up Android SDK environment variables..."

if grep -q "export ANDROID_HOME" ~/.zshrc; then
    echo "ANDROID_HOME already set in ~/.zshrc"
else
    echo "export ANDROID_HOME=$ANDROID_HOME" >> ~/.zshrc
    echo 'export PATH=$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$PATH' >> ~/.zshrc
    source ~/.zshrc
fi

if grep -q "export ANDROID_HOME" ~/.bash_profile; then
    echo "ANDROID_HOME already set in ~/.bash_profile"
else
    echo "export ANDROID_HOME=$ANDROID_HOME" >> ~/.bash_profile
    echo 'export PATH=$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$PATH' >> ~/.bash_profile
    source ~/.bash_profile
fi

# SDK 경로 확인
if [ ! -d "$ANDROID_HOME" ]; then
    echo "Error: Android SDK path '$ANDROID_HOME' does not exist."
    exit 1
else
    echo "Android SDK path confirmed: $ANDROID_HOME"
fi

# adb devices 명령어로 장치 확인
echo "Checking connected Android devices..."
adb devices

# 2. pyenv 설치 및 설정
if ! command -v pyenv &> /dev/null
then
    echo "pyenv가 설치되어 있지 않습니다. pyenv를 설치합니다."
    brew install pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
    source ~/.zshrc
else
    echo "pyenv가 이미 설치되어 있습니다."
fi

# 3. Python 설치 (pyenv 사용)
PYTHON_VERSION=3.8.10  # 필요에 따라 Python 버전을 변경하세요

if ! pyenv versions | grep -q "$PYTHON_VERSION"
then
    echo "Python $PYTHON_VERSION 버전을 설치합니다."
    pyenv install $PYTHON_VERSION
else
    echo "Python $PYTHON_VERSION 버전이 이미 설치되어 있습니다."
fi

pyenv global $PYTHON_VERSION

# 4. 가상 환경 설정
PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "가상 환경을 생성합니다."
    python3 -m venv "$VENV_DIR"
else
    echo "가상 환경이 이미 존재합니다."
fi

# 가상 환경 활성화
source "$VENV_DIR/bin/activate"

# 5. 패키지 설치
if [ -f "requirements.txt" ]; then
    echo "필요한 패키지를 설치합니다."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "requirements.txt 파일이 없습니다. 패키지 설치를 건너뜁니다."
fi

# 6. Redis 설치 및 실행 (옵션)
if ! command -v redis-server &> /dev/null
then
    echo "Redis가 설치되어 있지 않습니다. Redis를 설치합니다."
    brew install redis
fi

# Redis 서버 시작
if ! pgrep redis-server > /dev/null 2>&1; then
    echo "Redis 서버를 시작합니다."
    redis-server --daemonize yes
else
    echo "Redis 서버가 이미 실행 중입니다."
fi

# 7. Appium 설치 및 실행 (옵션)
if ! command -v appium &> /dev/null
then
    echo "Appium이 설치되어 있지 않습니다. Appium을 설치합니다."
    npm install -g appium
else
    echo "Appium이 이미 설치되어 있습니다."
fi

# Appium 서버 시작 (새 터미널 창에서 실행)
osascript <<EOF
tell application "Terminal"
    do script "appium"
end tell
EOF

# 8. Celery 워커 실행 (새 터미널 창에서 실행)
osascript <<EOF
tell application "Terminal"
    do script "cd $PROJECT_DIR && source $VENV_DIR/bin/activate && celery -A autotest_server.celery worker --loglevel=info"
end tell
EOF

# 9. Flask 서버 실행
echo "Flask 서버를 시작합니다."
python autotest_server.py


# Check if uiautomator2 driver is installed
echo "Checking installed Appium drivers..."
INSTALLED_DRIVERS=$(appium driver list --installed)

if [[ ! "$INSTALLED_DRIVERS" == *"uiautomator2"* ]]; then
    echo "uiautomator2 driver not found. Installing..."
    appium driver install uiautomator2
else
    echo "uiautomator2 driver is already installed."
fi

# Restart Appium server
echo "Restarting Appium server..."
pkill -f appium
appium &

echo "Appium server restarted."
