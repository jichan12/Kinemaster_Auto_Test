from atc_mix import AtcMix
from pathlib import Path

class AtcMixRg( AtcMix):
    def __init__(self, tc, device,account,version,folder,subTC,result_path):
        print("Init AtcMixRg")
        super().__init__( tc, device,account ,version,folder,subTC,result_path)
        # self.capabilities = super().capabilities

    def rg_tc_mix(self,driver):
        print(f"rg_tc_mix version: {self.version1},subTC:{self.subTC},{self.driver}")
        file1 = self.install_tc_mix(self.version1, self.subTC,self.driver)
        return file1


    def run(self):
        self.driver = self._initialize_appium()
        try:
            tc_url = 'https://kine.to/template/66cbb3d7c9ed66472fc2903d'
            version1fileName = self.rg_tc_mix(self.driver )

            file1 = self.file_download(version1fileName, self.subTC.split("/")[-1], Path(self.version1).name)
            file2 = f'{self.current_folder}/Test/{self.subTC.split("/")[-1]}.mp4'
            return_val =  self.compare_files(file1, file2, self.subTC.split("/")[-1])
            return return_val
        except Exception as e:
            print(f"예외 발생: {e}")
            self.take_screenshot(f'/sdcard/DCIM/f{self.subTC.split("/")[-1]}.png', f'fail_{self.tc}_{self.subTC.split("/")[-1]}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            #self.driver.quit()
            return False