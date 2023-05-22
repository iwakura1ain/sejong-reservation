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
				<text-input class="content" v-model="name"></text-input>
			</div>
			<div class="field-set email">
				<span class="label">이메일</span>
				<text-input class="content" v-model="email"></text-input>
			</div>
			<div class="field-set dept">
				<span class="label">학과</span>
				<radio-group class="content" v-model="dept" :buttons="deptRadios" />
			</div>

			<div class="pw-toggle-btn">
				<span class="label">비밀번호</span>
				<div v-if="!pwChangeEnabled">
					<filled-button @click="togglePwChange">변경하기</filled-button>
				</div>
				<div v-else>
					<filled-button @click="togglePwChange" color="white"
						>변경하지 않기</filled-button
					>
				</div>
			</div>
			<div class="password-container">
				<div v-if="pwChangeEnabled">
					<div class="field-set">
						<span class="label">현재 비밀번호</span>
						<text-input class="content" v-model="currentPw"></text-input>
					</div>
					<div class="field-set">
						<span class="label">새 비밀번호 입력</span>
						<text-input class="content" v-model="newPw"></text-input>
					</div>
					<div class="field-set">
						<span class="label">새 비밀번호 확인</span>
						<text-input class="content" v-model="newPwConfirm"></text-input>
					</div>
				</div>
			</div>

			<section-header></section-header>

			<div class="btn-wrap">
				<filled-button class="submit-btn" @click="submit">
					수정하기
				</filled-button>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import TextInput from '@/components/atoms/TextInput.vue';
import RadioGroup from '@/components/RadioGroup.vue';
import { userStore } from '@/stores/user.js';

// shared state
const userInfo = userStore.getInfo();

// local states
const name = ref(userInfo.name);
const email = ref(userInfo.email);
const dept = ref(userInfo.dept);

const pwChangeEnabled = ref(false); // 패스워드 변경을 할지 말지. (true : 한다, false : 안한다)
const currentPw = ref('');
const newPw = ref('');
const newPwConfirm = ref('');
function togglePwChange() {
	pwChangeEnabled.value = !pwChangeEnabled.value;
}

// normal variables
const deptRadios = [
	{ text: '컴퓨터공학과', value: 1 },
	{ text: '기타 학과', value: 2 },
];

// handlers
function submit() {
	alert('submitted');
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
