<template>
	<div id="register-view">
		<section-header>회원가입</section-header>
		<main v-if="submitted" class="after-submit">
			<img :src="doorIcon" alt="열린 문" />
			<p>가입이 완료되었습니다</p>

			<filled-button class="btn go-login" @click="handleGoLoginView"
				>로그인 화면으로 가기</filled-button
			>
		</main>
		<main v-else class="before-submit">
			<article class="logo-container">
				<img class="logoimg" :src="LogoImgRed" alt="sejong univ. logo" />
				<h1 class="logotext-ko">회의실 예약 시스템</h1>
				<h2 class="logotext-en">Meeting Room Reservation System</h2>
			</article>

			<div class="form-container">
				<div>
					<router-link to="/login">
						<filled-button class="btn signup" color="white">
							돌아가기
						</filled-button>
					</router-link>
				</div>
				<form>
					<div class="field-set">
						<span class="label">이름</span>
						<text-input v-model="formdata.name"></text-input>
					</div>
					<div class="field-set">
						<span class="label">사용자 구분</span>
						<radio-group v-model="formdata.type" :buttons="radioButton.type" />
					</div>
					<div class="field-set">
						<span class="label">학과</span>
						<radio-group v-model="formdata.dept" :buttons="radioButton.dept" />
					</div>
					<div class="field-set">
						<span class="label">학번(직번)</span>
						<text-input v-model="formdata.id"></text-input>
					</div>
					<div class="field-set">
						<span class="label">비밀번호</span>
						<text-input
							type="password"
							v-model="formdata.password"
						></text-input>
					</div>
					<div class="field-set">
						<span class="label">비밀번호 확인</span>
						<text-input
							type="password"
							v-model="formdata.passwordConfirm"
						></text-input>
					</div>
					<div class="field-set">
						<span class="label">이메일</span>
						<text-input v-model="formdata.email"></text-input>
					</div>
					<div class="field-set">
						<span class="label">휴대전화번호</span>
						<digit-input v-model="formdata.phone"></digit-input>
					</div>

					<div style="width: 100%">
						<filled-button class="btn signin" @click="handleSubmit">
							가입하기
						</filled-button>
					</div>
				</form>
			</div>
		</main>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import LogoImgRed from '@/assets/images/logo_red.png';
import doorIcon from '@/assets/images/icons/door.png';

import TextInput from '@/components/atoms/TextInput.vue';
import DigitInput from '@/components/atoms/DigitInput.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import RadioGroup from '@/components/RadioGroup.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import makeToast from '@/assets/scripts/utils/makeToast.js';

import { userService } from '@/assets/scripts/requests/request.js';
import { loadingStore } from '@/stores/loading.js';

// 상태 ----------------------------------
const formdataTemplate = {
	name: '',
	type: 4,
	dept: 1,
	id: '',
	password: '',
	passwordConfirm: '',
	email: '',
	phone: '',
};
const formdata = ref(formdataTemplate);

const submitted = ref(false);

// 초기화 ---------------------------------
const router = useRouter();
const radioButton = {
	type: [
		{ text: '학부생', value: 4 },
		{ text: '대학원생', value: 3 },
		{ text: '교수', value: 2 },
	],
	dept: [
		{ text: '컴퓨터공학과', value: 1 },
		{ text: '기타 학과', value: 2 },
	],
};

// 일반함수 -------------------------
function validateForm(req) {
	let flag = true; // 검증통과여부 (true:통과, false:불통)
	if (
		!req.name ||
		!req.id ||
		!req.password ||
		!req.passwordConfirm ||
		!req.email
	) {
		makeToast('빈 항목이 있습니다', 'warning');
		flag = false;
	}
	if (!(1 <= req.dept && req.dept <= 2)) {
		makeToast('학과의 선택값이 올바르지 않습니다', 'warning');
		flag = false;
	}
	if (!(2 <= req.type && req.type <= 4)) {
		makeToast('사용자 구분의 선택값이 올바르지 않습니다', 'warning');
		flag = false;
	}
	if (req.password !== req.passwordConfirm) {
		makeToast('비밀번호와 비밀번호 확인이 일치하지 않습니다.', 'warning');
		flag = false;
	}
	if (!req.email.includes('@')) {
		makeToast('이메일의 형식이 올바르지 않습니다', 'warning');
		flag = false;
	}

	return flag;
}

// 이벤트핸들러 ----------------------
async function handleSubmit() {
	try {
		loadingStore.start();

		const req = { ...formdata.value };
		if (!validateForm(req)) {
			return;
		}

		// 통신
		const res = await userService.register(req);
		if (!res.status) {
			if (res.msg) throw new Error(res.msg);
			else throw new Error(res);
		}

		// 완료
		submitted.value = true;
		formdata.value = formdataTemplate;
		location.href = location.href + '#app';
		// ------------------------------
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);

		if (msg === 'User Exists') {
			makeToast('이미 가입된 학번(직번)입니다', 'error');
		} else {
			makeToast('예기치 못한 오류가 발생했습니다.', 'error');
		}
	} finally {
		loadingStore.stop();
	}
}

function handleGoLoginView() {
	router.push({ name: 'Login' });
}
</script>

<style lang="scss" scoped>
#register-view {
	// background: linear-gradient(
	// 	rgba(255, 255, 255, 1),
	// 	rgba(255, 255, 255, 1),
	// 	rgba(195, 0, 47, 0.2)
	// );
	background-size: cover;
	main {
		padding: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		flex-direction: row;
		width: 100%;

		.logo-container {
			flex: 1;
			text-align: center;
			font-weight: bold;
			.logoimg {
				width: 196px;
				height: 196px;
			}
			.logotext-ko {
				color: $sejong-grey;
				font-size: 2rem;
				margin: 8px 0;
			}
			.logotext-en {
				color: $sejong-red;
				font-size: 1rem;
			}
		}

		.form-container {
			background-color: white;
			padding: 48px;
			margin-top: 48px;
			border: 1px solid lightgrey;
			border-radius: $box-radius;

			form {
				display: flex;
				flex-direction: column;
				align-items: flex-end;
				margin-top: 24px;
				.field-set {
					margin: 12px 0;
					display: flex;
					align-items: center;
					.label {
						margin-right: 8px;
					}
				}

				.btn {
					// width: 98px;
					text-align: center;
					width: 100%;
					margin: 0;
					margin-top: 16px;
				}
			}
		}
	}
}

@media (max-width: 768px) {
	#register-view {
		main {
			flex-direction: column;

			.logo-container {
				transform: scale(0.7);
			}
			.label {
				font-size: 0.85rem;
			}
			.form-container {
				width: 100%;
				padding: 12px;
			}
		}
	}
}

@media (max-width: 320px) {
	#register-view {
		main {
			.logo-container {
				transform: scale(0.6);
				.logotext-ko {
					font-size: 1.6rem;
				}
				.logotext-en {
					font-size: 0.85rem;
				}
			}
			.form-container {
				form {
					align-items: center;
					.field-set {
						flex-direction: column;
						align-items: center;
						.label {
							margin-bottom: 4px;
						}
					}
				}
			}
		}
	}
}

// --------------

#register-view {
	.after-submit {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 50vh;
		p {
			font-size: 2rem;
			margin: 24px 0;
		}
		.btn {
			margin-top: 48px;
		}
	}

	@media (max-width: 768px) {
		.after-submit {
			p {
				font-size: 1.5rem;
			}
			img {
				width: 128px;
				height: 128px;
			}
		}
	}
}
</style>
