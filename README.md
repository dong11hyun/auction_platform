#### 가상환경 사용 / 독립적인 패키지 버전 관리
- 배포용이성
#### 앱구조
-장고 기능별로 앱을 분리하는 철학 반영
auction_platform/
├── apps/
│   ├── accounts/      # 회원 관련 = 하나의 독립적 모듈
│   ├── auctions/      # 경매 관련 = 하나의 독립적 모듈
│   ├── bids/          # 입찰 관련 = 하나의 독립적 모듈
1.) 단일책임 원칙
2.) 재사용성
#### 추가 디렉토리 구조의 의미
core/
  services/      # 비즈니스 로직 (여러 앱이 공유)
  tasks/         # Celery 백그라운드 작업

websockets/      # WebSocket Consumer (실시간 통신)
common/          # 공통 유틸리티
#### settings 설정
- .env 파일 사용해서 민감정보 코드와 분리, 환경별 설정, 협업
```
INSTALLED_APPS = [
    'daphne',  # ← 1. 최상단: ASGI 서버 (WebSocket 지원)
    
    # Django 기본 앱들
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    
    # Third Party (외부 라이브러리)
    'rest_framework',
    'channels',
    
    # Local Apps (우리가 만든 앱)
    'apps.accounts',
    'apps.auctions',
]
```



