
from datetime import datetime
from adbutils import device
import os

# TestClass
from ATC_kine_push_VC import AtcKinePushVc
from ATC_Kine_push_RG import AtcKinePushRg
from ATC_kine_push_reverse import AtcKinePushReverse
from ATC_Mix_VC import AtcMixVc
from ATC_Mix_RG import AtcMixRg
from ATC_Server import ATC_Server
from ATC_Stress import ATC_Stress


from videoCompare import videoComapre


class AndroidTest:
    def __init__(self, tc,account ,version,folder ,device=""):
        print(f"AndroidTest Init")
        self.device = device
        self.tc = tc
        self.version = version
        self.folder = folder
        current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.current_folder = os.path.dirname(__file__)
        self.result_folder = f"{tc}_{current_time}"
        self.result_path = f"{self.current_folder}/Result/{self.result_folder}/"
        self.account = account
        result_prepath = f"{self.current_folder}/Result/"
        if not os.path.exists(result_prepath):
            os.mkdir(result_prepath)
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)

    def set_subTC(self,subTC):
        test_type, test_case = subTC.split(',')
        self.subTC = test_case
        self.test_type = test_type

    def set_device(self, device):
        self.device = device


    def perform_actions(self,count=False):
        print(f"perform_actions  {self.tc} {self.test_type} {self.device}, {self.account},{self.version},{self.folder},{self.subTC},{self.result_path}")
        if self.test_type == 'kine':
            if self.tc == 'versioncompare':
                test= AtcKinePushVc("versioncompare_kine",self.device, self.account,self.version,self.folder,self.subTC,self.result_path)
                return test.run()
            elif self.tc == 'regression':
                test = AtcKinePushRg("regression_kine",self.device, self.account, self.version, self.folder, self.subTC,self.result_path)
                return test.run()
            elif self.tc == 'reverse':
                test = AtcKinePushReverse("reverse_kine",self.device, self.account, self.version, self.folder, self.subTC,self.result_path)
                return test.run()
            else:
                return "error"
        elif self.test_type == 'mix':
            if self.tc == 'versioncompare':
                test= AtcMixVc("versioncompare_mix",self.device, self.account,self.version,self.folder,self.subTC,self.result_path)
                return test.run()
            elif self.tc == 'regression':
                test = AtcMixRg("regression_mix",self.device, self.account, self.version, self.folder, self.subTC,self.result_path)
                return test.run()
            else:
                return "error"
        elif self.test_type == 'server':
            if self.tc == 'server':
                test= ATC_Server("server",self.device, self.account,self.version,self.folder,self.subTC,self.result_path,count)
                return test.run()
        elif self.test_type == 'stress':
            if self.tc == 'stress':
                test= ATC_Stress("server",self.device, self.account,self.version,self.folder,self.subTC,self.result_path,count)
                return test.run()
        
        else:
            return "error"


