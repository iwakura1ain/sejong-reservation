# sejong-reservation
## 소금구이덮밥 

## 1. 팀원

- 이원진 / 컴퓨터공학과 / 17011573 / studioplug17@gmail.com / 010-5898-9817
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/8d721fb4-ba53-44d1-81f4-86d5b5df5ab0/Untitled.jpeg)
    
- 안창언 / 컴퓨터공학과 / 17011505 / ernie937@gmail.com
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d68be413-8a61-4f7c-8c36-2a16656cac64/Untitled.png)
    
- 장호진 / 컴퓨터공학과 / 17011540 / jhojin7@sju.ac.kr / 010-4534-7640
    
    ![Screenshot_20230207_114124_Drive.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0d0e2d3a-b201-4d16-9312-13ecf2d2f409/Screenshot_20230207_114124_Drive.jpg)
    
- 한수현 / 컴퓨터공학과 / 18011561 / suess98@naver.com


## 2. 개발 목표 
 <회의실 예약 시스템>은 대양AI센터 835호, 836호의 현행 수기 예약 체계를 대체하기 위한 목적으로 개발되고 있다. 모두가 쉽게 접근할 수 있는 전산 시스템의 개발로 수기식이라는 태생 자체에서 기인한 문제를 해결하고자 한다. 

 <회의실 예약 시스템>은 웹 어플리케이션이다. 네이티브 어플리케이션 대비 운영체제 의존성이 낮은 본래의 특성에 더해 UI를 반응형으로 구성함으로써 윈도우즈, 맥, 리눅스 등을 사용하는 PC는 물론 모바일 기기의 브라우저도 지원한다. 가장 중요한 예약기능을 충실히 지원하면서 직관적인 UI/UX와 이메일을 통한 회의 알림기능 등 부가적인 요소들을 제공할 예정이다. 예상 사용자는 세종대학교 컴퓨터공학과 구성원이다. 본 시스템을 통해 회의실 예약을 간단하고 원격으로 처리할 수 있을 것으로 기대한다. 


## 3. 전체 프로젝트 구조 

- 프론트엔드를 담당하는 Web 서비스
- 백엔드를 담당하는 User, Reservation, Admin, Alert 서비스
- 백엔드 서비스들이 공통적으로 상속받는 Service 클래스 
- 프로젝트 DB가 구축되어 있는 DB 서비스
- 모든 서비스들은 RESTful 방식으로 서로 통신
