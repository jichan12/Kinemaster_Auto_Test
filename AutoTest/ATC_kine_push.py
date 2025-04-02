from  AndroidTC import AndroidTC
import subprocess
from selenium.common.exceptions import WebDriverException
import time


class AtcKinePush(AndroidTC):
    def __init__(self, tc, device,account,version,folder,subTC,result_path):
        print("Init AtcKinePush")
        super().__init__( tc, device,account ,version,folder,subTC,result_path)
        # self.capabilities = super().capabilities



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
        print("_create_new_project AtcKinePush")
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


        print("_create_new_project AtcKinePush1")
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

        print("_create_new_project AtcKinePush11")
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
        el = self.find_button(driver,'xpath','//android.view.ViewGroup[@resource-id="com.nexstreaming.app.kinemasterfree:id/option_panel_default_fragment_export"]')
        if el:
            el.click()
        else:
            el = self.find_button(driver,'xpath', '//android.widget.FrameLayout[@resource-id="com.nexstreaming.app.kinemasterfree:id/option_panel_default_fragment_export"]/android.widget.ImageView')
            el.click()
        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
        if el:
            el.click()
        else:
            el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_main_fragment_save")
            if el:
                el.click()

        savecnt =0                               
        el = self.find_button(driver,'xpath', '//android.widget.TextView[@resource-id="com.nexstreaming.app.kinemasterfree:id/save_as_process_fragment_message"]')
        while el:
            el = self.find_button(driver,'xpath', '//android.widget.TextView[@resource-id="com.nexstreaming.app.kinemasterfree:id/save_as_process_fragment_message"]',3)
            savecnt=savecnt+1
            time.sleep(1)
            if savecnt>3000:
                break
        el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again",5)
        if el:
            el.click()
            el = self.find_button(driver,'ID',"com.nexstreaming.app.kinemasterfree:id/app_dialog_button_right",1)
            if el:
                el.click()

