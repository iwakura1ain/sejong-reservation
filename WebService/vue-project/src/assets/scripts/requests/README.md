# /src/assets/scripts/requests

### 이게 대체 뭔가요?
백엔드로부터 데이터를 받고 1차가공 작업을 처리하는 스크립트의 모음입니다.

### 어떤 코드가 있나요?
* `./ request.js` : 요청하고 응답받는 과정을 수행합니다. 각 서비스에 대한 통신코드가 있습니다.
  * AdminService
  * ReservationService
  * UserService
  * AlertService
* `./responseConverters/*.js` : 날것의 백엔드 응답 데이터를 프론트엔드에 적합하게 가공하는 코드입니다.

### 동작 과정이 어떻게되나요?
1. 백엔드로 요청합니다. (request.js)
2. 데이터를 응답받습니다. (request.js)
3. 응답받은 날 것의 데이터를 프론트엔드가 쓰기 좋게 가공합니다. (request.js --> responseConverters/convert___Res.js)
4. 가공한 데이터를 아래의 형식으로 callee에 반환합니다.

```js
return {
  status : Boolean
  data : 가공된 데이터(converted)
  msg : 응답데이터에 담겨온 msg
}
```