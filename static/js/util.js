// 지역과 도시 데이터
var area = {
    "강원특별자치도": ["춘천시", "원주시", "강릉시", "동해시", "태백시", "속초시", "삼척시", "홍천군", "횡성군", "영월군", "평창군", "정선군", "철원군", "화천군", "양구군", "인제군", "양양군"],
    "경기도": ["수원시장안구", "수원시권선구", "수원시팔달구", "수원시영통구", "성남시수정구", "성남시중원구", "성남시분당구", "의정부시", "안양시만안구", "안양시동안구", "부천시원미구", "부천시소사구", "부천시오정구", "광명시", "평택시", "동두천시", "안산시상록구", "안산시단원구", "고양시덕양구", "고양시일산동구", "고양시일산서구", "과천시", "구리시", "남양주시", "오산시", "시흥시", "군포시", "의왕시", "하남시", "용인시처인구", "용인시기흥구", "용인시수지구", "파주시", "이천시", "안성시", "김포시", "화성시", "광주시", "양주시", "포천시", "여주시", "연천군", "가평군", "양평군"],
    "경상남도": ["창원시의창구", "창원시성산구", "창원시마산합포구", "창원시마산회원구", "창원시진해구", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시", "의령군", "함안군", "창녕군", "고성군", "남해군", "하동군", "산청군", "함양군", "거창군", "합천군"],
    "경상북도": ["포항시남구", "포항시북구", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시", "의성군", "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군"],
    "광주광역시": ["광산구"],
    "대구광역시": ["수성구", "달서구", "달성군", "군위군"],
    "대전광역시": ["유성구", "대덕구"],
    "부산광역시": ["서구", "동구", "영도구", "부산진구", "동래구", "남구", "북구", "해운대구", "사하구", "금정구", "연제구", "수영구", "사상구", "기장군"],
    "서울특별시": ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"],
    "세종특별자치시": ["세종특별자치시"],
    "울산광역시": ["울주군"],
    "인천광역시": ["미추홀구", "연수구", "남동구", "부평구", "계양구", "강화군", "옹진군"],
    "전라남도": ["목포시", "여수시", "순천시", "나주시", "광양시", "담양군", "곡성군", "구례군", "고흥군", "보성군", "화순군", "장흥군", "강진군", "해남군", "영암군", "무안군", "함평군", "영광군", "장성군", "완도군", "진도군", "신안군"],
    "전라북도": ["전주시완산구", "전주시덕진구", "군산시", "익산시", "정읍시", "남원시", "김제시", "완주군", "진안군", "무주군", "장수군", "임실군", "순창군", "고창군", "부안군"],
    "제주특별자치도": ["제주시", "서귀포시"],
    "충청남도": ["천안시동남구", "천안시서북구", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군"],
    "충청북도": ["청주시상당구", "청주시서원구", "청주시흥덕구", "청주시청원구", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군", "괴산군", "음성군", "단양군"]
  };
  

function updateCities(region) {
  var citiesSelect = document.getElementById("city");
  citiesSelect.options.length = 0; // 기존 도시 목록을 비웁니다.
  citiesSelect.disabled = true; // 도시 선택 비활성화

  if (region && region !== "--선택--") {
    citiesSelect.disabled = false; // 도시 선택 활성화
    var defaultOption = new Option("--선택--", "");
    citiesSelect.add(defaultOption);
    
    area[region].forEach(function(city) {
      var option = new Option(city, city);
      citiesSelect.add(option);
    });
  }

  validateForm();
}

function initRegions() {
  var regionsSelect = document.getElementById("region");
  var defaultOption = new Option("--선택--", "");
  regionsSelect.add(defaultOption);

  for (var region in area) {
    var option = new Option(region, region);
    regionsSelect.add(option);
  }
  
  validateForm();
}

function validateForm() {
  var submitButton = document.getElementById("submit");
  var region = document.getElementById("region").value;
  var city = document.getElementById("city").value;

  submitButton.disabled = !region || region === "--선택--" || !city || city === "--선택--";
}

function toggleNotificationControls() {
    var alarmTimeSelect = document.getElementById("alarmTime");
    var agree = document.getElementById('agree').checked;
    var submitButton = document.getElementById('save');

    if (agree) {
        alarmTimeSelect.disabled = false;  // 동의하면 알람 시간 선택 가능
        submitButton.disabled = false;     // 동의하면 저장 버튼 활성화
    } else {
        alarmTimeSelect.disabled = true;   // 비동의하면 알람 시간 선택 비활성화
        submitButton.disabled = false;     // 비동의해도 저장 버튼은 활성화
  }
}

window.onload = function() {
  initRegions();
  toggleNotificationControls();
};

