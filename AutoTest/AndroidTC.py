from appium import webdriver
from videoCompare import videoComapre
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import AppiumOptions
from appium.webdriver.common.touch_action import TouchAction

import time
import subprocess
import os
import inspect
from pathlib import Path
import shutil


class AndroidTC:
    def __init__(self, tc, device,account,version,folder,subTC,result_path):
        print("Init AndroidTC")
        self.driver = None
        self.test_seting(tc, device,account, version, folder,subTC,result_path)
        self.current_folder = os.path.dirname(__file__)
        
    def __del__(self):
        if self.driver:
            try:
                self.driver.quit()
            finally:
                self.driver = None  # 드라이버 객체 초기화
    def test_seting(self, tc,  device,account ,version,folder,subTC,result_path):
        self.tc = tc
        self.account = account
        self.version = version
        self.folder = folder
        self.capabilities = {
            "platformName": "Android",
            "automationName": "uiautomator2",
            "deviceName": "udid",
            "udid": device
        }
        self.subTC = subTC
        self.result_path=result_path

    def _initialize_appium(self):
        appium_options = AppiumOptions()
        appium_options.load_capabilities(self.capabilities)
        appium_server_url = 'http://localhost:4723'
        print(f"_initialize_appium : {self.capabilities}")
        self.driver = webdriver.Remote(appium_server_url, options=appium_options)
        return self.driver

    def compare_files(self, file1, file2, subTC):
        retvalue =True
        lc = videoComapre(file1, file2)
        max_val, img1, img2 = lc.compare_frames()
        threshold = 0.02 if self.tc != 'versioncompare' else 0
        audio_val,audio1,audio2 = lc.compare_audio()
        if max_val.item() > threshold:
            retvalue=False
            img1.save(f'{self.result_path}fail_{self.tc}_TC{subTC}_{self.capabilities.get("udid")}-1.jpg')
            img2.save(f'{self.result_path}fail_{self.tc}_TC{subTC}_{self.capabilities.get("udid")}-2.jpg')
        else:
            img1.save(f'{self.result_path}Success_{self.tc}_TC{subTC}_{self.capabilities.get("udid")}.jpg')

        
        if audio_val<0.99 and audio_val!=0 :
            shutil.move(audio1, f'{self.result_path}fail_{self.tc}_TC{subTC}_{self.capabilities.get("udid")}-1.wav')
            shutil.move(audio2, f'{self.result_path}fail_{self.tc}_TC{subTC}_{self.capabilities.get("udid")}-2.wav')
            retvalue= False
        else: 
            shutil.move(audio1, f'{self.result_path}Success_{self.tc}_TC{subTC}_{self.capabilities.get("udid")}.wav')
            os.remove(audio2)
        return retvalue

    def find_button(self,driver, appium_type, locator,maxcount=60):
        count = 0
        while count < maxcount:
            try:
                if appium_type == 'xpath':
                    return driver.find_element(by=AppiumBy.XPATH, value=locator)
                elif appium_type == 'ID':
                    return driver.find_element(by=AppiumBy.ID, value=locator)
                else:
                    return driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=locator)
            except:
                try:
                    if locator == f"new UiSelector().text(\"{self.account}\")":
                        el = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                                      value="new UiSelector().text(\"minji.kim@kinemaster.com\")")
                        return el
                except:
                    time.sleep(1)
                # 팦업 제거
                try:
                    el = driver.find_element(by=AppiumBy.ID,
                                                  value="com.nexstreaming.app.kinemasterfree:id/collapse_button")
                    if el != None:
                        el.click()
                except:
                    time.sleep(0)
                try:
                    el = driver.find_element(by=AppiumBy.ID,
                                                  value="com.android.permissioncontroller:id/permission_allow_button")
                    if el != None:
                        el.click()
                except:
                    time.sleep(0)
                try:

                    el = driver.find_element(by=AppiumBy.ID,
                                                  value="com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again")
                    if el:
                        el.click()
                        el = driver.find_element(by=AppiumBy.ID,
                                                  value="com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
                        if el:
                            el.click()
                except:
                    time.sleep(0)            
                # save anyway 제거
                try:
                    el = driver.find_element(by=AppiumBy.ID,
                                                  value="com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
                                            
                    # if el != None:
                    #     if el.text=="Save Anyway" :
                    if el:
                        el.click()
                except:
                    time.sleep(0)
                # 스프링 설치 가이드 삭제
                try:
                    el = driver.find_element(by=AppiumBy.ID,
                                                  value="com.nexstreaming.app.kinemasterfree:id/installation_guidance_cancel_button")
                                            
                    # if el != None:
                    #     if el.text=="Save Anyway" :
                    if el:
                        el.click()
                except:
                    time.sleep(0)
                try:
                    el = driver.find_element(by=AppiumBy.ID,
                                                  value="com.nexstreaming.app.kinemasterfree:id/message_title")
                                            
                    if el != None:
                        if el.text=="Free Video Editing App, Spring" :
                            print(f"Spring error")
                            # 특정 좌표 (x=16, y=125)에서 터치 액션 실행
                            touch = driver.TouchAction()
                            touch.tap(x=16, y=125).perform()
                    
                except:
                    time.sleep(0)
                    
                count += 1
        print(f"Failed to find element: {locator}")
        return None

    def apk_install(self, filename='7.4.12.33222.GP.apk',folder='uploads'):
        apkfilename = os.path.join(folder, filename)
        local_path = f'{self.current_folder}/'
        package_name = 'com.nexstreaming.app.kinemasterfree'

        try:
            self.run_adb_command(f"adb -s {self.capabilities.get('udid')} uninstall {package_name}")
            self.run_adb_command(f"adb -s {self.capabilities.get('udid')} install {local_path}{apkfilename}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

    def run_adb_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"ADB Error: {command}{result.stderr.strip()}")
            return None

    def take_screenshot(self, device_path='/sdcard/screenshot.png', local_path='screenshot.png'):
        try:
            subprocess.run(['adb', '-s', self.capabilities.get("udid"), 'shell', 'screencap', device_path], check=True)
            subprocess.run(['adb', '-s', self.capabilities.get("udid"), 'pull', device_path, f"{self.result_path}{local_path}"], check=True)
            subprocess.run(['adb', '-s', self.capabilities.get("udid"), 'shell', 'rm', device_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            stack = inspect.stack()
            print("Call stack:")
            for frame in stack:
                print(f"Function {frame.function} in {frame.filename} at line {frame.lineno}")
        return f"{self.result_path}{local_path}"

    def delete_files_in_remote_folder(self, remote_folder):
        try:
            command = f'adb -s {self.capabilities.get("udid")} shell rm -rf {remote_folder}/*'
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode('utf-8')}")

    def file_download(self, filename,subTC, version=0):
        remote_dir = '/sdcard/Movies/KineMaster/'
        local_dir = f'{self.current_folder}/Test/'
        local_path = local_dir + f'{subTC}_{self.capabilities.get("udid")}_{version}' + '.mp4'
        remote_path = remote_dir + filename + '.mp4'
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        try:
            subprocess.run(['adb', '-s', self.capabilities.get('udid'), 'pull', remote_path, local_path],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            return local_path
        except subprocess.CalledProcessError as e:
            print(f"File download failed: {e.stderr.decode('utf-8')}")
            return None

    def _push_file(self, local_path, remote_path):
        # 원격 디렉토리 경로 추출
        remote_dir = remote_path.rsplit('/', 1)[0]

        # 원격 디렉토리 존재 여부 확인
        check_dir_command = ['adb', '-s', self.capabilities.get("udid"), 'shell','if [ ! -d "{0}" ]; then mkdir -p "{0}"; fi'.format(remote_dir)]

        # 디렉토리 생성 명령어 실행
        subprocess.run(check_dir_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 파일을 원격 장치로 푸시
        push_command = ['adb', '-s', self.capabilities.get("udid"), 'push', local_path, remote_path]
        subprocess.run(push_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def app_install_login(self, account,driver):
        self.driver =driver
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right",60)
        if el:
            el.click()
        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_deny_button",10)
        if el:
            el.click()
        el = self.find_button(driver,'UI',
                              "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(4)")
        el.click()
        el = self.find_button(driver,'UI',
                              "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/cl_loading_button_container\").instance(0)")
        el.click()
        ac_text = f"new UiSelector().text(\"{account}\")"
        el = self.find_button(driver,'UI', ac_text)
        el.click()

    def get_device_name_by_udid(self,udid):
        result = subprocess.run(['adb', '-s', udid, 'shell', 'settings', 'get', 'global', 'device_name'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            device_name = result.stdout.strip()
            return device_name
        else:
            raise Exception(f"Failed to get device name for {udid}: {result.stderr}")




