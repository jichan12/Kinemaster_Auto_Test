from  AndroidTC import AndroidTC
from ATC_kine_push import AtcKinePush
import subprocess
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import time

import json
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from email.mime.image import MIMEImage

import traceback

SUCCESS_MAILCOUNT = 12*2
class ATC_Server(AndroidTC):
    def __init__(self, tc, device,account,version,folder='',subTC='',result_path='',count=0):
        print("Init ATC_Server")
        self.count = count
        
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
        
            self.mail_pw = config["mail_pw"]
            self.mail_id = config["mail_id"]
            self.mail_count = config["mail_count"]
            self.mail_recv = config["mail_recv"]
            self.server_timeout = config["server_timeout"]
            self.server_region = config["server_region"]
            
            
            
        except Exception as e:
            print(f"예외 발생: {e}")
        self.failed_regions = self.load_failed_regions()
        super().__init__( tc, device,account ,version,folder,subTC,result_path)
    
    def load_failed_regions(self):
        """JSON 파일에서 실패한 지역 및 서버 타입 데이터 불러오기"""
        try:
            with open("failed_regions.json", "r") as file:
                return json.load(file)
        except Exception as e:
            return {}  # 파일이 없으면 빈 딕셔너리 반환

    def save_failed_regions(self):
        """실패한 지역 및 서버 타입 데이터를 JSON 파일에 저장"""
        with open("failed_regions.json", "w") as file:
            json.dump(self.failed_regions, file)

    def server_check_tc(self, version, subbTC,driver,folder):
        self.driver = driver
        if self.count % (self.mail_count*5) ==self.mail_count*5-1:

            self.run_adb_command(f"adb -s {self.capabilities.get('udid')} reboot")
            self.run_adb_command(f"adb -s {self.capabilities.get('udid')} wait-for-device")
            # 부팅 후 안정적인 상태가 될 때까지 추가 대기
            time.sleep(60)
        
        if self.count==0:
            self.apk_install(version,folder)
            try:
                # 앱 활성화
                time.sleep(2)
                driver.activate_app('com.nexstreaming.app.kinemasterfree')
            except WebDriverException as e:
                traceback.print_exc()
                print(f"앱을 활성화하는 데 실패했습니다: {e}")
                return "fail"
            time.sleep(10)
            self.app_install_login(self.account,driver)
            time.sleep(10)
        return self.sever_check(driver)

    def send_email_with_embedded_image(self,to_email, subject, body, image_path):
        sender_email = self.mail_id
        sender_password = self.mail_pw

        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = ", ".join(to_email)
        msg["Subject"] = subject

        # HTML 본문 (CID 참조)
        html_body = f"""
        <html>
        <body>
            <h2>🚨 테스트 알림</h2>
            <p><b>테스트 발생:</b> {body}</p>
            <p><b>시간:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <h3>📷 캡처된 스크린샷:</h3>
            <img src="cid:screenshot" width="500">
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))

        # CID 이미지 추가
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                img = MIMEImage(img_file.read())
                img.add_header("Content-ID", "<screenshot>")
                msg.attach(img)

        # SMTP 서버에 연결하여 이메일 전송
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.quit()
            print(f"✅ 이메일이 {to_email}로 성공적으로 전송되었습니다.")
        except Exception as e:
            print(f"❌ 이메일 전송 중 오류 발생: {e}")
            traceback.print_exc()

    def chaneg_region(self,driver,region):
        self.driver =driver
        driver.activate_app('com.surfshark.vpnclient.android')
        
        el = self.find_button(driver,'UI','new UiSelector().className("android.widget.ImageView")')
        if el:
            el.click()
        el = self.find_button(driver,'xpath','//android.widget.TextView[@text="Favourites"]')
        if el==None:
            driver.back()


        el = self.find_button(driver,'UI',f'new UiSelector().text(\"{region}\")')
        el.click()

        el = self.find_button(driver,'UI',"new UiSelector().className(\"android.widget.Button\").instance(0)")
        if el:
            return True
        else:
            return False
    def error_screenshot(self, el, servertype, region):
        """
        - 성공이면 True 반환
        - 실패하면 기록 유지 후 이메일 발송
        - 이전 실행에서 같은 리전과 서버 타입이 실패였고, 이번에도 실패하면 이메일 발송
        - 성공하면 해당 실패 기록 삭제
        - self.count % self.mail_count == 0 조건일 경우 이메일 발송
        """
        current_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        success = bool(el)  # True면 성공, False면 실패
        status = "Success" if success else "Fail"

        # 저장할 스크린샷 파일 경로
        local_screenshot_path = f"{status}_{servertype}_{region}_{current_time_str}.jpg"

        # ✅ 설정 파일에서 메일 수신자 정보 가져오기
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
            self.mail_recv = config["mail_recv"]
        except Exception as e:
            print(f"예외 발생: {e}")
            traceback.print_exc()
            self.mail_recv = "default@example.com"  # 예외 발생 시 기본 이메일 설정

        key = f"{region}_{servertype}"  # ✅ 지역 + 서버 타입 조합 키

        # ✅ 이메일을 보내야 하는 경우:
        # 1️⃣ 이전 실행에서 같은 리전과 서버 타입이 실패했고, 이번에도 실패한 경우
        # 2️⃣ self.count % self.mail_count == 0 (1000번 실행마다 이메일 발송)
        send_email = False

        if key in self.failed_regions and not success:
            send_email = True  # ✅ 이전에 실패했고 이번에도 실패 → 이메일 발송
        elif self.count % self.mail_count == 0:
            send_email = True  # ✅ 1000번 실행마다 이메일 발송

        # ✅ 스크린샷 저장 및 이메일 발송
        if send_email:
            try:
                screenshot = self.take_screenshot(
                    f"/sdcard/DCIM/f{current_time_str}.png",
                    local_screenshot_path
                )
                self.send_email_with_embedded_image(
                    to_email=self.mail_recv,
                    subject=f"[ALERT] Test {status}: {region}",
                    body=f"테스트 {status} 발생:  {region} \n서버 타입: {servertype}",
                    image_path=screenshot
                )
                print(f"🚨 실패 알림 이메일 전송 완료: {screenshot}")
            except Exception as e:
                traceback.print_exc()
                print(f"❌ 이메일 전송 실패: {e}")

        # ✅ 실패한 경우 기록 유지
        if not success:
            self.failed_regions[key] = True  # 실패 기록 유지
            self.save_failed_regions()
            return False
        else:
            # ✅ 성공하면 해당 실패 기록 삭제
            if key in self.failed_regions:
                del self.failed_regions[key]
                self.save_failed_regions()
            return True
        

    def sever_check(self,driver):
        self.driver =driver
        retvalue = True


        for region in self.server_region:
            if self.chaneg_region(driver,region):
                try:
                    driver.terminate_app('com.nexstreaming.app.kinemasterfree')
                except WebDriverException as e:
                    traceback.print_exc()
                    driver.terminate_app('com.nexstreaming.app.kinemasterfree')
                driver.activate_app('com.nexstreaming.app.kinemasterfree')
                time.sleep(5)
            #  change server
                try:
                    el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(0)",self.server_timeout)
                    el.click()
                    el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/iv_thumbnail\").instance(4)",self.server_timeout)
                    if el == None:
                        self.error_screenshot(False, 'mix',region)
                        retvalue = False
                    else:
                        self.error_screenshot(True, 'mix',region)
                        el.click()  # 성공한 경우 다음 스텝 진행
                        el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(0)",self.server_timeout)
                        el.click()

                    el = self.find_button(driver,'UI','new UiSelector().text("Asset Store")',self.server_timeout)
                    el.click()  # 성공한 경우 다음 스텝 진행
                    
                    el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/asset_store_image_h_list_asset_item_form_thumbnail\").instance(0)",self.server_timeout)
                    if el == None:
                        self.error_screenshot(False, 'asset',region)
                        retvalue = False
                    else:
                        self.error_screenshot(True, 'asset',region)
                        el.click()  # 성공한 경우 다음 스텝 진행
             
                    el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(0)",self.server_timeout)
                    el.click()
                    
                except Exception as e:
                    print(f"예외 발생: {e}")
                    traceback.print_exc()
                    self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail1_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
                    print("Version compare test failed")
                    retvalue = False
                    continue
            else:
                self.error_screenshot(False, 'vpn',region)
        return retvalue


    def run(self):
        self.driver = self._initialize_appium()
        
        try:
            # local_path = f'{self.current_folder}/Test/'
            # local_file = f'{self.subTC}'
            # remote_path = '/sdcard/Download/AutoTest/'
            return_val = self.server_check_tc( self.version[0],self.subTC,self.driver,self.folder)
            return return_val
        except Exception as e:
            print(f"예외 발생: {e}")
            self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail2_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            return False

