<template>
	<div id="user-edit-profile-view">
		<section-header>내 정보 수정</section-header>

		<form>
			<div class="btn-wrap">
				<router-link to="/mypage">
					<filled-button class="go-mypage-btn" color="white">
						돌아가기
					</filled-button>
				</router-link>
			</div>
			<section-header></section-header>

			<div class="field-set name">
				<span class="label">이름</span>
				<text-input class="content" v-model="formdata.name"></text-input>
			</div>
			<div class="field-set email">
				<span class="label">이메일</span>
				<text-input class="content" v-model="formdata.email"></text-input>
			</div>
			<div class="field-set phone">
				<span class="label">전화</span>
				<digit-input class="content" v-model="formdata.phone"></digit-input>
			</div>
			<div class="field-set dept">
				<span class="label">학과</span>
				<radio-group
					class="content"
					v-model="formdata.dept"
					:buttons="deptRadios"
				/>
			</div>

			<div class="pw-toggle-btn">
				<span class="label">비밀번호</span>
				<div v-if="!formdata.pwChangeEnabled">
					<filled-button @click="togglePwChange">변경하기</filled-button>
				</div>
				<div v-else>
					<filled-button @click="togglePwChange" color="white">
						변경하지 않기
					</filled-button>
				</div>
			</div>
			<div class="password-container">
				<div v-if="formdata.pwChangeEnabled">
					<div class="field-set">
						<span class="label">현재 비밀번호</span>
						<text-input
							class="content"
							type="password"
							v-model="formdata.curPw"
						></text-input>
					</div>
					<div class="field-set">
						<span class="label">새 비밀번호 입력</span>
						<text-input
							class="content"
							type="password"
							v-model="formdata.newPw"
						></text-input>
					</div>
					<div class="field-set">
						<span class="label">새 비밀번호 확인</span>
						<text-input
							class="content"
							type="password"
							v-model="formdata.newPwConfirm"
						></text-input>
					</div>
				</div>
			</div>

			<section-header></section-header>

			<div class="btn-wrap">
				<filled-button class="submit-btn" @click="handleSubmit">
					수정하기
				</filled-button>
			</div>
		</form>
	</div>
</template>

<script setup>
import { watch, reactive } from 'vue';
import { useRouter } from 'vue-router';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import TextInput from '@/components/atoms/TextInput.vue';
import RadioGroup from '@/components/RadioGroup.vue';
import DigitInput from '@/components/atoms/DigitInput.vue';
import { userInfoStore, userIsLogin } from '@/stores/userInfo.js';
import { userTokenStore } from '@/stores/userToken.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';
import { userService } from '@/assets/scripts/requests/request.js';

const router = useRouter();
// local states
const userInfo = userInfoStore.get();
const formdata = reactive({
	name: userInfo.name,
	email: userInfo.email,
	phone: userInfo.phone,
	dept: userInfo.dept,

	pwChangeEnabled: false,
	curPw: '',
	newPw: '',
	newPwConfirm: '',
});

// 상태감시
watch(userIsLogin, () => {
	if (userIsLogin) {
		const userInfo = userInfoStore.get();
		formdata.name = userInfo.name;
		formdata.email = userInfo.email;
		formdata.phone = userInfo.phone;
		formdata.dept = userInfo.dept;
		console.log('hi', userIsLogin);
	}
});

const deptRadios = [
	{ text: '컴퓨터공학과', value: 1 },
	{ text: '기타 학과', value: 2 },
];

// 이벤트 핸들러
function togglePwChange() {
	formdata.pwChangeEnabled = !formdata.pwChangeEnabled;
}

async function handleSubmit() {
	try {
		if (!validateForm(formdata)) return;

		const infoReq = {
			username: formdata.name,
			email: formdata.email,
			phone: formdata.phone,
			dept: formdata.dept,
		};
		const pwReq = {
			current_pasword: formdata.curPw,
			new_password: formdata.newPw,
		};

		const infoRes = await userService.update(
			userInfo.id,
			infoReq,
			userTokenStore.getAccessToken(),
		);
		if (!infoRes.status) {
			if (infoRes.msg) throw new Error(infoRes.msg);
			else throw new Error(infoRes);
		}

		// const pwReq = await userService.changePassword();
		// if (!pwReq.status) {
		// 	if (pwReq.msg) throw new Error(pwReq.msg);
		// 	else throw new Error(pwReq);
		// }

		router.push({ name: 'UserMyPage', state: { userPorfileUpdated: true } });
	} catch (err) {
		console.error(err);
	}
}

// 일반함수
function validateForm(formdata) {
	let flag = true; // 검증통과여부 (true:통과, false:불통)
	if (!formdata.name || !formdata.email || !formdata.phone) {
		makeToast('빈 항목이 있습니다', 'warning');
		flag = false;
	}
	if (
		formdata.pwChangeEnabled &&
		(!formdata.curPw || !formdata.newPw || !formdata.newPwConfirm)
	) {
		makeToast('빈 항목이 있습니다', 'warning');
		flag = false;
	}

	if (!(1 <= formdata.dept && formdata.dept <= 2)) {
		makeToast('학과의 선택값이 올바르지 않습니다', 'warning');
		flag = false;
	}
	if (formdata.newPw !== formdata.newPwConfirm) {
		makeToast('비밀번호와 비밀번호 확인이 일치하지 않습니다.', 'warning');
		flag = false;
	}
	if (!formdata.email.includes('@')) {
		makeToast('이메일의 형식이 올바르지 않습니다', 'warning');
		flag = false;
	}

	return flag;
}
</script>

<style lang="scss" scoped>
#user-edit-profile-view {
	form {
		.field-set,
		.password-container {
			display: flex;
			align-items: center;
			margin-bottom: 8px;
		}

		.field-set {
			flex-wrap: wrap;
			.label {
				margin-right: 8px;
			}
			.content {
				flex: 1;
			}
		}

		.pw-toggle-btn {
			display: flex;
			flex-wrap: wrap;
			align-items: center;
			margin-bottom: 8px;

			margin-top: 32px;
		}

		.submit-btn {
			margin: 0;
			width: 100%;
			text-align: center;
		}
	}

	.btn-wrap {
		width: 100%;
	}
}

@media (max-width: 320px) {
	#user-edit-profile {
		form {
			.field-set {
				.label {
					margin-bottom: 4px;
				}
			}
		}
	}
}
</style>
