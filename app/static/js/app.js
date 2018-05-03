Vue.component('header-app',{
    template: `
        <header>
            <ul class="nav_bar">
            <li class="nav_item logo"><router-link class="router_link logo" to="/"><img class="logo_image" src="./static/img/camera-icon.png">Photogram</router-link></li>
            <li class="nav_item"><router-link class="router_link" to="/logout">Logout</router-link></li>
            <li class="nav_item"><router-link  class="router_link" to="/profile">My Profile</router-link></li>   
            <li class="nav_item"><router-link  class="router_link" to="/explore">Explore</router-link></li>   
            <li class="nav_item"><router-link class="router_link" to="/">Home</router-link></li>
            </ul>
        </header>
    `,
     watch: {
        '$route' (to, fom){
            this.reload()
        }
      },
    created: function() {
        let self = this;
        self.user=localStorage.getItem('token');
        self.user_id=localStorage.getItem('user_id');
    },
    data: function() {
        return {
            user: [],
        }
    },
    methods:{
        reload(){
            let self = this;
            self.user=localStorage.getItem('token');
            self.user_id=localStorage.getItem('user_id');
        }
    }
    
});

const Home = Vue.component('home',{
    template:
    `<div class="body-container">
        <div class="inforbox">
            <img class="wallpaper_small" src="./static/img/HD-Wallpapers1_FOSmVKg.jpeg">
        </div>
         <div class="inforbox">
            <table class="info_table">
                <tbody>
                    <tr class="top_table">
                        <td>
                            <img class="logo_image" src="./static/img/camera-icon.png">
                            <p class="logo small_logo">Photogram</p>
                        </td>
                    </tr>
                    <tr class="table_row">
                        <td>
                            <p>Share photos of your favourite moments with friends, family and the world.</p>
                        </td>
                    </tr>
                    <tr class="table_row">
                        <td>
                            <router-link class="router_link" to="/register"><button class="submit_btn color_green">Register</button></router-link>
                            <router-link class="router_link" to="/login"><button class="submit_btn color_blue">Login</button></router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>`,
     data: function() {
        return {}
    }
});

const Register = Vue.component('register',{
    template: `  
   <form id="signupform" method="POST" enctype="multipart/form-data" @submit.prevent="register">
        <table class="userinformation">
              <tr>
                  <h4><label for="username">Username</label></h4>
                  <input id="username" name="username" type="text" value="">
              </tr>
              <tr>
                  <h4><label for="password">Password</label></h4>
                  <input id="password" name="password" type="password" value="">
              </tr>
              <tr>
                  <h4><label for="firstname">Firstname</label></h4>
                  <input id="firstname" name="firstname" type="text" value="">
              </tr>
              <tr>
                  <h4><label for="lastname">Lastname</label></h4>
                  <input id="lastname" name="lastname" type="text" value="">
              </tr>
              <tr>
                  <h4><label for="email">Email</label></h4>
                  <input id="email" name="email" type="text" value="">
              </tr>
              <tr>
                  <h4><label for="location">Location</label></h4>
                  <input id="location" name="location" type="text" value="Location">
              </tr>
              <tr>
                  <h4><label for="bio">Biograpghy</label></h4>
                  <textarea id="bio" name="biography"></textarea>
              </tr>
              <tr>
                  <h4><label for="photo">Photo</label></h4>
                      <input id="photo" name="photo" type="file">
                      <br>
              </tr>
              <tr>
                  <button type="submit" class="color_green submit_btn2">Register</button>
              </tr>
    </form>`,
    data: function() {
        return {
            reponse:[],
            error:[]
        }
    },
    methods:{
        register:function(){
            let self=this;
                    let username = document.getElementById('username').value;
                    let password = document.getElementById('password').value;
                    let firstname = document.getElementById('firstname').value;
                    let lastname = document.getElementById('lastname').value;
                    let email = document.getElementById('email').value;
                    let location = document.getElementById('location').value;
                    let bio= document.getElementById('bio').value;
                    let photo = document.getElementById('photo').value;
                    let form = document.getElementById("signupform");
                    let formData = new FormData(form);
            fetch("/api/user/register",{
                method:'POST',
                body:formData,
                header:{
                    "Content-Type": "application/json",
                    "Authorization":"X-Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.1IgQSJegDKFAAJyua8STZ1X9M62Ykq4cZjxXRUjq6JI"
                }
            }).then(function(response){
                return response.json();
            }).then(function (jsonResponse){
                alert(jsonResponse.message);
                self.reponse = jsonResponse.response;
                self.$router.push('/explore')
            }).catch(function(error){
               alert(error);
                self.error = error;
            });
        }
    }
});

Vue.use(VueRouter);

const router = new VueRouter({
   routes:[
       {
           path:'/',
           component:Home
       },
       {
           path:'/register',
           component:Register
       }
       ]
});


const app = new Vue({
    el:'#project2',
    router
})