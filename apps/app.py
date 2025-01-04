from pytubefix import YouTube
from datetime import datetime
import os
import cv2

class nammtubee():

    def __init__(self, url="", upper_dir="", lower_dir=""):
        self.url = url
        self.upper_dir = upper_dir
        self.lower_dir = lower_dir
        
        self.upper_path = f"./contents/{upper_dir}" if self.upper_dir else ""
        self.lower_path = f"{self.upper_path}/{lower_dir}" if self.lower_dir else ""
        
        self.video_path = ""
        self.audio_path = ""
        self.image_path = ""
        pass
    
    def download(self):
        print("-- starting Download") 
        def progress_function(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            percent_complete = (total_size - bytes_remaining) / total_size * 100
            print(f"Progress: {percent_complete:.2f}%")
        
        video_filename = "video.mp4"
        audio_filename = "audio.mp3"
        if "" in [self.upper_dir, self.lower_dir]:
            self.upper_dir, self.lower_dir = datetime.now().strftime("%y%m%d/%H%M%S").split("/")
            self.upper_path = f"./contents/{self.upper_dir}"
            self.lower_path = f"{self.upper_path}/{self.lower_dir}"
        
            yt = YouTube(self.url, on_progress_callback=progress_function)

            ys_v = yt.streams.filter(res="720p").first() # 화질
            ys_a = yt.streams.filter(only_audio=True).first()

            os.makedirs(self.upper_path, exist_ok=True) # 날짜
            os.makedirs(self.lower_path, exist_ok=True) # 시간

            ys_v.download(output_path=self.lower_path, filename=video_filename) # 비디오 파일 저장
            ys_a.download(output_path=self.lower_path, filename=audio_filename) # 오디오 파일 저장

            self.video_path = os.path.join(self.lower_path, video_filename)
            self.audio_path = os.path.join(self.lower_path, audio_filename)
            
        else:
            content_path = f"./contents/{self.upper_dir}/{self.lower_dir}"
            
            self.video_path = os.path.join(content_path, video_filename)
            self.audio_path = os.path.join(content_path, audio_filename)
        
        print("-- finished Download")    
        print(f"    * video_path: {self.video_path}")
        print(f"    * audio_path: {self.audio_path}")
        print("="*50)
        return self.video_path, self.audio_path
    
    
    def capture(self):
        print("-- starting Capture") 
        self.image_path = os.path.join(self.lower_path, "images")
        if os.path.exists(self.image_path):
           pass
       
        else:
            os.makedirs(self.image_path)
            video = cv2.VideoCapture(self.video_path)

            fps = video.get(cv2.CAP_PROP_FPS)  # 프레임 속도
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # 총 프레임 수
            frame_interval = int(fps * 2)  # 10초 간격 (10초 * FPS)
            frame_count, capture_count = 0, 0
            
            # 진행률 체크를 위한 마일스톤 설정
            milestones = [0.25, 0.5, 0.75, 1.0]  # 25%, 50%, 75%, 100%
            milestone_index = 0
            
            
            while True:
                ret, frame = video.read()
                if not ret:
                    print(f"Progress: {int(milestones[milestone_index] * 100)}%")
                    break
                
                # 10초 간격 프레임인지 확인
                if (frame_count % frame_interval == 0):
                    current_time_sec = frame_count / fps
                    minutes, seconds = divmod(int(current_time_sec), 60)
                    time_str = f"{minutes:02d}{seconds+1:02d}"  # 분초 형식으로 포맷팅
                    
                    progress = frame_count / total_frames # 현재 프레임의 진행률 계산
                    if milestone_index < len(milestones) and progress >= milestones[milestone_index]:
                        print(f"Progress: {int(milestones[milestone_index] * 100)}%")
                        milestone_index += 1
                        
                    output_path = os.path.join(self.image_path, f"capture_{capture_count:03d}_{time_str}.jpg") # capture_057_0154.jpg : 57번째 사진이며 01분54초 화면
                    cv2.imwrite(output_path, frame)  # 이미지 저장
                    capture_count += 1

                frame_count += 1
            video.release()
            
        print("-- finished Capture")    
        print(f"    * image_path: {self.image_path}")
        print("="*50)
        return self.image_path
    
    def contour(self):
        print("-- starting Contour") 
        self.contour_path = os.path.join(self.lower_path, "contours")
        os.makedirs(self.contour_path, exist_ok=True)
        # if os.path.exists(self.contour_path):
        #    pass
        
        # else:
            # os.makedirs(self.contour_path)
        image_files = [f for f in os.listdir(self.image_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        for image_file in image_files:
            # 이미지 읽기
            input_image_path = os.path.join(self.image_path, image_file)
            image = cv2.imread(input_image_path)
            
            if image is None:
                print(f"Failed to load {input_image_path}")
                continue
            
            # 이미지 그레이스케일 변환
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # 이진화
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            # 윤곽선 찾기
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 윤곽선 그리기
            outlined_image = image.copy()
            cv2.drawContours(outlined_image, contours, -1, (0, 255, 0), 2)  # 초록색, 두께 2

            # 결과 저장
            output_image_path = os.path.join(self.contour_path, image_file.replace("capture", "contour"))
            cv2.imwrite(output_image_path, outlined_image)
            print(f"Saved outlined image: {output_image_path}")
            
        print("-- finished Contour")    
        print(f"    * contour_path: {self.contour_path}")
        print("="*50)
        return 
    
    def contour_video(self):
        video = cv2.VideoCapture(self.video_path)
        self.output_path= "./contents/output.mp4"
        # 원본 동영상 정보 가져오기
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # MP4 코덱
        # 출력 동영상 설정
        output_video = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))
        while True:
            ret, frame = video.read()
            if not ret:
                break

            # 그레이스케일로 변환
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 이진화
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            # 윤곽선 찾기
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 윤곽선 그리기
            contour_frame = frame.copy()
            cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 2)  # 초록색, 두께 2

            # 프레임 저장
            output_video.write(contour_frame)
        # 자원 해제
        video.release()
        output_video.release()
        print(f"윤곽선이 그려진 동영상이 저장되었습니다: {self.output_path}")
        return 
        
####################################################################################################
####################################################################################################


if __name__ == "__main__":
    # nt = nammtubee(url="https://www.youtube.com/watch?v=AYfwQISVGQk", 
    #                upper_dir="", 
    #                lower_dir="")
    nt = nammtubee(url="", 
                   upper_dir="250104", 
                   lower_dir="165717")
    video_path, audio_path = nt.download()
    image_path = nt.capture()
    # contour_path = nt.contour()
    nt.contour_video()