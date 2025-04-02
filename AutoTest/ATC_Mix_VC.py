from atc_mix import AtcMix
from pathlib import Path
import os

class AtcMixVc(AtcMix):
    def __init__(self, tc, device,account,version,folder,subTC,result_path):
        print("Init AtcMixVc")
        super().__init__( tc, device,account ,version,folder,subTC,result_path)
        
    def version_compare_tc_mix(self,driver):
        files = []
        for version in self.version:
            files.append(self.install_tc_mix(version,self.subTC,driver,self.folder))
        return files
    

    def run(self):
        self.driver = self._initialize_appium()
        try:
            versionfileNames = self.version_compare_tc_mix(self.driver)
            #self.driver.quit()

            files = []
            return_val = True
            for i, versionfileName in enumerate(versionfileNames): 
                files.append(self.file_download(versionfileName,  self.subTC.split("/")[-1], Path(self.version[i]).name))
            for i in range(len(files) - 1):  # 마지막 요소는 비교할 것이 없음
                str1 = files[i]
                str2 = files[i + 1]
                retvalue = self.compare_files(files[i],files[i+1], self.subTC.split("/")[-1])
                if retvalue==False:
                    return_val =False 
                os.remove(files[i])
            os.remove(files[len(files)-1])

        
        except Exception as e:
            print(f"예외 발생: {e}")
            self.take_screenshot(f'/sdcard/DCIM/f{self.subTC.split("/")[-1]}.png', f'fail_{self.tc}_{self.subTC.split("/")[-1]}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            return False