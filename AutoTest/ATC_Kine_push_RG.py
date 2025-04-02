from ATC_kine_push import AtcKinePush
import os

class AtcKinePushRg(AtcKinePush):
    def __init__(self, tc, device,account,version,folder,subTC,result_path):
        super().__init__( tc, device,account ,version,folder,subTC,result_path)
        # self.capabilities = super().capabilities

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

            filename = os.path.splitext(filename_with_extension)[0]
            file2 = f'{self.current_folder}/Test/{filename}.mp4'
            return self.compare_files(file1, file2, self.subTC)
        except Exception as e:
            print(f"예외 발생: {e}")
            self.take_screenshot(f"/sdcard/DCIM/f{self.subTC}.png", f'fail_{self.tc}_{self.subTC}_{self.capabilities.get("udid")}.jpg')
            print("Regression test failed")
            return False