<template>
	<div class="room-card" :class="{ selected: selected }">
		<div class="info-container">
			<img class="room-img" :src="contents.img" alt="회의실 사진" />
			<div>
				<span class="room-address">{{
					`${contents.address1} ${contents.address2}`
				}}</span>
				<!-- <span class="room-address2">{{ contents.address2 }}</span> -->
				<span class="room-name">{{ contents.name }}</span>
				<div class="max-user">
					<img class="icon" :src="groupIcon" alt="최대 수용인원" />
					<span class="value">{{ contents.maxUsers }}명</span>
				</div>
				<div class="opening-hour">
					<img class="icon" :src="clockIcon" alt="개방시간" />
					<span class="value">
						{{ contents.time.open }}
						─ {{ contents.time.close }}
					</span>
				</div>
				<filled-button class="select-room-btn" @click="selectRoom">
					선택
				</filled-button>
			</div>
		</div>
		<div class="reservation-viewer">
			<!--  -->
		</div>
	</div>
</template>

<script setup>
import FilledButton from '@/components/atoms/FilledButton.vue';
import groupIcon from '@/assets/images/icons/group.png';
import clockIcon from '@/assets/images/icons/time.png';

const props = defineProps({
	contents: {
		required: false,
		type: [Object, null],
	},
	selected: {
		required: false,
		type: Boolean,
		default: false,
	},
});

const emit = defineEmits(['update-selected-room']);

function selectRoom() {
	emit('update-selected-room', props.contents.id);
}
</script>

<style lang="scss" scoped>
.room-card {
	margin: 12px;
	padding: 24px;

	background-color: white;
	border-radius: $box-radius;

	box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);
	-webkit-box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);
	-moz-box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);

	.info-container {
		display: flex;
		align-items: flex-end;
		.room-img {
			width: 192px;
			height: 192px;
			border-radius: $box-radius;
			object-fit: cover;
		}

		> div {
			display: flex;
			flex-direction: column;
			justify-content: center;
			padding-left: 12px;

			.icon {
				vertical-align: middle;
				display: inline-block;
				height: 24px;
				width: auto;
				margin-right: 8px;
			}

			.room-address {
				display: block;
				font-weight: bold;
			}
			.room-name {
				display: block;
				font-size: 1.6rem;
				padding: 12px 0;
			}
			.opening-hour {
				margin: 8px 0;
			}

			.max-user,
			.opening-hour {
				display: flex;
				align-items: center;
			}

			.select-room-btn {
				text-align: center;
				margin: 0;
				margin-top: 8px;
			}
		}
	}
}

.room-card.selected {
	border: 2px solid $sejong-red;
	.info-container {
		filter: opacity(50%);
	}
}

@media (max-width: 768px) {
	.room-card {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		margin: 12px 0;
		border: 2px solid white;
		.info-container {
			flex-direction: column;
			align-items: center;
			.room-img {
				width: 160px;
				height: 160px;
				margin-bottom: 24px;
			}
		}
	}
}
</style>
