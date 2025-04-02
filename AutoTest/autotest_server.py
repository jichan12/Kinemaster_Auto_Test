#auto_server.py
from flask import Flask, request, redirect, url_for, render_template, session, jsonify, send_from_directory
import os
import subprocess
from celery_app import make_celery
from Android_Test import AndroidTest
from pathlib import Path
import csv
from ATC_kine_push_VC import AtcKinePushVc
from ATC_Kine_push_RG import AtcKinePushRg
from ATC_Mix_VC import AtcMixVc
from ATC_Mix_RG import AtcMixRg
from  jiradown import JiraDownloader
import csv
from pathlib import Path
import pandas as pd  # pandas import 추가

app = Flask(__name__)
app.secret_key = 'supersecretkey'
# RESULT_FOLDER = "static/result"  # ✅ Flask의 static 폴더 내부에 이미지 저장

# 폴더 설정 (파일이 저장된 폴더)
FOLDER_PATH = 'uploads'
os.makedirs(FOLDER_PATH, exist_ok=True)
app.config['FOLDER_PATH'] = FOLDER_PATH

RESULT_FOLDER = 'Result'
os.makedirs(RESULT_FOLDER, exist_ok=True)
app.config['RESULT_FOLDER'] = RESULT_FOLDER

TEST_FOLDER = 'Test'  # Test 폴더 경로 설정
os.makedirs(TEST_FOLDER, exist_ok=True)

TestCaseFilepath = f'./{TEST_FOLDER}/TestCase.csv'
FILED_NAME = ["Type", "TestCase", "Result", "Desc"]

def create_or_update_csv(file_path, fieldnames):
    # 파일이 존재하는지 확인
    file_exists = os.path.exists(file_path)

    # 파일이 없는 경우 생성
    if not file_exists:
        print(f"파일이 존재하지 않으므로 {file_path} 파일을 생성합니다.")
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # 필드명을 추가
        print(f"필드명이 추가되었습니다: {fieldnames}")
    else:
        # 파일이 있는 경우, 필드명이 있는지 확인하고 없으면 추가
        with open(file_path, mode='r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

            if len(rows) == 0 or rows[0] != fieldnames:
                print(f"필드명이 없거나 잘못되어 필드명을 추가합니다.")
                # 파일 내용을 새로 쓰기 위해 파일 포인터를 처음으로 이동
                file.seek(0)
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()  # 필드명을 첫 줄에 추가
                file.writelines([','.join(row) + '\n' for row in rows])  # 기존 내용 유지
                print(f"필드명이 추가되었습니다: {fieldnames}")
            else:
                print(f"필드명이 이미 존재합니다: {fieldnames}")


# Celery 인스턴스 생성
celery = make_celery(app)

@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    task_ids = session.get('task_ids', [])
    if task_id in task_ids:
        task_ids.remove(task_id)
        session['task_ids'] = task_ids
    return redirect(url_for('task_status'))
def get_connected_devices():
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True)
    devices = []
    for line in result.stdout.splitlines():
        if '\tdevice' in line:
            devices.append(line.split('\t')[0])
    return devices

def log_result_csv(file_path, action, subtc_or_file, original_file_name=None, device=None,apkfile_path1=None, file_path2=None, status=None):
    # CSV 파일에 로그를 추가하는 함수
    csv_headers = ['status', 'TC', 'SubTC/DownloadedFile', 'OriginalFileName', 'Device']
    csv_headers += [f"Version{i}" for i in range(1, len(apkfile_path1) + 1)]
    print(f'csv_headers{csv_headers}')
    
    log_data = {
        'status': 'Success' if status else 'Fail',
        'TC': action,
        'SubTC/DownloadedFile': subtc_or_file,
        'OriginalFileName': original_file_name if original_file_name else '',
        'Device': device if device else '',
    }
    for idx, apkfile_path in enumerate(apkfile_path1, start=1):
        log_data[f"Version{idx}"] = Path(apkfile_path).name
    print(f'{log_data}')
    try:
        # 파일이 존재하지 않으면 헤더 추가
        file_exists = Path(file_path).exists()
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow(log_data)
    except Exception as e:
        print(f"Error writing to log file: {e}")


@celery.task(bind=True, name='autotest_server.process_files_and_text')
def process_files_and_text(self, devices, account, action, tcs, file_path, range_type, folder_path):
    current_step = 0
    fail_cnt = 0
    success_cnt = 0
    if range_type == 'server':
        total_steps = tcs * len(devices)
    else:
        total_steps = len(tcs) * len(devices)
    print(f'version{file_path}')    
    test = AndroidTest(action, account=account,version=file_path, folder=folder_path)
    

    # 결과 로그 파일 경로 설정
    result_folder = f"./result/{test.result_folder}"  # test.result_folder를 기반으로
    os.makedirs(result_folder, exist_ok=True)
    log_file_path = os.path.join(result_folder, "result_log.txt")
    
    if range_type == 'server':
         for count in range(tcs):
            print(f"count {count} total{tcs}")
            for device in devices:
                test.set_device(device)
                subTC = ['server,kr']
                test.set_subTC(subtc)
                current_step += 1
                self.update_state(state='PROGRESS', meta={
                    'current': current_step,
                    'total': total_steps,
                    'success_cnt': success_cnt,
                    'fail_cnt': fail_cnt,
                    'status': f'Processing step {current_step}'
                })
                retvalue = test.perform_actions(count)

                log_result_csv(
                file_path=log_file_path,
                action=action,
                subtc_or_file=test.test_type,
                original_file_name=test.subTC,
                device=device,
                apkfile_path1=file_path,
                status=retvalue
                )
                
                # 카운트 업데이트
                if retvalue:
                    success_cnt += 1
                else:
                    fail_cnt += 1

                self.update_state(state='PROGRESS', meta={
                    'current': current_step,
                    'total': total_steps,
                    'success_cnt': success_cnt,
                    'fail_cnt': fail_cnt,
                    'status': f'Processing step {current_step}'
                })

    if range_type == 'tc':
        for subtc in tcs:
            for device in devices:
                test.set_device(device)
                test.set_subTC(subtc)
                current_step += 1
                self.update_state(state='PROGRESS', meta={
                    'current': current_step,
                    'total': total_steps,
                    'success_cnt': success_cnt,
                    'fail_cnt': fail_cnt,
                    'status': f'Processing step {current_step}'
                })
                retvalue = test.perform_actions()

                log_result_csv(
                file_path=log_file_path,
                action=action,
                subtc_or_file=test.test_type,
                original_file_name=test.subTC,
                device=device,
                apkfile_path1=file_path,
                status=retvalue
                )
                
                # 카운트 업데이트
                if retvalue:
                    success_cnt += 1
                else:
                    fail_cnt += 1

                self.update_state(state='PROGRESS', meta={
                    'current': current_step,
                    'total': total_steps,
                    'success_cnt': success_cnt,
                    'fail_cnt': fail_cnt,
                    'status': f'Processing step {current_step}'
                })

    if range_type == 'jira':
        jira_downloader = JiraDownloader('Test')
        tickets = jira_downloader.fetch_tickets(tcs)
        kine_links = jira_downloader.get_kine_links(tickets)
        total_steps = len(kine_links) * len(devices)
    
        for kine in kine_links:
            downloaded_file = jira_downloader.download_file(kine['link'], kine['ticket'], kine['filename'])
            fail_status = not bool(downloaded_file)
            for device in devices:
                test.set_device(device)
                test.set_subTC(f"kine,{downloaded_file}" if not fail_status else "kine,failed")
                current_step += 1
                self.update_state(state='PROGRESS', meta={
                    'current': current_step,
                    'total': total_steps,
                    'success_cnt': success_cnt,
                    'fail_cnt': fail_cnt,
                    'status': f'Processing step {current_step}'
                })

                retvalue = test.perform_actions() if not fail_status else False

      
                log_result_csv(
                    file_path=log_file_path,
                    action=action,
                    subtc_or_file=downloaded_file,
                    original_file_name=kine['filename'],
                    device=device,
                    apkfile_path1=file_path,
                    status=retvalue
                )
                # 카운트 업데이트
                if retvalue:
                    success_cnt += 1
                else:
                    fail_cnt += 1

                self.update_state(state='PROGRESS', meta={
                    'current': current_step,
                    'total': total_steps,
                    'success_cnt': success_cnt,
                    'fail_cnt': fail_cnt,
                    'status': f'Processing step {current_step}'
                })

            if downloaded_file:
                os.remove(f"./Test/{downloaded_file}")

    return {
        'result': f"Total : {total_steps} Success Count: {success_cnt}, "
                  f"Result path = http://127.0.0.1:5000/images/{test.result_folder}"
    }


def read_csv_file(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        csv_content = []
        for row in reader:
            csv_content.append(row)
        return csv_content

@app.route('/')
def index():


    create_or_update_csv(TestCaseFilepath, FILED_NAME)

    apk_files = get_apk_files(FOLDER_PATH)
    devices = get_connected_devices()  # 디바이스 목록 가져오기
    test_cases = []
    with open(TestCaseFilepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            test_cases.append(row)

    return render_template('index.html', apk_files=apk_files, devices=devices, test_cases=test_cases)

@app.route('/upload_apk', methods=['POST'])
def upload_apk():
    if 'file1' not in request.files:
        return "테스트 APK를 선택하세요."
    file1 = request.files['file1']


    # 파일을 새 폴더에 저장
    filepath1 = os.path.join(FOLDER_PATH, file1.filename)
    file1.save(filepath1)

    return redirect(url_for('index'))

@app.route('/upload_TC', methods=['POST'])
def upload_TC():
    print(f"tc0")
    test_type = request.form['test_type']
    if test_type =='mix':
        if 'mixurl' not in request.form or 'tcresultfile' not in request.files or 'tcdesc' not in request.form:
            return "Mix url 선택 하고  TC 설명을 입력 하세요.."
        tcurl = request.form['mixurl']
        tc = os.path.basename(tcurl)

    elif test_type =='kine':
        if 'tckinefile' not in request.files or 'tcresultfile' not in request.files or 'tcdesc' not in request.form:
            return "TC 파일 및 결과 파일을 선택 하고  TC 설명을 입력 하세요.."
        tcfile = request.files['tckinefile']
        tc=os.path.splitext(tcfile.filename)[0]
        if os.path.splitext(tcfile.filename)[1].lower() != '.kine':
            return "Kine 파일을 선택하세요."

    else:
        return "잘못된 테스트 타입입니다."

    tcresultfile= request.files['tcresultfile']
    tcdesc = request.form['tcdesc']
    print(f"tc1")

    # Kine 파일을 새 폴더에 저장
    if test_type == 'kine':
        kine_filepath = os.path.join(TEST_FOLDER , f'{tc}.kine')
        tcfile.save(kine_filepath)
    result_filepath = os.path.join(TEST_FOLDER, f'{tc}.mp4')
    tcresultfile.save(result_filepath)
    print(f"tc2")
    FILED_NAME = ["Type", "TestCase", "Result", "Desc"]

    if test_type =='mix':
        row_data = {'Type': test_type, 'TestCase': tcurl, 'Result': f'{tc}.mp4',"Desc":tcdesc}
    elif test_type == 'kine':
        row_data = {'Type': test_type, 'TestCase': f'{tc}.kine', 'Result': f'{tc}.mp4', "Desc": tcdesc}
    print(f"tc3 {row_data}")
    with open(TestCaseFilepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FILED_NAME)

        # 행 추가
        writer.writerow(row_data)
    print(f"t43")
    # 설명을 텍스트 파일로 저장

    return redirect(url_for('index'))
#메인

@app.route('/upload_files', methods=['POST'])
def upload_files():
    print(f"test0")
    print(f"tc0")
    selected_files = request.form.getlist('files')
    devices = request.form.getlist('devices')
    action = request.form.get('action')
    range_type = request.form.get('range_type')
    tcs = request.form.getlist('range')
    account = request.form['account']
    if range_type=='tc':
        tcs = request.form.getlist('range')

    if range_type=='jira':
        tcs = request.form.get('jira_project')
    if action =='server':
        tcs = request.form.get("server_count", type=int, default=1000)

    num_devices = len(devices)
    print(f"test1")
    if not action:
        return "Please select TC"
    print(f"test2")
    if action == "versioncompare":
        print(f"test3 {range_type}")
        
        if range_type =='tc':
            if len(selected_files) < 2 or num_devices == 0 or not action:
                return f"Please select  2 files, at least one device, and an action. len(selected_files)={len(selected_files)}, num_devices={num_devices}, TC={action}"
            print(f"test4   tcs {tcs} {selected_files[0]} {selected_files[1]}")
            task = process_files_and_text.apply_async(args=[devices, account,action, tcs,selected_files,range_type, FOLDER_PATH])
        elif range_type=='jira':
            if len(selected_files) < 2 or num_devices == 0 or not action:
                return f"Please select 2 files, at least one device, and an action. len(selected_files)={len(selected_files)}, num_devices={num_devices}, TC={action}"
           
            task = process_files_and_text.apply_async(args=[devices, account,action, tcs,selected_files,range_type, FOLDER_PATH])
    elif action == "regression":
        if range_type =='tc':
            if len(selected_files) != 1 or num_devices == 0 or not action:
                return f"Please select exactly 1 files, at least one device, and an action. len(selected_files)={len(selected_files)}, num_devices={num_devices}, TC={action}"
            file_path1 = os.path.join(FOLDER_PATH, selected_files[0])
            task = process_files_and_text.apply_async(args=[devices, account, action, tcs, selected_files,range_type,FOLDER_PATH])
        elif range_type=='jira':
            if len(selected_files) != 1 or num_devices == 0 or not action:
                return f"Please select exactly 1 files, at least one device, and an action. len(selected_files)={len(selected_files)}, num_devices={num_devices}, TC={action}"
            file_path1 = os.path.join(FOLDER_PATH, selected_files[0])
            task = process_files_and_text.apply_async(args=[devices, account, action, tcs, selected_files,range_type,FOLDER_PATH])
    elif action == "server":
        task = process_files_and_text.apply_async(args=[devices, account,action, tcs,selected_files,action, FOLDER_PATH])

    # 작업 ID를 세션에 추가
    task_ids = session.get('task_ids', [])
    task_ids.append(task.id)
    session['task_ids'] = task_ids

    return redirect(url_for('task_status'))

@app.route('/task_status')
def task_status():
    task_ids = session.get('task_ids', [])
    tasks = [{'id': task_id, 'task': process_files_and_text.AsyncResult(task_id)} for task_id in task_ids]
    return render_template('task_status.html', tasks=tasks)

@app.route('/task_detail/<task_id>')
def task_detail(task_id):
    task = process_files_and_text.AsyncResult(task_id)
    return render_template('task_detail.html', task=task)


def get_apk_files(folder_path):
    apk_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.apk'):
                apk_files.append(os.path.relpath(os.path.join(root, file), folder_path))
    return apk_files


@app.route('/result/<path:filename>')
def result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)


def get_image_files(folder_path, filename, subfolder, status):
    """파일명을 기반으로 해당하는 이미지 리스트 반환 (Fail & Success 모두 포함)"""
    base_name = f"{filename}"  

    images = [
        f"{subfolder}/{f}"  # ✅ 서브폴더 포함한 경로 반환
        for f in os.listdir(folder_path)
        # if f.startswith(base_name) and f.endswith('.jpg')
        if base_name in f and f.endswith('.jpg')
    ]
    return images

def read_csv_as_html_with_images(log_file_path, folder_path, subfolder):
    """CSV 파일을 읽고 각 행에 해당하는 이미지를 추가한 HTML 테이블 생성"""
    try:
        df = pd.read_csv(log_file_path, encoding="utf-8-sig")  # ✅ UTF-8-SIG로 읽기
        print("📄 CSV 데이터 로드 완료")
        print(df.head())  # ✅ 데이터 확인

        if "SubTC/DownloadedFile" in df.columns:
            df.rename(columns={"SubTC/DownloadedFile": "DownloadedFile"}, inplace=True)

        # ✅ `status` 값을 변환 없이 그대로 사용하여 적용
        def get_images(row):
            try:
                if row["DownloadedFile"]=='mix':
                    print(f'{row["OriginalFileName"].split("/")[-1]}')
                    return get_image_files(folder_path, row["OriginalFileName"].split("/")[-1], subfolder, row["status"])
                else:
                    return get_image_files(folder_path, row["DownloadedFile"], subfolder, row["status"])
            except Exception as e:
                print(f"❌ 이미지 검색 오류: {e}")
                return []

        df["Images"] = df.apply(get_images, axis=1)

        # ✅ HTML 테이블 생성 (이미지가 2개 이상이면 강조)
        html_table = '<table class="styled-table">'
        html_table += "<thead><tr>" + "".join(f"<th>{col}</th>" for col in df.columns if col != "Images") + "<th>Images</th></tr></thead>"
        html_table += "<tbody>"

        for _, row in df.iterrows():
            num_images = len(row["Images"])  # ✅ 이미지 개수 확인
            highlight_class = "highlight" if num_images >= 2 else ""  # ✅ 이미지가 2개 이상이면 강조

            html_table += f'<tr class="{highlight_class}">'
            for col in df.columns:
                if col != "Images":
                    html_table += f"<td>{row[col]}</td>"
            
            # ✅ 이미지 표시
            html_table += "<td>"
            if row["Images"]:
                for img in row["Images"]:
                    img_path = f"/result/{img}"  # ✅ 정적 파일 경로 설정
                    html_table += f'<img src="{img_path}" class="thumbnail" alt="{img}" width="100" style="margin-right:5px;">'
            html_table += "</td>"

            html_table += "</tr>"
        html_table += "</tbody></table>"

        return html_table
    except Exception as e:
        return f"<p>CSV 파일을 읽는 중 오류 발생: {str(e)}</p>"
    
        
@app.route('/result/<path:filename>')
def serve_image(filename):
    """result 폴더의 이미지를 제공하는 엔드포인트"""
    return send_from_directory(RESULT_FOLDER, filename)

@app.route('/images/<path:subfolder>')
def list_images_in_subfolder(subfolder):
    """선택한 서브폴더의 CSV 데이터를 테이블로 표시하고, 이미지 목록 출력"""
    folder_path = os.path.join(RESULT_FOLDER, subfolder)

    # CSV 파일 읽기
    log_file_path = os.path.join(folder_path, "result_log.txt")
    log_html = ""
    if os.path.exists(log_file_path):
        # ✅ subfolder 인자를 추가하여 호출
        log_html = read_csv_as_html_with_images(log_file_path, folder_path, subfolder)

    return render_template('image_list.html', log_html=log_html, subfolder=subfolder)
@app.route('/images')
def list_images():
    """서브폴더 목록을 반환"""
    subfolders = [f.name for f in os.scandir(RESULT_FOLDER) if f.is_dir()]
    return render_template('images.html', subfolders=subfolders)
if __name__ == '__main__':
    app.run(debug=True)


# log_file_path='./result/versioncompare_2025_02_13_17_58_31/result_log.txt'
# retvalue='Fail' 
# action='versioncompare' 
# downloaded_file='kine' 
# OriginalFileName='KM-11214.kine' 
# Device='15151FDD4001GT' 
# file_path = ['7.5.1.33830.GP.apk','7.5.16.34132.GP1.apk' ,'7.4.17.33410.GP.apk']
# log_result_csv(
#                     file_path=log_file_path,
#                     action=action,
#                     subtc_or_file=downloaded_file,
#                     original_file_name=OriginalFileName,
#                     device=Device,
#                     apkfile_path1=file_path,
#                     status=retvalue
#                 )
# # log_result_csv(
# #                 file_path=log_file_path,
# #                 action=action,
# #                 subtc_or_file=test.test_type,
# #                 original_file_name=test.subTC,
# #                 device=device,
# #                 apkfile_path1=file_path,
# #                 status=status
# #                 )