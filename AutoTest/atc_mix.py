from AndroidTC import AndroidTC
import time
from selenium.common.exceptions import WebDriverException

class AtcMix(AndroidTC):
    def __init__(self, tc, device,account,version,folder,subTC,result_path):
        print("Init AtcMix")
        super().__init__( tc, device,account ,version,folder,subTC,result_path)
        # self.capabilities = super().capabilities

    def _create_mix_project(self,driver):
        self.driver =driver
        value = "//android.view.ViewGroup[@resource-id=\"com.nexstreaming.app.kinemasterfree:id/mix_item_download\"]"

        el = self.find_button(driver,'xpath', value)
        if not el:
            value = "com.nexstreaming.app.kinemasterfree:id/tv_download"
            el = self.find_button(driver, 'ID', value)
        el.click()
        # el = self.find_button(driver,'ID',
        #                      "com.nexstreaming.app.kinemasterfree:id/dialog_does_not_show_again_view_does_not_show_again")
        # el.click()
        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_allow_button",5)
        if el:
            el.click()
        el = self.find_button(driver,'ID', "com.android.permissioncontroller:id/permission_allow_button",5)
        if el:
            el.click()


        el = self.find_button(driver,'xpath', '//android.widget.FrameLayout[@resource-id="com.nexstreaming.app.kinemasterfree:id/option_panel_default_fragment_export"]/android.widget.ImageView',30)
        if el:
            print("01111!@#$%")
            el.click()
        else:
            el = self.find_button(driver,'xpath','//android.view.ViewGroup[@resource-id="com.nexstreaming.app.kinemasterfree:id/option_panel_default_fragment_export"]')
            el.click()
        print("!@#$%")
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
            if savecnt>1000:
                break


    def install_tc_mix(self, version, tc_url,driver,folder):

        try:
            self.apk_install(version,folder)

            try:
                # 앱 활성화
                driver.activate_app('com.nexstreaming.app.kinemasterfree')
            except WebDriverException as e:
                print(f"앱을 활성화하는 데 실패했습니다: {e}")
                return "fail"

            self.app_install_login(self.account,driver)
            time.sleep(5)
            driver.terminate_app('com.nexstreaming.app.kinemasterfree')
        except Exception as e:  # 모든 예외를 처리하는 대신 Exception 클래스로 구체적인 정보를 출력
            print(f"Error occurred: {e}")

        self.run_adb_command(
            f'adb -s {self.capabilities.get("udid")} shell am start -a android.intent.action.VIEW -d "{tc_url}"')

        self._create_mix_project(driver)

        el = self.find_button(driver,'ID', "com.nexstreaming.app.kinemasterfree:id/save_as_output_item_form_name")
        el.click()
        return el.text

