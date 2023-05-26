// 입력으로 n을 넣으면 [1,2,3,4,5,....,n-1] 배열을 뱉습니다.

export default function generateRange(n) {
	var arr = [];
	for (var i = 0; i < n; i++) {
		arr.push(i);
	}
	return arr;
}
