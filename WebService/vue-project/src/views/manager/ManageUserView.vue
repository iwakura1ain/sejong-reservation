<template>
	<div id="manage-user-view">
		<manage-tool-header name="사용자 관리 " />
		<div>
			<!-- 엑셀로 사용자 추가 -->
			<div class="excel-register-container">
				<div style="text-align: left">
					<filled-button
						v-if="!enableExcelUpload"
						@click="toggleEnableExcelUpload(true)"
					>
						+ 엑셀로 사용자 추가
					</filled-button>
					<div
						v-if="enableExcelUpload"
						style="
							padding: 8px;
							border: 1px solid lightgrey;
							border-radius: 8px;
						"
					>
						<div>
							<filled-button
								color="white"
								style="margin-left: 0"
								@click="toggleEnableExcelUpload(false)"
							>
								취소
							</filled-button>
							<filled-button @click="registerFromExcel">전송하기</filled-button>
						</div>

						<input type="file" @change="uploadFile" style="height: 32px" />
					</div>
				</div>
			</div>

			<!-- 사용자 검색 -->
			<div style="display: flex; justify-content: center; margin-bottom: 24px">
				<div class="filter-container">
					<!-- 1행 -->
					<div class="field-row">
						<div class="field-set">
							<span class="field-label user-id">사용자ID</span>
							<text-input
								class="field-value text user-id"
								v-model="filter.userId"
							/>
						</div>
						<div class="field-set">
							<span class="field-label user-name">사용자이름</span>
							<text-input
								class="field-value text user-name"
								v-model="filter.userName"
							/>
						</div>
					</div>

					<!-- 2행 -->
					<div class="field-row">
						<div class="field-set">
							<span class="field-label email">이메일</span>
							<text-input
								class="field-value text email"
								v-model="filter.email"
							/>
						</div>
						<div class="field-set">
							<span class="field-label phone">전화번호</span>
							<digit-input
								class="field-value text phone"
								v-model="filter.phone"
							></digit-input>
						</div>
					</div>

					<!-- 3행 -->
					<div class="field-row">
						<div class="field-set">
							<span class="field-label dept">학과</span>
							<vue-select
								class="field-value select dept"
								v-model="filter.dept"
								:options="selectOptions.dept"
								placeholder="학과"
								:disabled="selectOptions.dept.length === 0"
							/>
						</div>

						<div class="field-set">
							<span class="field-label user-type">사용자유형</span>
							<vue-select
								class="field-value select user-type"
								v-model="filter.userType"
								:options="selectOptions.userType"
								placeholder="사용자유형"
								:disabled="selectOptions.userType.length === 0"
							/>
						</div>
					</div>

					<!-- 4행 -->
					<div class="field-row">
						<div class="field-set">
							<span class="field-label order-target">정렬기준</span>
							<vue-select
								class="field-value select order-target"
								v-model="filter.orderTarget"
								:options="selectOptions.orderTarget"
								placeholder="정렬기준"
								:disabled="selectOptions.orderTarget.length === 0"
							/>
						</div>

						<div class="field-set">
							<span class="field-label order-method">정렬순서</span>
							<vue-select
								class="field-value select order-method"
								v-model="filter.orderMethod"
								:options="selectOptions.orderMethod"
								placeholder="정렬순서"
								:disabled="selectOptions.orderMethod.length === 0"
							/>
						</div>
					</div>

					<div style="display: flex; align-items: center; margin-top: 8px">
						<p style="font-weight: bold">{{ userList.length }}건 조회</p>
						<div style="margin-left: auto">
							<!-- 조회버튼 -->
							<filled-button @click="fetchUserList" style="margin: 0">
								조회하기</filled-button
							>
						</div>
					</div>

					<!-- 현재사용자의 노쇼만 모아보기 -->
					<div v-if="userList.length > 0" style="margin-top: 24px">
						<div style="text-align: right">
							<text-button
								v-if="!onlyNoshow"
								@click="toggleOnlyNoshow"
								style="margin: 0"
							>
								노쇼 현황만 모아보기</text-button
							>
							<filled-button
								v-else
								color="white"
								@click="toggleOnlyNoshow"
								style="margin: 0"
								>전체 정보 보기</filled-button
							>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- 유저 목록 -->
		<div class="user-container-wrap">
			<div v-if="userList.length > 0" class="user-container">
				<template v-if="!onlyNoshow">
					<div class="user-item" v-for="user in userList" :key="user.id">
						<div class="default-view" style="margin-bottom: 24px">
							<span class="name">{{ user.name }}</span>
							<span class="dept-type">{{
								`${user.deptStr} ${user.typeStr}`
							}}</span>
						</div>
						<div class="detail-info">
							<p class="detail-item user-id">
								<span class="label">사용자ID</span>
								<span class="value">{{ user.id }}</span>
							</p>
							<p class="detail-item email">
								<span class="label">이메일</span>
								<span class="value">{{ user.email }}</span>
							</p>
							<p class="detail-item phone">
								<span class="label">전화번호</span>
								<span class="value">{{ user.phone }}</span>
							</p>
							<p class="detail-item noshow">
								<span class="label">노쇼횟수</span>
								<span class="value">{{ user.noShow }}회</span>
							</p>
						</div>
						<div class="user-tool-box">
							<div
								class="btns"
								v-if="!confirmResetPw && !confirmChangeType && !confirmDelete"
							>
								<text-button class="btn" @click="toggleConfirmResetPw(user.id)"
									>암호초기화</text-button
								>

								<text-button
									class="btn"
									@click="toggleConfirmChangeType(user.id)"
									>유형 수정</text-button
								>
								<text-button class="btn" @click="toggleConfirmDelete(user.id)"
									>삭제</text-button
								>
							</div>
							<div class="actions">
								<div v-if="confirmResetPw === user.id">
									<section-header style="padding: 0; margin: 12px 0" />
									<p>정말 초기화할까요?</p>
									<p>
										<span style="font-weight: bold">00000000</span>으로
										초기화됩니다.
									</p>
									<div>
										<text-button @click="toggleConfirmResetPw()"
											>취소</text-button
										>
										<filled-button @click="handleResetPw(user.id)"
											>초기화</filled-button
										>
									</div>
								</div>
								<div v-if="confirmChangeType === user.id">
									<vue-select
										style="width: 140px"
										v-model="nextUserType"
										:options="nextUserTypeOption"
										placeholder="사용자유형"
									/>
									<div>
										<text-button @click="toggleConfirmChangeType()"
											>취소</text-button
										>
										<filled-button @click="handleChangeType(user.id)"
											>유형 변경</filled-button
										>
									</div>
								</div>
								<div v-if="confirmDelete === user.id">
									<p style="color: red">
										사용자를 삭제합니다. 되돌릴 수 없습니다.
									</p>
									<div>
										<text-button @click="toggleConfirmDelete()"
											>취소</text-button
										>
										<filled-button @click="handleDelete(user.id)"
											>삭제</filled-button
										>
									</div>
								</div>
							</div>
						</div>
					</div>
				</template>
				<template v-else>
					<div class="user-item-onlynoshow">
						<div
							class="noshow-cell-container"
							style="background-color: #c2153f; color: white"
						>
							<div class="noshow-cell">사용자이름</div>
							<div class="noshow-cell">사용자 ID</div>
							<div class="noshow-cell">노쇼 횟수</div>
						</div>
						<div
							v-for="user in userList"
							:key="user.id"
							class="noshow-cell-container"
						>
							<div class="noshow-cell">{{ user.name }}</div>
							<div class="noshow-cell">{{ user.id }}</div>
							<div class="noshow-cell">{{ user.noShow }}</div>
						</div>
					</div>
				</template>
			</div>
			<div v-else>
				<empty-sign />
			</div>
		</div>
	</div>
</template>

<script setup>
import ManageToolHeader from '@/layouts/Manage/ManageToolHeader.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';

import { ref } from 'vue';
import EmptySign from '@/components/atoms/EmptySign.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import TextButton from '@/components/atoms/TextButton.vue';
import TextInput from '@/components/atoms/TextInput.vue';
import DigitInput from '@/components/atoms/DigitInput.vue';
import { userTokenStore } from '@/stores/userToken.js';
import { loadingStore } from '@/stores/loading.js';
import { userService } from '@/assets/scripts/requests/request.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';
import VueSelect from '@/components/wrappers/VueNextSelectWrapper.vue';

import { DEPT_TYPE, USER_TYPE } from '@/assets/constants.js';

// 폼 유지 관련 -----------------------------
const filter = ref({
	userId: '',
	userName: '',
	email: '',
	phone: '',
	dept: '전체',
	userType: '전체',
	orderTarget: '정렬안함',
	orderMethod: '',
});

const selectOptions = ref({
	dept: ['전체', '컴퓨터공학과', '기타학과'],
	userType: ['전체', '관리자', '교수', '대학원생', '학부생'],
	orderTarget: ['정렬안함', '노쇼횟수', '사용자ID'],
	orderMethod: ['오름차순', '내림차순'],
});

// 유저 불러오기, 필터링
const userList = ref([]);

function getUserTypeStr(type) {
	if (type === USER_TYPE.ADMIN) {
		return '관리자';
	} else if (type === USER_TYPE.PROFESSOR) {
		return '교수';
	} else if (type === USER_TYPE.GRAD_STUDENT) {
		return '대학원생';
	} else if (type === USER_TYPE.UNDER_GRAD_STUDENT) {
		return '학부생';
	} else {
		console.error('사용자 유형이 올바르지 않습니다.');
		return 'X';
	}
}

function getUserDeptStr(dept) {
	if (dept === DEPT_TYPE.COMPUTER) {
		return '컴퓨터공학과';
	} else if (dept === DEPT_TYPE.OTHERS) {
		return '기타학과';
	} else {
		console.error('학과 유형이 올바르지 않습니다.');
		return 'X';
	}
}

function filterUsers(_users) {
	let users = _users;
	if (filter.value.dept != '전체') {
		users = users.filter(user => user.deptStr === filter.value.dept);
	}
	if (filter.value.userType != '전체') {
		users = users.filter(user => user.typeStr === filter.value.userType);
	}
	if (filter.value.userId) {
		users = users.filter(user => user.id.includes(filter.value.userId));
	}
	if (filter.value.userName) {
		users = users.filter(user => user.name.includes(filter.value.userName));
	}
	if (filter.value.email) {
		users = users.filter(user => user.email.includes(filter.value.email));
	}
	if (filter.value.phone) {
		users = users.filter(user => user.phone.includes(filter.value.phone));
	}
	return users;
}

async function fetchUserList() {
	try {
		loadingStore.start();

		// 유저 데이터 가져오기
		const accessToken = userTokenStore.getAccessToken();
		const res = await userService.getAll(accessToken);
		if (!res.status) {
			console.error(res);
			throw new Error(res);
		}

		// 사용자 유형, 학과코드 문자열로 변환
		const data = res.data;
		data.forEach(user => {
			user.deptStr = getUserDeptStr(user.dept);
			user.typeStr = getUserTypeStr(user.type);
		});

		// 필터링
		const filteredData = filterUsers(data);

		// 정렬
		if (filter.value.orderTarget === '사용자ID') {
			if (filter.value.orderMethod === '오름차순') {
				filteredData.sort((a, b) => a.id - b.id);
			} else if (filter.value.orderMethod === '내림차순') {
				filteredData.sort((a, b) => b.id - a.id);
			}
		} else if (filter.value.orderTarget === '노쇼횟수') {
			if (filter.value.orderMethod === '오름차순') {
				filteredData.sort((a, b) => a.noShow - b.noShow);
			} else if (filter.value.orderMethod === '내림차순') {
				filteredData.sort((a, b) => b.noShow - a.noShow);
			}
		}

		userList.value = filteredData;
		console.log(userList.value);
	} catch (err) {
		const msg = err.msg;
		if (msg === 'Token has expired') {
			makeToast('로그인정보가 올바르지 않습니다(Token has expired)', 'error');
		} else {
			makeToast('알 수 없는 오류입니다', 'error');
		}
	} finally {
		loadingStore.stop();
	}
}

// 노쇼테이블 작업
const onlyNoshow = ref(false);
function toggleOnlyNoshow() {
	onlyNoshow.value = !onlyNoshow.value;
}

// 유저 작업
const confirmResetPw = ref(0);
const confirmChangeType = ref(0);
const confirmDelete = ref(0);
const nextUserType = ref('');
const nextUserTypeOption = ['관리자', '교수', '대학원생', '학부생'];
function toggleConfirmResetPw(id = 0) {
	confirmResetPw.value = id;
}
function toggleConfirmChangeType(id = 0) {
	confirmChangeType.value = id;
}
function toggleConfirmDelete(id = 0) {
	confirmDelete.value = id;
}

async function handleResetPw(id) {
	try {
		loadingStore.start();
		const accessToken = userTokenStore.getAccessToken();
		const res = await userService.update(
			id,
			{ password: '00000000' },
			accessToken,
		);
		if (!res.status) {
			console.error(res);
			throw new Error(res);
		}
		makeToast('초기화가 완료되었습니다', 'info');
		fetchUserList();
		toggleConfirmResetPw();
	} catch (err) {
		console.error(err);
		makeToast('오류가 발생했습니다', 'error');
	} finally {
		loadingStore.stop();
	}
}

async function handleChangeType(id) {
	try {
		loadingStore.start();

		let codeType = 0;
		if (nextUserType.value === '관리자') {
			codeType = 1;
		} else if (nextUserType.value === '교수') {
			codeType = 2;
		} else if (nextUserType.value === '대학원생') {
			codeType = 3;
		} else if (nextUserType.value === '학부생') {
			codeType = 4;
		}

		const accessToken = userTokenStore.getAccessToken();
		const res = await userService.update(id, { type: codeType }, accessToken);
		if (!res.status) {
			console.error(res);
			throw new Error(res);
		}

		makeToast('수정이 완료되었습니다', 'info');
		fetchUserList();
		toggleConfirmChangeType();
	} catch (err) {
		console.error(err);
		makeToast('오류가 발생했습니다', 'error');
	} finally {
		loadingStore.stop();
	}
}

async function handleDelete(id) {
	try {
		loadingStore.start();
		const accessToken = userTokenStore.getAccessToken();
		const res = await userService.delete(id, accessToken);
		if (!res.status) {
			console.error(res);
			throw new Error(res);
		}
		makeToast('삭제가 완료되었습니다', 'info');
		fetchUserList();
		toggleConfirmDelete();
	} catch (err) {
		console.error(err);
		makeToast('오류가 발생했습니다', 'error');
	} finally {
		loadingStore.stop();
	}
}

// 엑셀로 회원가입하기
const enableExcelUpload = ref(false);
const file = ref(null);

function toggleEnableExcelUpload(s) {
	enableExcelUpload.value = s;
}
function uploadFile(event) {
	file.value = event.target.files[0];
}
async function registerFromExcel() {
	try {
		loadingStore.start();
		if (file.value === null) {
			makeToast('엑셀파일이 없습니다', 'warning');
			return;
		}
		const _formdata = new FormData();
		_formdata.append('file', file.value);

		const accessToken = userTokenStore.getAccessToken();
		const res = await userService.registerFromExcel(_formdata, accessToken);
		if (!res.status) {
			console.error(res);
			throw new Error(res);
		}
		makeToast('전송이 완료되었습니다', 'info');
		fetchUserList();
		toggleEnableExcelUpload(false);
	} catch (err) {
		console.error(err);
		makeToast('오류가 발생했습니다', 'error');
	} finally {
		loadingStore.stop();
	}
}

// 초기화
async function init() {
	await fetchUserList();
}
init();
</script>

<style lang="scss" scoped>
#manage-user-view {
	width: 100%;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.excel-register-container {
	margin-bottom: 48px;
}
.filter-container {
	width: fit-content;
	.field-row {
		display: flex;
		flex-wrap: wrap;
		width: 100%;

		.field-set {
			width: 260px;
			// flex: 1;
			display: flex;
			align-items: center;
			justify-content: flex-end;
			margin: 8px;
			// width: 100%;
			.field-label {
				display: block;
				margin-right: 4px;
				word-break: keep-all;
				word-wrap: normal;
			}
			.field-value.select,
			.field-value.text {
				width: 180px;
			}
			.datepicker-container {
				display: flex;
			}
		}
	}
}

.user-container {
	word-break: break-all;

	.user-item {
		transition: all 0.2s;
		border: 1px solid lightgrey;
		padding: 24px 48px;
		border-radius: $box-radius;
		margin: 24px 0;
		box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);
		-webkit-box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);
		-moz-box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);
		.default-view {
			display: flex;
			flex-wrap: wrap;
			align-items: flex-end;
			.name {
				font-size: 1.2rem;
				font-weight: bold;
				margin-right: 4px;
			}
			.dept-type {
			}
		}
		.detail-info {
			margin: 4px 0;
			.label {
				font-weight: bold;
				margin-right: 4px;
				font-size: 0.9rem;
			}
			.value {
				font-size: 0.9rem;
			}
		}
		.user-tool-box {
			margin-top: 24px;
			.btns {
				display: flex;
				justify-content: center;
			}
			.btns .btn {
				margin: 2px;
			}

			.actions > div {
				display: flex;
				flex-direction: column;
				align-items: center;
			}
		}
	}

	.user-item:hover {
		border: 1px solid $sejong-red;
		// background-color: rgb(255, 222, 222);
		transform: translateY(-5px);
	}

	//

	.user-item-onlynoshow {
		border: 1px solid lightgrey;
		// width: 100%;
		.noshow-cell-container {
			display: flex;
			.noshow-cell {
				width: 200px;
				text-align: center;
				padding: 8px;
				border: 1px solid lightgrey;
			}
		}
	}
}

@media (max-width: 650px) {
	.filter-container {
		.field-row {
			flex-direction: column;

			.field-set {
				// width: 100%;
				margin: 8px 0;

				.field-value.select,
				.field-value.text {
					width: 140px;
				}
			}

			.datepicker-field-set {
				display: flex;
				flex-direction: column;
				align-items: flex-start !important;
				.field-label {
					margin-bottom: 4px !important;
				}
				.datepicker-container {
					flex-direction: column;
					.date-after {
						margin-right: 0;
					}
					.date-before {
						margin-top: 8px;
						margin-left: 4px;
					}

					.date-after,
					.date-before {
						max-width: 160px;
					}
				}
			}
		}
	}

	.user-container-wrap {
		width: 100%;

		.user-container {
			width: 100%;
			.user-item {
				padding: 16px 0;
				width: 100%;
				display: flex;
				flex-direction: column;
				align-items: center;

				.default-view {
					flex-direction: column;
					align-items: center;
				}
			}
		}
	}
}

@media (max-width: 320px) {
	.user-item-onlynoshow {
		.noshow-cell-container {
			.noshow-cell {
				font-size: 0.8rem;
			}
		}
	}
}
</style>
