// localstorage상에서 access token, refresh token을 관리합니다.

// vue reactive객체가 아니기 때문에 사실 store가 아니기는 한데,
// 전역 공유데이터라는 점에서 다른 store들과 그 특성이 다를바 없어보여서 그냥 store취급하기로 했습니다.

export const userTokenStore = {
	// clear
	clear: function () {
		// 토큰 삭제
		localStorage.removeItem('SEJONG_RESERVATION_ACCESSTOKEN');
		localStorage.removeItem('SEJONG_RESERVATION_REFRESHTOKEN');
	},

	// exist
	exist: function () {
		const { accessToken, refreshToken } = this.get();
		if (!accessToken || !refreshToken) {
			return false;
		}
		return true;
	},

	// set
	setAccessToken: function (accessToken) {
		if (accessToken) {
			localStorage.setItem('SEJONG_RESERVATION_ACCESSTOKEN', accessToken);
		} else {
			console.error('[set거부]유효하지 않은 accessToken : ', accessToken);
		}
	},
	setRefreshToken: function (refreshToken) {
		if (refreshToken) {
			localStorage.setItem('SEJONG_RESERVATION_REFRESHTOKEN', refreshToken);
		} else {
			console.error('[set거부]유효하지 않은 refreshToken : ', refreshToken);
		}
	},
	set: function ({ accessToken, refreshToken }) {
		this.setAccessToken(accessToken);
		this.setRefreshToken(refreshToken);
	},

	// get
	getAccessToken: function () {
		const accessToken = localStorage.getItem('SEJONG_RESERVATION_ACCESSTOKEN');
		return accessToken;
	},
	getRefreshToken: function () {
		const refreshToken = localStorage.getItem(
			'SEJONG_RESERVATION_REFRESHTOKEN',
		);
		return refreshToken;
	},
	get: function () {
		return {
			accessToken: this.getAccessToken(),
			refreshToken: this.getRefreshToken(),
		};
	},
};

// item은 두 개입니다.
// 1) 'SEJONG_RESERVATION_ACCESSTOKEN'
// 2) 'SEJONG_RESERVATION_REFRESHTOKEN'
