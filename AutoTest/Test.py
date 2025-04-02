from Android_Test import AndroidTest

devices = ["9C241FFBA001L8"]#15151FDD4001GT"]# , "1A051FDF600BG0"]
devices = ["ㅍ"]
devices = ["10.10.2.79:5555"]#15151FDD4001GT"]# , "9C241FFBA001L8"]
devices = ["15151FDD4001GT"]#15151FDD4001GT"]# , "9C241FFBA001L8"]

platform = ["Android", "iOS"]
TCS = ["versioncompare"]
TCS = ["server"]
TCS = ["stress"]
TCS = ["regression"]
TCS = ["server"]
# subTC = ["Test1"]
# TCS = ["regression_kine"]
# subTC = ["Test1"]
# TCS = ["regression"]

subTC = ['kine,KM-11790.kine']
subTC = ['jira,key=KM-11790']
subTC = ['server,kr']
subTC = ['stress,vocal']
subTC = ['mix,https://kine.to/template/66e03a361098d00c48cf8933','kine,20240726.kine']
subTC = ['server,kr']
FOLDER_PATH = 'uploads'
failcount = 0
Successcount = 0
onetineTest_cnt = 0
version1='uploads/7.5.1.33830.GP.apk'
version2='uploads/7.5.16.34132.GP.apk'
# version=['7.5.1.33830.GP.apk','7.5.16.34132.GP.apk','7.4.17.33410.GP.apk']
# version=['7.5.16.34132.GP.apk','7.5.16.34132.GP1.apk']
versions=['7.6.0.34438.GP.apk']#,'7.6.0.34438.GP.apk']
    # 'uploads/7.3.4.31612.GP.apk'
# __init__(self, tc, device='', account="yk.moon@kinemaster.com", version1='7.4.12.33222.GP.apk',
#          version2='7.4.17.33410.GP.apk'):
#
# def test_seting(self, tc, account="", device='9C241FFBA001L8', version1='7.4.12.33222.GP.apk',
#                 version2='7.4.17.33410.GP.apk'):

# test = AndroidTest(action, account="yk.moon@kinemaster.com", version1=file_path1, version2=file_path2)

# file1 = './Test/7.5.1.33830.GP.apk_15151FDD4001GT_0.mp4'
# file2 = './Test/7.5.16.34132.GP.apk_15151FDD4001GT_0.mp4'


# lc = videoComapre(file1, file2)
# print("compare_files1")
# max_val, img1, img2 = lc.compare_audio()


accountid="swear01.kine@gmail.com"
accountid="yk.moon@kinemaster.com"



import time

start = time.perf_counter()
time.sleep(1)  # 1ms 대기
end = time.perf_counter()
print(f"실제 대기 시간: {end - start:.6f} 초")

count =0
retvalue = True
for tc in TCS:
    test = AndroidTest(tc, account=accountid, version=versions, folder=FOLDER_PATH)
    for count in subTC:
    
        if onetineTest_cnt == 0 and tc == "downandup":
            onetineTest_cnt = 1
        elif onetineTest_cnt == 1 and tc == "downandup":
            continue

        for device in devices:
            test.set_device( device)
            test.set_subTC(count)
            # serverd의 경우
            for c in range(100):
                try:
                    retvalue = test.perform_actions(c)
                    # retvalue = test.perform_actions()
                except Exception as e:
                    print(f"예외 발생: {e}")

                if not retvalue:
                    failcount += 1
                else:
                    Successcount += 1
                print(f"Total :{Successcount + failcount} Success : {Successcount} , Fail : {failcount}")

print(f"Total :{Successcount + failcount} Success : {Successcount} , Fail : {failcount}")
