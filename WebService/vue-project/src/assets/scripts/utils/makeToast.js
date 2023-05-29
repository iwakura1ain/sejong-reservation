import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default function makeToast(msg, type) {
	toast(msg, {
		autoClose: 3000,
		position: toast.POSITION.BOTTOM_RIGHT,
		transition: toast.TRANSITIONS.SLIDE,
		type: type,
	});
}
