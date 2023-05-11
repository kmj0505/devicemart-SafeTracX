import torch
import cv2
import numpy as np
import socket
import select
from datetime import datetime
from utils.torch_utils import select_device, time_sync
from utils.general import non_max_suppression
from utils.general import scale_boxes
from models.experimental import attempt_load

# 객체 감지를 위한 Yolov5 모델 불러오기
weight = '/home/ubuntu/Project/yolov5-master/industhelmet.pt'

# GPU or CPU 디바이스 설정
device = select_device('')

# YOLOv5 모델 로드
model = attempt_load(weight,device=device)

# YOLOv5 inference 설정값
conf_thres = 0.85
iou_thres = 0.45

# 캠 설정
url = "http://10.10.141.202:4747/video"
cap = cv2.VideoCapture(url)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 프레임 폭 설정
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 프레임 높이 설정

# 텍스트 출력 폰트 설정
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 3

# 소켓 통신 설정
HOST = '10.10.141.69'  # 서버의 IP 주소
PORT = 5000        # 서버의 포트 번호
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send('[HelCheck:PASSWD]\n'.encode())

# 소켓 통신 non-blocking 모드 설정
client_socket.setblocking(False)
inputs = [client_socket]

# 상태 값 초기 설정
state = 0

# 객체 감지 함수 정의
while True:
    # 소켓 통신 처리
    readable, _, _ = select.select(inputs, [], [], 0.1)
    for sock in readable:
        data = sock.recv(1024)
        if not data:
            inputs.remove(sock)
        else:
            name = data.decode().strip()[6:]
            print(name)

    # 캠에서 프레임 읽어오기
    ret, frame = cap.read()

    if not ret:  # 캠에서 프레임을 제대로 읽어왔는지 확인
            # 프레임 전처리
        print('Error reading frame from webcam!')
        break

    img = frame[:,:,::-1].copy() # 입력 이미지를 RGB 채널 순서로 변경
    img = torch.from_numpy(img).to(device=device)  # NumPy 배열로부터 PyTorch tensor를 생성
    img = img.permute(2,0,1).float().unsqueeze(0)/255.0 # 이미지 tensor를 정규화 후 RGB 채널을 첫 번째 차원으로 변경하고, tensor를 float 자료형으로 변환, 차원을 추가하여 배치 크기를 1로 만들고 255로 나누어 값을 [0,1] 범위로 조정
           
        # 객체 감지
    with torch.no_grad():
        time1 = time_sync()
        results = model(img)[0]
        results = non_max_suppression(results, conf_thres, iou_thres, classes = None, agnostic=False)
        time2 = time_sync()

    if len(results) > 0: # 검출된 객체가 있는 경우에만 다음 코드 블록을 실행
        now = datetime.now()
        results = results[0]
        # 박스 좌표 스케일링
        results[:,:4] = scale_boxes(img.shape[2:],results[:,:4],frame.shape).round() # bounding box 좌표를 입력 이미지 크기에 맞게 스케일링
        for *xyxy, conf, cls in reversed(results): # bounding box 좌표, confidence score, class id를 반복문 변수로 사용하여 출력, reversed 함수를 이용해서 결과를 역순으로 출력
            number = model.names[int(cls)]  # number = 객체 이름
            label = f'{number}{conf:.2}' # label = 객체 이름 + 정확도
            print(label)
            if(name == 'KMJ' or name == 'KYH' or name == 'JYH' or name == 'RHJ'):
                state = 1
                
            if(state == 1):
                f=open('safetyhelmetdb.txt','a')
                f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S ')}{name}{' Helmet OK'}\n")
                client_socket.send('[Info]{}@OK\n'.format(name).encode())  # WorkerInfo
                name = ''
                state = 0

            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 0, 255), 2)
            cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1])-10), font, font_scale, (0, 255, 255), font_thickness)


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
    # 종료 시 소켓 닫기

cap.release()
