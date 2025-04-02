from  AndroidTC import AndroidTC
from ATC_kine_push import AtcKinePush
import subprocess
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import time



import traceback

SUCCESS_MAILCOUNT = 12*2
class ATC_Stress(AndroidTC):
    def __init__(self, tc, device,account,version,folder='',subTC='',result_path='',count=0):
        print("Init ATC_Steress")
        self.count = count
        super().__init__( tc, device,account ,version,folder,subTC,result_path)
    
    def Strress_tc(self, version, subbTC,driver,folder):
        self.driver = driver
        
        # if self.count==0:
        #     # self.apk_install(version,folder)
        #     try:
        #         # 앱 활성화
        #         time.sleep(2)
        #         driver.activate_app('com.nexstreaming.app.kinemasterfree')
        #     except WebDriverException as e:
        #         traceback.print_exc()
        #         print(f"앱을 활성화하는 데 실패했습니다: {e}")
        #         return "fail"
        #     time.sleep(10)
        #     self.app_install_login(self.account,driver)
        #     time.sleep(10)
        return self.routin_check(driver)

    
    def routin_check(self,driver):
        self.driver =driver
        return self.impor_project(driver)
        if self.subTC =='aivoice':
            return self.aivocie_check(driver)
        elif self.subTC =='vocal':
            return self.vocal_Separator_check(driver)

    def vocal_Separator_check(self,driver):
        self.driver =driver
        
        driver.activate_app('com.nexstreaming.app.kinemasterfree')
        time.sleep(5)
    #  change server
        try:
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(2)")
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/project_more")
            el.click()
            el = self.find_button(driver,'UI',"new UiSelector().className(\"android.widget.ImageView\").instance(3)")
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/text")
            el.click()
            el = self.find_button(driver,'UI',"new UiSelector().text(\"20250305-Copy\")")
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/project_editor_timeline_view")
            el.click()
  
            el = self.find_button(driver,'UI','new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Vocal Separator"))')
            el.click()  # ✅ 해당 요소가 보이면 클릭
            # el = self.find_button(driver,'UI','//android.widget.TextView[@resource-id="com.nexstreaming.app.kinemasterfree:id/option_menu_landscape_list_item_form_label" and @text="AI Voice"]')
            # el.click()
            
            # el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/ai_voice_item_thumbnail\").instance(0)")
            # el.click()
            # el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/ai_voice_item_transcoding_button\")")
            # el.click()
            # # el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/text")
            # el = self.find_button(driver,'xpath', '//android.widget.TextView[@resource-id="com.nexstreaming.app.kinemasterfree:id/aimodel_process_fragment_title"]')
            savecnt=0
            while el:
                el = self.find_button(driver,'xpath', '//android.widget.TextView[@resource-id="com.nexstreaming.app.kinemasterfree:id/aimodel_process_fragment_title"]',3)
                savecnt=savecnt+1
                time.sleep(1)
                if savecnt>3000:
                    break
            # el.click()
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(3)")
            el.click()
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(5)")
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
            if el:
                el.click()
            else:
                el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
                if el:
                    el.click()
            while el:
                el = self.find_button(driver,'xpath', '//android.widget.TextView[@resource-id="com.nexstreaming.app.kinemasterfree:id/save_as_process_fragment_message"]',3)
                savecnt=savecnt+1
                time.sleep(1)
                if savecnt>3000:
                    break
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/icon")
            el.click()
            driver.execute_script('mobile: pressKey', {"keycode": 4})
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/project_more\").instance(0)")
            el.click()
            el = self.find_button(driver,'UI',"new UiSelector().className(\"android.widget.ImageView\").instance(4)")
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
            el.click()
            retvalue = True     
        except Exception as e:
            print(f"예외 발생: {e}")
            traceback.print_exc()
            self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail1_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            retvalue = False            
           
        return retvalue
    
    def aivocie_check(self,driver):
        self.driver =driver
        
        driver.activate_app('com.nexstreaming.app.kinemasterfree')
        time.sleep(5)
    #  change server
        try:
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(2)")
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/project_more")
            el.click()
            el = self.find_button(driver,'UI',"new UiSelector().className(\"android.widget.ImageView\").instance(3)")
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/text")
            el.click()
            el = self.find_button(driver,'UI',"new UiSelector().text(\"20250305-Copy\")")
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/project_editor_timeline_view")
            el.click()
  
            el = self.find_button(driver,'UI','new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("AI Voice"))')
            el.click()  # ✅ 해당 요소가 보이면 클릭
            # el = self.find_button(driver,'UI','//android.widget.TextView[@resource-id="com.nexstreaming.app.kinemasterfree:id/option_menu_landscape_list_item_form_label" and @text="AI Voice"]')
            # el.click()
            
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/ai_voice_item_thumbnail\").instance(0)")
            el.click()
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/ai_voice_item_transcoding_button\")")
            el.click()
            # el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/text")
            # el = self.find_button(driver,'xpath', '//android.widget.TextView[@resource-id="com.nexstreaming.app.kinemasterfree:id/aimodel_process_fragment_title"]')
            savecnt=0
            while el:
                el = self.find_button(driver,'xpath', '//android.widget.TextView[@resource-id="com.nexstreaming.app.kinemasterfree:id/aimodel_process_fragment_title"]',3)
                savecnt=savecnt+1
                time.sleep(1)
                if savecnt>3000:
                    break
            # el.click()
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(3)")
            el.click()
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(5)")
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
            if el:
                el.click()
            else:
                el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
                if el:
                    el.click()
            while el:
                el = self.find_button(driver,'xpath', '//android.widget.TextView[@resource-id="com.nexstreaming.app.kinemasterfree:id/save_as_process_fragment_message"]',3)
                savecnt=savecnt+1
                time.sleep(1)
                if savecnt>3000:
                    break
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/icon")
            el.click()
            driver.execute_script('mobile: pressKey', {"keycode": 4})
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/project_more\").instance(0)")
            el.click()
            el = self.find_button(driver,'UI',"new UiSelector().className(\"android.widget.ImageView\").instance(4)")
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
            el.click()
            retvalue = True     
        except Exception as e:
            print(f"예외 발생: {e}")
            traceback.print_exc()
            self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail1_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            retvalue = False            
           
        return retvalue
    
    def impor_project(self,driver):
        self.driver =driver
    
        el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/new_project_button_imageview")
        el.click()
        el = self.find_button(driver,'UI',"new UiSelector().text(\"Import\")")
        el.click()
        el = self.find_button(driver,'UI',"new UiSelector().text(\"스위스 캠핑카 5.kine\")")
        el.click()
        time.sleep(5)
        el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(0)",60)
        el.click()
        return True

    def run(self):
        self.driver = self._initialize_appium()
        
        try:
            # local_path = f'{self.current_folder}/Test/'
            # local_file = f'{self.subTC}'
            # remote_path = '/sdcard/Download/AutoTest/'
            return_val = self.Strress_tc( self.version[0],self.subTC,self.driver,self.folder)
            return return_val
        except Exception as e:
            print(f"예외 발생: {e}")
            self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail2_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            return False

