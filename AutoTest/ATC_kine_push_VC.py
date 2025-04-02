from ATC_kine_push import AtcKinePush
from pathlib import Path
import os

class AtcKinePushVc(AtcKinePush):
    def __init__(self, tc, device,account,version,folder,subTC,result_path):
        super().__init__( tc, device,account ,version,folder,subTC,result_path)
        print("Init AtcKinePushVc")
    def __del__(self):
        print(f"AtcKinePushVc 객체가 소멸되었습니다.")
    def version_compare_tc(self, loacal_file, loacal_path, remote_path, subTC):
        files = []
        count=0
        for version in self.version:
            files.append(self.install_tc(version, loacal_file, loacal_path, remote_path,self.driver,self.folder))
            print(f'!!!!!!!@AAAA{count}')
            count=count+1
        return files


    def run(self):
        self.driver = self._initialize_appium()
        try:
            local_path = f'{self.current_folder}/Test/'
            local_file = f'{self.subTC}'
            remote_path = '/sdcard/Download/AutoTest/'
            versionfileNames = self.version_compare_tc( local_file, local_path, remote_path, self.subTC)
            print("version_compare_tc")
            self.delete_files_in_remote_folder(remote_path)
            print("delete_files_in_remote_folder")
            files = []
            return_val = True
            for i, versionfileName in enumerate(versionfileNames):  
                files.append(self.file_download(versionfileName, Path(self.version[i]).name))
            for i in range(len(files) - 1):  # 마지막 요소는 비교할 것이 없음
                str1 = files[i]
                str2 = files[i + 1]
                retvalue = self.compare_files(files[i],files[i+1], self.subTC)
                if retvalue==False:
                    return_val =False 
                os.remove(files[i])
            os.remove(files[len(files)-1])
            return return_val
        except Exception as e:
            print(f"예외 발생: {e}")
            self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
            print("Version compare test failed")
            return False