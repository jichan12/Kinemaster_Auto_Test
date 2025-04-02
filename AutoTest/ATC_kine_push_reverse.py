from  AndroidTC import AndroidTC
import subprocess
from selenium.common.exceptions import WebDriverException
import os

class AtcKinePushReverse(AndroidTC):
    def __init__(self, tc, device,account,version,folder,subTC,result_path):
        print("Init AtcKinePush")
        super().__init__( tc, device,account ,version,folder,subTC,result_path)


    def install_tc(self, version, filename, localpath, remotepath,driver,folder):
        self.driver = driver
        self.apk_install(version,folder)
        try:
            self._push_file(localpath + filename, remotepath + filename)
        except subprocess.CalledProcessError as e:
            print(f"File upload failed: {e.stderr.decode('utf-8')}")
            return "fail"

        try:
            # 앱 활성화
            driver.activate_app('com.nexstreaming.app.kinemasterfree')
        except WebDriverException as e:
            print(f"앱을 활성화하는 데 실패했습니다: {e}")
            return "fail"

        self.app_install_login(self.account,driver)
        self._create_new_project(driver)

        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name")
        el.click()
        return el.text



    def _create_new_project(self,driver):
        self.driver = driver
        el = self.find_button(driver,'UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/navigation_bar_item_icon_view\").instance(2)")
        el.click()
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/new_project_button_imageview")
        el.click()

        el = self.find_button(driver,'UI', "new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(1)")
        el.click()
        
        el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again",5)
        if el:
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
            if el:
                el.click()


        el = self.find_button(driver,'UI',"new UiSelector().description(\"Show roots\")")
        if el:
            el.click()
        udid = self.capabilities.get("udid")
        deviceName= self.get_device_name_by_udid(udid)
        device_value =  f'//android.widget.TextView[@resource-id=\"android:id/title\" and @text=\"{deviceName}\"]'
        el = self.find_button(driver,'xpath',device_value)
        el.click()

        el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.google.android.documentsui:id/sub_menu_list\")")
        if not el:
            el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.google.android.documentsui:id/sub_menu_grid\")")
            if el:
                el.click()

        el = self.find_button(driver,'UI',"new UiSelector().text(\"Download\")")
        el.click()

        el = self.find_button(driver,'UI',"new UiSelector().text(\"AutoTest\")")
        el.click()


        tc_string = f'//android.widget.TextView[@resource-id=\"android:id/title\" and @text=\"{self.subTC}\"]'
        el = self.find_button(driver,'xpath', tc_string)
        if el:
            el.click()

        #권한 획득
        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_allow_button",5)
        if el:
            el.click()
        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_allow_button",5)
        if el:
            el.click()

        #비디오  클립 선택
        # 
        #  
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/project_editor_timeline_view")
        el.click()
        el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(0)")
        el.click()
        el = self.find_button(driver,'UI',"new UiSelector().text(\"Duplicate\")")
        el.click()
        el = self.find_button(driver,'UI',"new UiSelector().text(\"Reverse\")")
        el.click()
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/project_editor_timeline_view")
        el.click()
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/project_editor_timeline_view")
        el.click()
        el = self.find_button(driver,'UI',"new UiSelector().resourceId(\"com.nexstreaming.app.kinemasterfree:id/icon\").instance(3)")
        el.click()


        # 


        el = self.find_button(driver,'xpath', f'//android.widget.FrameLayout[@resource-id="com.nexstreaming.app.kinemasterfree:id/option_panel_default_fragment_export"]/android.widget.ImageView')
        el.click()
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
        el.click()

        el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again",5)
        if el:
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
            if el:
                el.click()


    def run(self):
        self.driver = self._initialize_appium()
        try:
            local_path = f'{self.current_folder}/Test/'
            local_file = f'{self.subTC}'
            remote_path = '/sdcard/Download/AutoTest/'
            testvideofileName1 = self.install_tc(self.version, local_file, local_path, remote_path,self.driver,self.folder)

            self.delete_files_in_remote_folder(remote_path)

            file1 = self.file_download(testvideofileName1, self.subTC)
            filename_with_extension = os.path.basename(self.subTC)

            return self.compare_files(file1, file1, self.subTC)
        except Exception as e:
            print(f"예외 발생: {e}")
            self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
            print("Regression test failed")
            return False