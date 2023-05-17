<template>
	<div id="register-view">
		<section-header>회원가입</section-header>

		<main>
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
						<radio-group
							v-model="formdata.usertype"
							:buttons="radioButton.usertype"
						/>
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
						<text-input type="password" v-model="formdata.pw"></text-input>
					</div>
					<div class="field-set">
						<span class="label">비밀번호 확인</span>
						<text-input
							type="password"
							v-model="formdata.pwConfirm"
						></text-input>
					</div>
					<div class="field-set">
						<span class="label">이메일</span>
						<text-input v-model="formdata.email"></text-input>
					</div>

					<div style="width: 100%">
						<filled-button class="btn signin" @click="register"
							>가입하기</filled-button
						>
					</div>
				</form>
			</div>
		</main>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import LogoImgRed from '@/assets/images/logo_red.png';
import TextInput from '@/components/atoms/TextInput.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import RadioGroup from '@/components/RadioGroup.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';

const formdata = ref({
	name: '',
	usertype: -1,
	dept: 0,
	id: '',
	pw: '',
	pwConfirm: '',
	email: '',
});
// 관리자 1
const radioButton = {
	usertype: [
		{ text: '학부생', value: 4 },
		{ text: '대학원생', value: 3 },
		{ text: '교수', value: 2 },
	],
	dept: [
		{ text: '컴퓨터공학과', value: 1 },
		{ text: '기타 학과', value: 2 },
	],
};
</script>

<style lang="scss" scoped>
#register-view {
	background: linear-gradient(
		rgba(255, 255, 255, 1),
		rgba(255, 255, 255, 1),
		rgba(195, 0, 47, 0.2)
	);
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
</style>
