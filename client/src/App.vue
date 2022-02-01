<template>
	<div id="app">
		<div>
			<router-view/>
		</div>
	</div>
</template>

<script>
import "./router.js";
//import router from "./router.js";
//import Autorisation from './components/Autorisation.vue'
//import room from './components/Room.vue'
//import axios from 'axios'
export default {
	name: 'App',
	//created(){
	//	router.push({name: 'Autorisation'});
	//}
	
	//components: {
	//	Autorisation,
		//room
	//},
};
</script>
