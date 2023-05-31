// 백엔드로부터 응답받은 유저(인증) 데이터를 프론트엔드에 맞게 변환합니다.
// 1. Mapping
// 2. 백엔드 응답 데이터 스키마
// 3-1. 프론트엔드 데이터 스키마
// 3-2. 프론트엔드 데이터 예시

// --------------------------------------------
// 1. 백엔드 응답 데이터 --> 프론트엔드 데이터 Mapping.
// --------------------------------------------
export default function convertUserRes(
	user,
	access_token = null,
	refresh_token = null,
) {
	const { id, name, dept, phone, email, type, no_show, created_at } = user;
	const obj = {
		accessToken: access_token,
		refreshToken: refresh_token,
		noShow: no_show,
		id,
		name: name ? name : '이름 없는 사용자',
		email,
		phone: phone ? phone : '01000000000',
		type,
		dept,
	};
	return obj;
}

// --------------------------------------------
// 2. 백엔드 응답 데이터 스키마
// --------------------------------------------
/*
{
	"status": Boolean,
  "access_token": String,
  "refresh_token": String,
  "User": {
      "id": String,
      "name": String | null,
      "dept": Int, // 
      "phone": String(2) | null,
      "email": String(50),
      "type": Int,
      "no_show": Int
  }
}
*/

// --------------------------------------------
// 3-1. 프론트엔드 데이터 스키마
// --------------------------------------------
/*
{ 
  id: String,
  name: String,
  email: String,
  phone: String,
  type: Int, // 1:관리자, 2:교수, 3:대학원생, 4:학부생
  dept: Int, // 1:컴공과, 2:기타학과
  noShow: Int, // 노쇼 카운트
  accessToken: String,
  refreshToken: String,
}
*/

// --------------------------------------------
// 3-2. 프론트엔드 데이터 예시
// --------------------------------------------
/*
{ 
  id: '1',
  name: '이원진',
  email: 'wjlee@example.com',
  phone: '010-1234-5678',
  type: 4, // 1:관리자, 2:교수, 3:대학원생, 4:학부생
  dept: 1, // 1:컴공과, 2:기타학과
  noShow: 0, // 노쇼 카운트
  accessToken: "aaa",
  refreshToken: "bbb",
}
*/
