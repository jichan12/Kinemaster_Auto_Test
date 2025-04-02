import logging
import unittest
import allure
from Android_Test import AndroidTest

devices = ["9C241FFBA001L8"]#15151FDD4001GT"]# , "9C241FFBA001L8"]
platform = ["Android", "iOS"]
TCS = ["regression"] #regression versioncompare
subTC = list(range(2, 3))  # "Create"

class MyTestCase(unittest.TestCase):
    @allure.step("Executing test case")
    def test_something(self):
        logging.info("Running perform_actions")
        failcount = 0
        Successcount = 0
        onetineTest_cnt = 0
        version1='uploads/7.4.13.33264.GP.apk'
        version2='uploads/7.4.17.33410.GP.apk'
        # __init__(self, tc, device='', account="yk.moon@kinemaster.com", version1='7.4.12.33222.GP.apk',
        #          version2='7.4.17.33410.GP.apk'):
        #
        # def test_seting(self, tc, account="", device='9C241FFBA001L8', version1='7.4.12.33222.GP.apk',
        #                 version2='7.4.17.33410.GP.apk'):

        # test = AndroidTest(action, account="yk.moon@kinemaster.com", version1=file_path1, version2=file_path2)
        test = AndroidTest("reverse", "device","yk.moon@kinemaster.com", version1, version2)
        for tc in TCS:
            for count in subTC:
                if onetineTest_cnt == 0 and tc == "downandup":
                    onetineTest_cnt = 1
                elif onetineTest_cnt == 1 and tc == "downandup":
                    continue

                for device in devices:
                    logging.info(f"TC : {tc} , Device : {device} subtc : {count}")
                    allure.step(f"TC : {tc} , Device : {device} subtc : {count}")
                    test.test_seting(tc,"yk.moon@kinemaster.com", device,version1)
                    retvalue = test.perform_actions(count)

                    if not retvalue:
                        logging.info(f"Fail TC : {tc} , Device : {device} subtc : {count}")
                        allure.attach(f"Fail TC : {tc} , Device : {device} subtc : {count}", name="Fail", attachment_type=allure.attachment_type.TEXT)
                        failcount += 1
                    else:
                        logging.info(f"Success TC : {tc} , Device : {device} subtc : {count}")
                        allure.attach(f"Success TC : {tc} , Device : {device} subtc : {count}", name="Success", attachment_type=allure.attachment_type.TEXT)
                        Successcount += 1

        print(f"Total :{Successcount + failcount} Success : {Successcount} , Fail : {failcount}")


if __name__ == '__main__':
    unittest.main()
