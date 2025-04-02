import os
import requests
import json

class JiraDownloader:
    def __init__(self, download_dir="downloads"):
        """
        Jira API 설정 및 초기화
        """
        with open("config.json", "r") as file:
            config = json.load(file)
        self.jira_url = config["jira_url"]
        self.jira_user = config["jira_user"]
        self.jira_token = config["jira_token"]

        self.max_results = 100
        self.download_dir = download_dir


        # 다운로드 디렉토리 생성
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

    def fetch_tickets(self, project_name, status="Closed"):
        """
        Jira 프로젝트의 모든 티켓 가져오기
        """
        start_at = 0
        all_issues = []
        # project = KM AND status = close
        #key = KM-10489",
        while True:
            # JQL Query
            query = {
                # "jql": f"project = {project_name}",
                # "jql": f"project = {project_name} AND status = {status}" ,
                #  "jql": f"key = KM-12262",
                "jql": f"{project_name}",
                "fields": ["description", "attachment"],
                "maxResults": self.max_results,
                "startAt": start_at
            }
            print(f'query{query}')
            # Jira API 요청
            response = requests.get(
                self.jira_url,
                headers={"Content-Type": "application/json"},
                auth=(self.jira_user, self.jira_token),
                params=query
            )

            if response.status_code == 200:
                data = response.json()
                issues = data.get("issues", [])
                all_issues.extend(issues)

                # 마지막 페이지인지 확인
                if len(issues) < self.max_results:
                    break

                start_at += self.max_results
            else:
                print(f"Error fetching tickets: {response.status_code} - {response.text}")
                break

        return all_issues

    def get_kine_links(self, tickets):
        """
        티켓 목록에서 .kine 첨부 파일 링크 추출
        """
        kine_links = []

        for ticket in tickets:
            ticket_key = ticket["key"]
            attachments = ticket["fields"].get("attachment", [])

            # Attachments에서 .kine 파일 링크 추출
            for attachment in attachments:
                if attachment["filename"].endswith(".kine"):
                    kine_links.append({
                        "ticket": ticket_key,
                        "filename": attachment["filename"],
                        "link": attachment["content"]
                    })

        return kine_links
    def download_file(self, url, ticket_key, filename):

        try:
            # URL의 마지막 ID 추출
            url_id = url.rstrip("/").split("/")[-1]

            # 파일명에 티켓 키와 URL ID 추가
            base_filename = f"{ticket_key}_{url_id}.kine"
            file_path = os.path.join(self.download_dir, base_filename)

            # 파일이 이미 존재하면 다운로드를 건너뜀
            if os.path.exists(file_path):
                print(f"File already exists: {file_path}")
                return base_filename

            # 파일 다운로드
            response = requests.get(url, auth=(self.jira_user, self.jira_token), stream=True)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"File downloaded: {base_filename}")
                return base_filename
            else:
                print(f"Failed to download file: {url} - Status Code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None
    # def download_file(self, url, ticket_key, filename):
    #     """
    #     링크를 통해 파일 다운로드
    #     파일명을 JIRA 티켓 이름으로 저장하며, 중복 파일의 경우 인덱스를 추가.
    #     """
    #     try:
    #         # 파일명에 티켓 키 추가
    #         base_filename = f"{ticket_key}.kine"
    #         file_path = os.path.join(self.download_dir, base_filename)

    #         # 파일명이 중복되는 경우 인덱스를 추가
    #         index = 1
    #         while os.path.exists(file_path):
    #             base_filename = f"{ticket_key}_{index}.kine"
    #             file_path = os.path.join(self.download_dir, base_filename)
    #             index += 1

    #         # 파일 다운로드
    #         response = requests.get(url, auth=(self.jira_user, self.jira_token), stream=True)
    #         if response.status_code == 200:
    #             with open(file_path, "wb") as file:
    #                 for chunk in response.iter_content(chunk_size=8192):
    #                     file.write(chunk)
    #             print(f"File downloaded: {base_filename}")
    #             return base_filename
    #         else:
    #             print(f"Failed to download file: {url} - Status Code: {response.status_code}")
    #             return None
    #     except Exception as e:
    #         print(f"Error downloading file: {e}")
    #         return None


# if __name__ == "__main__":
#     # Jira 설정
#     JIRA_URL = "https://kinemastercorp.atlassian.net/rest/api/2/search"
#     JIRA_USER = "yk.moon@kinemaster.com"
#     JIRA_TOKEN = "ATATT3xFfGF0SGCp3MpGRT_No1Rc_5ZjoRmYHBileOEFttjDVB3JvnZzQ3Wo7q3s-1Hi5QUXs6MmaQZljhAX4To7iROpFaewNsvVaws5xpMc6fdGh6gq_P50pv91yQHB7bSOatTbgUb_oPtHDBfUaPzSWW9HQJXR-gkdLaM6vk2CrbodWNKiOng=CEC8A430"

#     # 인스턴스 생성
#     jira_downloader = JiraDownloader("Test")

#     # 프로젝트별 데이터 처리
#     # projects = ["KM", "nesa"]
#     projects = ["key = KM-11214"]
#     for project in projects:
#         tickets = jira_downloader.fetch_tickets(project)
#         kine_links = jira_downloader.get_kine_links(tickets)

#         # 각 링크를 순차적으로 다운로드
#         for kine in kine_links:
#             print(f"Processing ticket: {kine['ticket']}")
#             print(f"File: {kine['filename']} | Link: {kine['link']}")
            
#             # 다운로드 호출
#             file_path = jira_downloader.download_file(kine['link'], kine['ticket'], kine['filename'])
#             if file_path:
#                 print(f"Downloaded: {file_path}")
#             else:
#                 print(f"Failed to download: {kine['filename']}")