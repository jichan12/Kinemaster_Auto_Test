AutoTest
설치 순서
스크립트 실행 권한
chomod +x *.sh

섪치및 테스트 서버 실행 스크립트 실행
./deploy.sh

설치가 완료 되면 3개의 콘솔이 실행 1.1 appium(원격 디바이스 제어) 1.2 celery(테스크 관리) 1.3 flask(웹서버)
jira 기능 사용할 경우 jiradown.py에 jira_token및 jira_user 저장
사전 작업및 제약 사항
Test를 하기위한 device연결 1.1. 디바이스 언어 설정 영어 1.2. 테스트 디바이스에 이미 설치된 kinemaster는 삭제 하고 테스트를위한 버전으로 새로 설치됨 1.3. 하나의 작업이 진행중일 경우 다른 테스트는 진행 하지말것
TC 추가 방법
127.0.0.1에 Upload TC kine파일, 결과 파일, 테스트 설명 or
./Test/TestCase.csv 만들기 sample Type,TestCase,Result,Desc kine,KM-12262.kine,20241231.mp4,테스트1 mix,https://kine.to/template/677d1fe1e9c154af117157a0,677d1fe1e9c154af117157a0.mp4,믹스 테스트
apk 추가 방법
맨 아레에 있는 Upload Apk로 테스트가 필요한 apk를 업로드 or
uploads 폴더 안에 apk 저장
테스트 방법
테스트 방법을 선택 1.1 Version Compare: 2개의 apk를 순차적으로 설치 후 경우 각각 저장한 비디오를 비교 1.2 Result Compare : TC 업로드시 업로드된 영상파일과 선택한 버전에서 저장한 비디오를 비교

테스트 진행할 디바이스 선택 (디바이스는 adb로 usb 디버그 연결되어 있는기기 표시됨)

TC 선택 7.1 jira : 입력한 프로젝트에 jql을 기반으로 jira티켓에 포함되어 있는 kine파일로 테스트 진행 7.2 TC : TestCase.csv에 기술된 TC중 선택된 TC만 진행

submit

Test status에서 작업 리스트를 확인가능

Test status 완료된 테스트에 대해서 결과 확인 ./result폴더 안에 이미지로 확인 가능

jira 관련 기능 2.1 jra result compare 기능 추가
