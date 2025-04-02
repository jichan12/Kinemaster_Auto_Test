from  AndroidTC import AndroidTC
import subprocess
from selenium.common.exceptions import WebDriverException


class AtcScript(AndroidTC):
    def __init__(self, tc, device,account,version,folder,subTC,result_path):
        print("Init AtcKinePush")
        super().__init__( tc, device,account ,version,folder,subTC,result_path)

    def install_script(self, version, filename, localpath, remotepath,driver,folder):
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


    def convert_script(self,):
        # 파일에서 내용을 읽어와 배열로 넣고, exec로 순차 실행
        # 1. 파일 열기 및 읽기
        with open('sc.sc', 'r') as file:
            commands = file.readlines()

        # 2. 각 라인의 코드를 순차적으로 실행
        for command in commands:
            exec(command.strip())

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

        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_allow_button",5)
        if el:
            el.click()
        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_allow_button",5)
        if el:
            el.click()
        el = self.find_button(driver,'xpath', f'//android.widget.FrameLayout[@resource-id="com.nexstreaming.app.kinemasterfree:id/option_panel_default_fragment_export"]/android.widget.ImageView')
        el.click()
        # el = self.find_button(driver,'UI', "new UiSelector().className(\"android.widget.ImageView\").instance(5)")
        # if el:
        #     el.click()
        # else:
        #     el = self.find_button(driver,'UI', "new UiSelector().className(\"android.widget.ImageView\").instance(6)")
        #     el.click()
        
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
        el.click()

        # el = self.find_button(driver, 'ID',"com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again")
        # el.click()
        # el = self.find_button(driver, 'ID', "com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
        # el.click()
        el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again",5)
        if el:
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right")
            if el:
                el.click()

