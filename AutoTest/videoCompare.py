import os
import shutil
import ssl
import time

import ffmpeg
import lpips
import natsort
import torch
from PIL import Image
from torchvision import transforms
# import numpy as np
# import librosa

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import librosa


# 동일한 파일을 주는 경우 리버스 검토
class videoComapre:
    def __init__(self, inputVideo1,inputVideo2):
        self.inputVideo1 =inputVideo1
        self.inputVideo2 =inputVideo2
        ssl._create_default_https_context = ssl._create_unverified_context
        # Load LPIPS model
        self.loss_fn = lpips.LPIPS(net='alex',verbose=False)
        # You can use 'alex', 'vgg', or 'squeeze'
        if inputVideo1==inputVideo2:
            self.reverse = True
        else:
            self.reverse = False
        # Define a transform to convert images to tensor and normalize
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),  # Resize to 256x256
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
    
    def extract_frames(self,inputfile):
         
        output_folder = os.path.dirname(inputfile)+'/' +os.path.splitext(os.path.basename(inputfile))[0]
        # output_folder삭제후 새로 생성
        print(f"extract_frames {output_folder}")
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        
        os.makedirs(output_folder)
        time.sleep(2)
        try:
            ffmpeg.input(inputfile).output(os.path.join(output_folder, 'frame_%04d.png')).run(capture_stdout=True, capture_stderr=True)
        except:
            time.sleep(2)

    def extract_audio(self,inputfile):
        output_folder = os.path.dirname(inputfile)+'/' +os.path.splitext(os.path.basename(inputfile))[0]
        if os.path.exists(output_folder)==False:
            os.makedirs(output_folder)
        output_folder = os.path.dirname(inputfile)+'/' +os.path.splitext(os.path.basename(inputfile))[0]
        ouput_file = os.path.join(output_folder, 'Audio.wav')
        time.sleep(2)
        try:
            ffmpeg.input(inputfile).output(ouput_file, acodec="pcm_s16le", ar=44100).run(capture_stdout=True, capture_stderr=True)
        except:
            time.sleep(2)
        return ouput_file

    def compare_frames(self):
        Maximg2 = None
        Maximg1 = None
        max_frame = None
        print(f"{self.inputVideo1} / {self.inputVideo2}")
        self.extract_frames(self.inputVideo1)
        self.extract_frames(self.inputVideo2)
        frames_dir1 = os.path.dirname(self.inputVideo1)+ '/'+os.path.splitext(os.path.basename(self.inputVideo1))[0]
        frames_dir2 = os.path.dirname(self.inputVideo2)+ '/'+os.path.splitext(os.path.basename(self.inputVideo2))[0]
        # List frame files
        #frames1 = sorted(os.scandir(frames_dir1))
        #frames2 = sorted(os.scandir(frames_dir2))

        all_files1 = os.listdir(frames_dir1)
        # .DS_Store 파일 제외
        filtered_files1 = [f for f in all_files1 if f != '.DS_Store']
        all_files2 = os.listdir(frames_dir2)
        # .DS_Store 파일 제외
        filtered_files2 = [f for f in all_files2 if f != '.DS_Store']

        # 자연스러운 정렬
        frames1 = natsort.natsorted(filtered_files1)
        frames2 = natsort.natsorted(filtered_files2)
 
        # frames1 = natsort.natsorted(os.listdir(frames_dir1))
        # frames2 = natsort.natsorted(os.listdir(frames_dir2),reverse)
        
        # Ensure both directories have the same number of frames
        # print(f' {len(frames1)} LPIPS score: {len(frames2)}')
        #assert len(frames1) == len(frames2), "Different number of frames in each video {}"
        # Compare frames
        total_score = 0
        max_score = 0

        for frame1, frame2 in zip(frames1, frames2):
            # if frame1!='.DS_Store' :
            img1 = Image.open(os.path.join(frames_dir1, frame1))
            img2 = Image.open(os.path.join(frames_dir2, frame2))


            # Apply transformations
            imgt1 = self.transform(img1).unsqueeze(0)  # Add batch dimension
            imgt2 = self.transform(img2).unsqueeze(0)  # Add batch dimension

            # Compute LPIPS score
            with torch.no_grad():
                score = self.loss_fn(imgt1, imgt2)
                if score>max_score or  Maximg2 ==None:
                    max_score = score
                    Maximg2 = img2
                    Maximg1 = img1
                    
        # print(f'{os.path.basename(self.inputVideo1)} , {os.path.basename(self.inputVideo2)} Average LPIPS score: {avg_score} Max Score: {max_score} max_frame: {max_frame}')
        # if max_score<0.01:
        shutil.rmtree(frames_dir1)
        shutil.rmtree(frames_dir2)
            # os.remove(self.inputVideo1)
            # os.remove(self.inputVideo2)
        return max_score,Maximg2,Maximg1
    def compare_audio(self):

        print(f"{self.inputVideo1} / {self.inputVideo2}")
        input1 = self.extract_audio(self.inputVideo1)
        input2 = self.extract_audio(self.inputVideo2)
        
       # 오디오 로드
        audio1, sr1 = librosa.load(input1, sr=None)
        audio2, sr2 = librosa.load(input2, sr=None)

        # 오디오 길이 맞추기
        min_length = min(len(audio1), len(audio2))
        audio1 = audio1[:min_length]
        audio2 = audio2[:min_length]

        # 벡터 변환 후 유사도 비교
        audio1 = audio1.reshape(1, -1)
        audio2 = audio2.reshape(1, -1)

        similarity = cosine_similarity(audio1, audio2)[0][0]
        print(f"Cosine Similarity: {similarity}")
        
        return similarity,input1,input2
# lc = lpipsCompare('/Users/yk.moon/Downloads/note.mp4','/Users/yk.moon/Downloads/719.mp4')
# max,img1,img2 = lc.compare_frames()
# img1.save('/Users/yk.moon/Downloads/note.jpg')
# img2.save('/Users/yk.moon/Downloads/719.jpg')
# print(f' {max} LPIPS score: {max}')     

