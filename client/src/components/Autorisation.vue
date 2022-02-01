<template>
	<div class="app">
		<nav class="navbar">
			<h3>Здесь будет название проекта</h3>
			<div class="links">
				<button type="button" class="btn btn-light" @click="showModalLogin">Вход</button>
				<button type="button" class="btn btn-light" @click="showModalRegister">Регистрация</button>
			</div>
		</nav>
		<div class="container">
			<div class="row text-center justify-content-center">
				<div class="d-flex flex-column">
					<div  class="p-2">
						<h1 class="title">Добро пожаловать в "название проекта"</h1>
					</div>
					<div class="p-2">
						<h4 class="site-description">Здесь будет описание сайта</h4>
					</div>
					<div class="p-2">
						<button type="button" class="btn btn-success" @click="showModalLogin">Вход</button>
						<button type="button" class="btn btn-warning" @click="showModalRegister">Регистрация</button>
					</div>
				</div>
			</div>
		</div>
		<b-modal ref="modal-login" hide-footer title="Вход">
			<alert v-if="message" :message="message"></alert>
			<div class="container">
				<div class="row justify-content-center">
					<div>
						<div>
							<label for="name" class="cols-sm-2 control-label">Логин </label> 
						</div>
						<div>
							<input type="text" name="login" v-model="LoginData.login" placeholder="Введите ваш логин">
						</div>
						<div>
							<label for="pass1">Пароль</label>
						</div>
						<div>
							<input type="password" name="pass1" v-model="LoginData.password" placeholder="Введите пароль">
						</div>
						<div>
							<label class="custom-control custom-checkbox custom-control-inline"><input type="checkbox" class="custom-control-input" v-model="LoginData.remember"><span class="custom-control-label">Remember me</span></label> 
						</div>
						<div class="p-2 text-center">
							<button tupe="button" class="btn btn-success" @click="Login">Войти</button>
							<button tupe="submit" class="btn btn-warning" @click="hideModalLogin">Отмена</button>
						</div>
					</div>
				</div>
			</div>
		</b-modal>
		<b-modal ref="modal-register" title="Регистрация" hide-footer>
			<alert v-if="message" :message="message"></alert>
			<div class="container">
				<div class="row justify-content-center">
					<div>
						<div>
							<label for="name" class="cols-sm-2 control-label">ФИО </label> 
						</div>
						<div>
							<input type="text" name="login" v-model="RegisterData.name" placeholder="Введите ваши ФИО">
						</div>
						<div>
							<label for="login" class="cols-sm-2 control-label">Логин </label> 
						</div>
						<div>
							<input type="login" name="login" v-model="RegisterData.login" placeholder="Введите ваш логин">
						</div>
						<div>
							<label for="email">E-mail </label> 
						</div>
						<div>
							<input type="text" name="email" v-model="RegisterData.email" placeholder="Введите ваш E-mai">
						</div>
						<div>
							<label for="pass1">Пароль </label>
						</div>
						<div>
							<input type="password" name="pass1" v-model="RegisterData.password1" placeholder="Введите пароль">
						</div>
						<div>
							<label fo="pass2">Повторите пароль </label> 
						</div>
						<div>
							<input type="password" name="pass2" v-model="RegisterData.password2" placeholder="Введите пароль">
						</div>
	
						<div class="p-2 text-center">
							<button type="button" class="btn btn-success" @click="Register">Зарегистрироваться</button>
							<button type="button" class="btn btn-warning" @click="hideModalRegister">Отмена</button>
						</div>
					</div>
				</div>
			</div>
		</b-modal>
	</div>
</template>
<script>

import alert from '@/components/Alert.vue';
import axios from 'axios';
import router from "../router.js";
export default {
	components: {
		alert

	},
	data() {
		return {
			message: "",
			DATA: [],
				LoginData: {
					login: '',
					password: '',
					remember: false
				},
				RegisterData: {
					name: "",
					login: "",
					email: "",
					password1: "",
					password2: ""
				}
		}	
	},
	methods: {
		Login() {
			const path = 'http://localhost:5000/Login';
			if (this.LoginData.login == '' || this.LoginData.password == '') {
				this.message = 'Введите логин и пароль';
			} else {
				axios.post(path, this.LoginData)
					.then((res) => {
						if (res.data.message) {
							this.message = res.data.message;
						} else {
							this.hideModalLogin();
							this.Signin();
						}
					})
			}
			
		},
		Signin: () => {
			router.push({name: 'Profile'});
		},
		
		showModalLogin() {
			this.$refs['modal-login'].show();
		},
		hideModalLogin() {
			this.$refs['modal-login'].hide();
			this.message = '';
			this.LoginData.login = '';
			this.LoginData.password = '';
		},
		showModalRegister() {
			this.$refs['modal-register'].show();

		},
		hideModalRegister() {
			this.$refs['modal-register'].hide();
			this.message = '';
		},
		clearForm() {
			this.RegisterData.name = "";
			this.RegisterData.login = "";
			this.RegisterData.email = "";
			this.RegisterData.password1 = "";
			this.RegisterData.password2 = "";
		},
		postData() {
			const path = 'http://localhost:5000/Register';
			axios.post(path, this.RegisterData)
				.then((res) => {
					console.log(res.data);
					if (res.data.message) {
						this.message = res.data.message;
					} else {
						this.hideModalRegister();
						this.clearForm();
					}
				})

		},
		validPasswiord() {
			if (this.RegisterData.password1 != this.RegisterData.password2) {
				this.message = 'Пароли не соответствуют';
			} else {
				this.postData();
				
			}
		},
		Register() {
			if (this.RegisterData.name == '' || this.RegisterData.login == '' || this.RegisterData.email == '' || this.RegisterData.password1 == '' || this.RegisterData.password2 == '') {
				this.message = "Не все поля заполнены";
			} else {
				this.validPasswiord();


			}
		},
	},
};
</script>

<style>
.btn {
	margin: 5px;
}
.row {
	margin: 20% 0 0 0;
}
label {
 margin-bottom: 10px;
}
input {
	width: 300px;
	padding-top: 3px;
	margin-bottom: 20px; 
}
</style>
