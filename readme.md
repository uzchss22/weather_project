# flask 날씨 알리미 프로젝트


1. 개요
대학 캡스톤 프로젝트

2. 팀
    * 이재혁(조장)
    * 이현식
    * 김형준
    * 최혁

3. 기능설명
    1. 프론트엔드
        * index.html: 날씨정보를 받을 지역을 설정하는 페이지.
        * weather.html: 날씨 정보를 보는 페이지.
        * air.html: 미세먼지정보를 받을 지역을 설정하는 페이지.
        * airDisplay.html: 미세먼지 정보를 보는 페이지.
        * alarm.html: 알림을 받는페이지
        > 푸시알림 api 서버에 인증키 넣는곳에서 막혀서 임시로 javascript로 작성
        * util.js: 클라이언트 단에서 기능적인 부분을 담당.
        * style.css: 스타일
    2. 백엔드
        * app.py: 파이썬 함수를 호출하고 페이지를 리디렉션.
        * db_manager.py: db와 관련된 모든 기능.
        > 인증키 보안 때문에 임시 값으로 변경되어있음.
        * weather_api.py: 기상청 허브 api 요청.
        > 240618 갑자기 api request 요청이 안됨.
        >> 기상청 api허브에 문의 넣음.
        >>> 기상청 api hub는 기상 **예보** 인데 익일 현재시간 이후의 시간대는 요청이 안됨. 널널하게 1시간 전 데이터를 불러와야 함.
        * air_api.py: 미세먼지 api 요청
        * region_data.csv: 기상청 api hub에서 제공하는 지역별 격자정보에서 비슷한 동네는 합쳐놓음.

4. 느낀점
aws elastic beanstalk 서비스로 웹 서버 배포하려 했는데 과정이 너무 어려웠음.
웹 푸시 알림기능을 다 구현하지 못해 아쉽다. 시간 분배를 잘 합시다!
다음 프로젝트는 더 열심히 해야겠습니다.
