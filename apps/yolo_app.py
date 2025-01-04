# from ultralytics import YOLO
# import cv2

# # YOLO 모델 로드 (YOLOv8 사용 예시)
# model = YOLO("yolov8n.pt")  # 사전 학습된 모델 (yolov8n, yolov8m, yolov8l 등 선택 가능)

# # 이미지 로드
# image_path = "./contents/250104/165717/images/capture_001_0002.jpg"
# image = cv2.imread(image_path)

# # 객체 탐지 실행
# results = model(image)

# # 탐지 결과에서 사람(0)과 공(32) 필터링
# filtered_results = [
#     box for box in results[0].boxes if box.cls in [0, 32]
# ]

# # 결과 시각화 및 표시
# for box in filtered_results:
#     x1, y1, x2, y2 = map(int, box.xyxy[0])  # 바운딩 박스 좌표
#     confidence = box.conf[0]  # 신뢰도
#     class_name = model.names[int(box.cls[0])]  # 클래스 이름
    
#     # 바운딩 박스 그리기
#     cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#     cv2.putText(image, f"{class_name} {confidence:.2f}", (x1, y1 - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# cv2.imwrite("./contents/111.jpg", image)

# # # 결과 이미지 보기
# # cv2.imshow("Detections", image)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# from ultralytics import YOLO
# import cv2
# import os

# # YOLO 모델 로드
# model = YOLO("yolov8n.pt")  # 사전 학습된 모델

# # 비디오 경로 설정
# video_path = "./contents/250104/165717/video.mp4"
# output_path = "./contents/output_video_with_boxes.mp4"

# # 비디오 로드
# cap = cv2.VideoCapture(video_path)
# if not cap.isOpened():
#     print(f"Error: Could not open video file: {video_path}")
#     exit()

# # 비디오 정보 가져오기
# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = int(cap.get(cv2.CAP_PROP_FPS))
# total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# max_frames = fps * 60  # 1분 = 60초

# print(f"Video Info - Width: {frame_width}, Height: {frame_height}, FPS: {fps}, Total Frames: {total_frames}")

# # 비디오 저장 설정
# fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 코덱 설정
# out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# # 프레임 단위로 처리
# frame_count = 0
# while frame_count < max_frames:
#     ret, frame = cap.read()
#     if not ret:
#         break  # 비디오 끝

#     # 객체 탐지 실행
#     results = model(frame)

#     # 탐지 결과에서 사람(0)과 공(32) 필터링
#     filtered_results = [
#         box for box in results[0].boxes if box.cls in [0, 32]
#     ]

#     # 바운딩 박스 그리기
#     for box in filtered_results:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])  # 바운딩 박스 좌표
#         confidence = box.conf[0]  # 신뢰도
#         class_name = model.names[int(box.cls[0])]  # 클래스 이름

#         # 바운딩 박스와 텍스트 추가
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(frame, f"{class_name} {confidence:.2f}", (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     # 프레임 저장
#     out.write(frame)
#     frame_count += 1


# # 자원 해제
# cap.release()
# out.release()

# print(f"Processed video saved at {output_path}")



from ultralytics import YOLO
import cv2
import numpy as np

# YOLO Segmentation 모델 로드
model = YOLO("yolov8n-seg.pt")

# 비디오 경로 설정
video_path = "./contents/250104/165717/video.mp4"
output_path = "./contents/output_video_with_masks.mp4"

cap = cv2.VideoCapture(video_path)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
max_frames = fps * 5  # 1분 처리

# 비디오 저장
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

frame_count = 0
while frame_count < max_frames:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 객체 탐지
    results = model(frame)

    # 마스크 존재 여부 확인
    if results[0].masks is not None:
        for box, mask in zip(results[0].boxes, results[0].masks.data):
            if int(box.cls[0]) == 0:  # 사람만 처리
                mask = mask.cpu().numpy()
                resized_mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
                mask_color = np.array([0, 255, 0], dtype="uint8")
                mask_overlay = (resized_mask[:, :, None] * mask_color).astype("uint8")
                frame = cv2.addWeighted(frame, 1.0, mask_overlay, 0.5, 0)

                # 바운딩 박스 추가
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Person {confidence:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    out.write(frame)
    frame_count += 1

cap.release()
out.release()

print(f"Processed video saved at {output_path}")
