# 프론트엔드 프로그램

### 테스트목적 실행 방법

* 도커로 돌리는 방법이 아닙니다. `[src]`폴더 안에 있는 파일들을 실시간 빌드해서 보는 방법입니다. 
* 도커로 돌리는 방법은 이 폴더 바로위의 `[WebService]`폴더 참고

1. 컴퓨터에 Node.js가 설치되어 있어야 합니다. npm을 사용합니다. (설치 링크 : https://nodejs.org/ko/download)
2. 터미널로 `[vue-project]`폴더에 들어갑니다.
3. `npm i` 입력 : 라이브러리 설치
4. `npm run dev` 입력 : 개발서버 실행

5. **(혹시?)** 도커로 웹앱을 돌리기 위해 `dist`폴더가 필요하신가요? 그럼 `npm run build`하시면 됩니다. dist가 생겨요.

### 프로젝트 구조

```
[vue-project]
└─ package.json : 프로젝트 개요 기술(이름, 버전, 필요한 라이브러리 등)
└─ package.json : (상동)
└─ .eslintrc.cjs : 코드 자동 포맷팅 설정
└─ .prettierrc.json : (상동)
└─ vite.config.js : 웹앱 빌드 설정
│
└─ index.html : 생각하는 index파일 맞음
│
└─ [public] : index.html에서 불러와야 하는 파일
│   └─ favicon.ico
│   └─ reset.css  
│
└─ [src] : 사실상 웹앱의 모든 것
    └─ main.js : "index.html"에 "App.vue"를 박아넣는 스크립트
    └─ App.vue : 웹앱의 최상위 컴포넌트
    └─ router.js : url path에 따라 다른 화면을 보여주기 위한 라우팅 설정파일
    │
    └─ [assets] : 이미지, css, script
    └─ [layouts] : 아주 빈번하게 등장하는 컴포넌트
    └─ [views] : "App.vue"의 router-view를 대체하는 컴포넌트
    └─ [components] : 기타 컴포넌트
```


