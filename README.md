# Devicemart-SafeTracX
2023 ICT convergence project contest by devicemart

## 프로젝트 기간

2023.02 ~ 2023.03

## 프로젝트 요약
- 각종 사건사고가 많은 산업 현장에서 안전하게 근무할 수 있는 환경 조성을 목표로 구현
- 예기치 못한 사고가 일어났을 때를 대비하여 건물 내 근로자 수, 근로자 정보 데이터베이스 저장

## 프로젝트 개요
1. 안전장비 미착용으로 인해 발생하는 사고 방지를 위한 모니터링 시스템
2. 근로자의 근무 가능 상태 여부 확인 시스템
3. 사고 발생 시 근로자의 위치와 정보를 확인
4. 근로자의 위치 데이터 수집으로 현재 이동 경로와 현재 위치 확인
5. 건물 내 근로자의 수를 확인할 수 있는 모니터링 시스템

## 프로젝트 사용 기술
- C
- C++
- Python
- OpenCV
- TCP/IP Socket Communication
- Raspberry Pi
- Ubuntu
- Linux

## 시스템 구성
<p align="center"><img src="https://github.com/kmj0505/smart-farm-project/assets/123744547/d9b8506a-3a84-4103-bd2f-7ba9fc41087e" style="width: 80vw; min-width: 400px;" /></p>

- 본 시스템은 근로자가 직접 착용하는 안전장비와 근로자의 인적 사항, 헬멧 착용 여부, 출입 근로자 수 등의 정보를 알 수 있는 모니터링 시스템으로 이루어져 있다. Main 서버에 Client들이 소켓으로 연결되어 있는 다중 쓰레드 통신이고, 이를 활용해 Client들끼리 상호 간의 통신이 이루어진다.
  
- 근로자가 착용하는 안전장비는 안전모와 안전조끼가 있으며, 안전모에는 초음파 센서, 알코올/가스 센서, 온도 센서를 부착하여 근로자의 음주 상태 및 가스 누출 위험을 판별하여 근무 가능 여부를 확인하였다. 안전조끼에는 IMU 센서를 통해 근로자의 위치를 알 수 있고, 4x4 버튼을 이용해 메시지를 출력하는 기능을 구현하였으며 개발 보드는 ESP32를 사용하였다.
- 모니터링 시스템에는 RFID KEY를 이용해 근로자의 인적 사항을 안전모와 안전 조끼에 등록시켰다. 이후 OpenCV를 활용해 안전모를 인식하여 근로자가 안전모 착용을 했는지 확인하고, 건물을 입출입하는 사람을 인식하여 건물 내 사람의 수를 실시간으로 나타내는 시스템으로 구현하였다.

## OpenCV 영상처리 시스템
### 1) Detect Safety Helmet
<p align="center"><img src="https://github.com/kmj0505/smart-farm-project/assets/123744547/bd747018-85f4-43f3-b296-2952a7e0f552"></p>
<p align="center"><img src="https://github.com/kmj0505/smart-farm-project/assets/123744547/65bae02d-4df2-46b5-a7ab-cc8b5e0803ea"></p>

- 근로자의 안전모 착용 여부를 영상처리로 감지하기 위해 안전모 데이터가 필요하였고, Roboflow의 ‘industrial-safety-helmet’ 데이터 셋을 활용해 Google Colab에서 데이터를 학습하였습니다. 이 과정에서 정밀도와 재현율의 평균을 나타내는 F1 지표의 최댓값은 0.94를 나타냈으며, [그림 2]과 같이 근로자가 안전모를 착용했을 때 감지할 수 있는 결과를 나타냈습니다.

<p align="center"><img src="https://github.com/kmj0505/smart-farm-project/assets/123744547/b8c42102-7fc7-4d81-bf40-16eee77742f6"></p>
<p align="center"><img src="https://github.com/kmj0505/smart-farm-project/assets/123744547/9a01753d-82cb-4a84-b6ae-bd68b7be8fc0"></p>

- 근로자가 RFID Key를 인식해 [Info] Client에서 근로자 정보를 보내오면, 안전모 착용 여부를 확인해 ‘날짜+시간+근로자 이름+’Helmet OK’ 데이터를 저장합니다. 이후 [Info] Client에 ‘근로자 이름@OK’를 재전송하고 이름을 초기화합니다. ([그림 4])

### 2) Area In & Out Counter
<p align="center"><img src="https://github.com/kmj0505/smart-farm-project/assets/123744547/af2830d7-0f19-41ce-a806-bd41537d167d"/></p>
<p align="center"><img src="https://github.com/kmj0505/smart-farm-project/assets/123744547/cb679007-29c8-4101-b8fc-57dbaddbcda8"/></p>

- 비상 상황을 대비해 건물 입구 CCTV에 'People-Counting-in-Realtime‘을 접목시켜 건물 내의 근로자의 수를 실시간으로 파악할 수 있게 구현했다. 스마트폰 카메라를 CCTV로 가정하고([그림 3]), 프레임의 가운데에 세로 선을 출력하였다([그림 4]).

- 세로 선 기준으로 인식한 객체가 오른쪽에서 왼쪽으로 이동할 때 Enter(들어온 사람)로 설정하였고 반대로, 객체가 왼쪽에서 오른쪽으로 이동할 때 Exit(나간 사람)로 설정하였다. 이후 Enter - Exit = Total people inside로 현재 건물에 있는 사람의 수를 파악할 수 있다.

## 기대효과
- 안전장비의 착용 유무 판별을 통해 안전한 작업 환경 조성
- IMU 센서 기반으로 위치를 모니터링하고 사고 유무 판별을 통해 사고 발생 시 빠른 대처 가능
- 안전장비마다 근로자의 정보를 업로드하여 근무할 수 있는지 파악 등 개인별 안전 상황 파악 가능
