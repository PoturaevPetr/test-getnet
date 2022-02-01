<template>
	<div class="app">
		<nav class="navbar">
			<h3>Личный кабинет</h3>
			<div class="links">
				<button type="button" class="btn btn-danger" @click="Exit">Выйти</button>
			</div>
		</nav>
		<div class="container">
			<div class="text-center ">
				<ul class="links row text-center d-flex flex-fill">
					<li class="col list-group-item">
						<router-link to='/Room/profile'>Профиль</router-link>
					</li>
					<li class="col list-group-item">
						<router-link to="/Room/history">Платежи</router-link>
					</li>
					<li class="col list-group-item">
						<router-link to="/Room/finance">Баланс</router-link>
					</li>
					<li class="col list-group-item">
						<router-link to="/Room/services">Услуги</router-link>
					</li>
				</ul>
			</div>
		</div>
		<router-view/>
	</div>
</template>

<script>
import axios from 'axios'
import router from "../router.js";

export default {
	signup: () => {
		router.push({ name: "Autorisation" });
	},
	Exit() {
		const path = 'http://localhost:5000/Exit'
		axios.get(path)
			.then(() => {
				router.push({ name: "Autorisation" });
			})
	}

};
</script>
<style>
.links {
	margin: 0 0 0 0;
}
</style>