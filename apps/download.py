from pytubefix import YouTube
from datetime import datetime
import os
 
def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    percent_complete = (total_size - bytes_remaining) / total_size * 100
    print(f"Progress: {percent_complete:.2f}%")
    
url = 'https://www.youtube.com/watch?v=gvXsmI3Gdq8'
 
yt = YouTube(url, on_progress_callback=progress_function)

ys_v = yt.streams.filter(res="720p").first() # 화질
ys_a = yt.streams.filter(only_audio=True).first()

upper_dir, lower_dir = datetime.now().strftime("%y%m%d/%H%M%S").split("/")
upper_path = f"./contents/{upper_dir}"
lower_path = f"./contents/{upper_dir}/{lower_dir}"

os.makedirs(upper_path, exist_ok=True) # 날짜
os.makedirs(lower_path, exist_ok=True) # 시간

ys_v.download(output_path=lower_path, filename="my_video.mp4")
ys_a.download(output_path=lower_path, filename="audio.mp3")  # 오디오 파일로 저장