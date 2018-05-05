Vue.component('header-app',{
    template: `
        <header>
            <ul class="nav_bar">
            <li class="nav_item logo"><router-link class="router_link logo" to="/"><img class="logo_image" src="./static/img/camera-icon.png">Photogram</router-link></li>
            <li class="nav_item"><router-link class="router_link" to="/logout/">Logout</router-link></li>
            <li class="nav_item"><router-link  class="router_link" v-bind:to="'/users/'+user_id">My Profile</router-link></li>   
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
            user_id:null
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
                            <router-link class="router_link" to="/login/"><button class="submit_btn color_blue">Login</button></router-link>
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
                  <input id="location" name="location" type="text" value="">
              </tr>
              <tr>
                  <h4><label for="bio">Biography</label></h4>
                  <textarea id="bio" name="biography"></textarea>
              </tr>
              <tr>
                  <h4><label for="photo">Photo</label></h4>
                      <input id="photo" name="photo" type="file">
                      <br>
              </tr>
               <tr v-for="mess in error" class="error1">
                  <h4>{{mess}}</h4>
              </tr>
              <tr>
                  <button type="submit" class="color_green submit_btn2">Register</button>
              </tr>
            </table> 
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
                if(jsonResponse.message == "Username taken" || jsonResponse.message=="Required Field is missing" || jsonResponse.message=="Please submit a profile photo"){
                    self.error = [jsonResponse.message];
                    self.$router.push('/register')
                }else{
                    alert(jsonResponse.message)
                    self.reponse = jsonResponse.response;
                    self.$router.push('/home')
                }
            }).catch(function(error){
                alert(error);
                self.error = error;
            });
        }
    }
});

const Login = Vue.component('login',{
    template: ` 
        <div>
        <h2 class="title">Login</h2>
        <form id="loginform" method="POST" enctype="multipart/form-data" @submit.prevent="login">
             <table class="logininformation">
              <tr v-for="mess in error" class="error1">
                  <h4>{{mess}}</h4>
              </tr>
              <tr>
                  <h4><label for="username">Username</label></h4>
                  <input id="username" name="username" type="text" value="">
              </tr>
              <tr>
                  <h4><label for="password">Password</label></h4>
                  <input id="password" name="password" type="password" value="">
              </tr>
              <tr>
                  <br>
                  <button type="submit" class="color_light_green submit_btn2">Login</button>
              </tr>
             </table>
        </form>
    </div>
    `,
    data: function() {
        return {
            reponse:[],
            error:[]
        }
    },
    methods:{
        login:function(){
            let self=this;
                    let form = document.getElementById("loginform");
                    let formData = new FormData(form);
            fetch("/api/auth/login",{
                method:'POST',
                body:formData,
                header:{
                    "Content-Type": "application/json",
                }
            }).then(function(response){
                return response.json();
            }).then(function (response){
                if(response.message == "sucess" ){
                    let token = response.token;
                    let user_id = response.user_id
                    
                    localStorage.setItem('token', token);
                    localStorage.setItem('user_id', user_id)
                    
                    self.$router.push('/explore')
                }else{
                    self.error = [response.message];
                    self.reponse = response.response;
                    self.$router.push('/login/')
                }
            }).catch(function(error){
                alert(error);
                self.error = error;
            });
        }
    }
});

const Logout = Vue.component('logout',{
    data: function() {
        return {
            reponse:[],
            error:[]
        }
    },
    created:function(){
            let self=this;
            fetch("/api/auth/logout",{
                method:'POST',
                header:{
                    "Content-Type": "application/json"
                }
            }).then(function(response){
                return response.json();
            }).then(function (response){
                    let token = response.token;
 
                    localStorage.setItem('token', token);
                    localStorage.setItem('user_id', null);
                    self.$router.push('/');
            }).catch(function(error){
                alert(error);
                self.error = error;
            });
        }
});

const Post = Vue.component('post',{
    template:`
    <div>
        <h2 class="title">New Post</h2>
        <form id="postform" method="POST" enctype="multipart/form-data" @submit.prevent="post">
             <table class="postinformation">
                <tr v-for="mess in error" class="error1">
                  <h4>{{mess}}</h4>
              </tr>
              <tr>
                  <h4><label for="photo">Photo</label></h4>
                  <input id="photo" name="photo" type="file">
              </tr>
              <tr>
                  <h4><label for="caption">Caption</label></h4>
                  <textarea id="caption" name="caption" placeholder="Write a caption..."></textarea>
              </tr>
              <tr>
                  <br>
                  <button type="submit" class="color_light_green submit_btn2">Submit</button>
              </tr>
             </table>
        </form>
    </div>
    `,
    data: function() {
        return {
            reponse:[],
            error:[]
        }
    },
    methods:{
     post:function(){
            let self=this;
                    let form = document.getElementById("postform");
                    let formData = new FormData(form);
            let user_id = localStorage.getItem('user_id');
            fetch("/api/users/"+user_id+"/posts",{
                method:'POST',
                body: formData,
                headers:{
                    'Authorization': 'X-Token ' + localStorage.getItem('token')
                }
            }).then(function(response){
                return response.json();
            }).then(function (response){
                if(response.message == "sucess" ){
                    self.$router.push('/explore')
                }else{
                    self.error = [response.message];
                    self.reponse = response.response;
                    self.$router.push('/post')
                }
            }).catch(function(error){
                alert(error);
                self.error = error;
            });
        }
    }
});

const Profile = Vue.component('profile',{
    template:`
        <div id="profile">
           <div class="profileinfo">
                   <img class="big_profile_photo" v-bind:src="'./static/img/'+user.profile_photo" />
                   <div class="userinfo">
                          <h3>{{user.firstname}} {{user.lastname}}</h3>
                          <h5>{{user.location}}<br>Member since {{user.created_on}}</h5>
                          <h5>{{user.biography}}</h5>
                   </div>
                   <div class="followinfo">
                       <p><em>{{userinfo.no_of_posts}}</em><em>{{userinfo.no_of_followers}}</em><br><b>Post</b><b>Following</b></p>
                       
                       <button v-if="nofollow" class="submit_btn color_blue" @click="follow">Follow</button>
                       <button v-else class="submit_btn color_green">Following</button>
                   </div>
           </div>
           
           <div v-if="haspost" class="allposts">
               <div v-for="post in posts" class="image_container">
                   <img class="profile_images" v-bind:src= "'./static/img/'+post.photo">
               </div>
           </div>
           <div v-else>
                <h1>No Posts</h1>
           </div>
    </div>
    `,
    watch:{
      'trigger' (newval,oldval){
          this.reload();
      }  
    },
    data: function() {
        return {
            reponse:[],
            error:[],
            posts:[],
            user:null,
            userinfo:null,
            logined_in:false,
            nofollow:true,
            haspost:true,
            trigger:null
        }
    },
    created:function(){
            let self=this;
            let user_id = this.$route.params.user_id;
            if (user_id == 'null'){
                self.$router.push('/explore');
            }
            fetch("/api/users/"+user_id+"/posts",{
                method:'GET',
                headers:{
                    "Content-Type": "application/json",
                    'Authorization': 'X-Token ' + localStorage.getItem('token')
                }
            }).then(function(response){
                return response.json();
            }).then(function (response){
                if(response.message == "All posts"){
                    self.logined_in = true;
                    self.posts = response.posts;
                    self.haspost = true;
                    self.trigger = false;
                }else if(response.message == 'No post'){
                    self.logined_in = true;
                    self.haspost = false;
                    self.trigger = false;
                }else{
                    self.logined = false;
                }
            }).catch(function(error){
                alert(error);
                self.error = error;
            });
            fetch("/api/users/"+user_id,{
                method:'GET',
                headers:{
                    "Content-Type": "application/json",
                    'Authorization': 'X-Token ' + localStorage.getItem('token')
                }
            }).then(function(response){
                return response.json();
            }).then(function (response){
                if(response.message == "sucess"){
                    self.user = response.user;
                    self.userinfo = response.userinfo;
                    self.nofollow = response.userinfo.no_follow;
                }
            }).catch(function(error){
                alert(error);
                self.error = error;
            });
        },
    methods:{
        follow:function(){
            let self=this;
            let user_id = this.$route.params.user_id;
            fetch("/api/users/"+user_id+"/follow",{
                method:'POST',
                headers:{
                    "Content-Type": "application/json",
                    'Authorization': 'X-Token ' + localStorage.getItem('token')
                }
            }).then(function(response){
                return response.json();
            }).then(function (response){
                alert(response.message)
                if(response.message == "sucess"){
                    self.nofollow = false;
                    self.userinfo.no_of_followers = self.userinfo.no_of_followers + 1
                    self.$router.push('/users/'+user_id)
                }
            }).catch(function(error){
                alert(error);
                self.error = error;
            });
 
        }       
    }
});


const Explore = Vue.component('explore',{
    template:`
        <div id="explorepost">
        <div v-if="!logined_in" class="error2">
            <center>
            <h5>You must login first</h5>
            <router-link class="router_link" to="/login/"><button class="submit_btn color_blue">Login</button></router-link>
            </center>
        </div>
        <div v-else class="sucess2">
            <center>
            <h5>Logged in </h5>
            </center>
        </div>
        <div class="rightinfo">
            <ul class="posts">
                <li v-for="post in posts">
                    <div class="post">
                        <table>
                            <tr>
                                <td>
                                    <img class="post_profile_image" v-bind:src="'./static/img/'+post.profile_pic">
                                      <h5><router-link  class="router_link color_black" v-bind:to="'/users/' +post.user_id">{{ post.username}}</router-link></h5>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                      <img class="post_image" v-bind:src= "'./static/img/'+post.photo"/>
                                        
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <p> {{ post.caption}}</p>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                <span class="like" >
                                    <img  v-if="post.liked" class="like_image" src='./static/img/liked.png'/>
                                    <img @click="like(post.id)" v-else class="like_image" src='./static/img/like.png'/>
                                    <h5>{{post.no_of_likes}} Like</h5>
                                </span>
                                <span class="date">
                                    <h5>{{post.created_on}}</h5>
                                </span>
                                </td>
                            </tr>
                        </table>
                    </div>
                </li>
            </ul>
        </div>
        
        <div v-if="logined_in" class="leftinfo">
            <router-link  class="router_link" to="/post/new"><button class="submit_btn2 color_blue" >New Post</button></router-link>
        </div>
    </div>
    `,
    watch:{
      'trigger' (newval,oldval){
          this.reload();
      }  
    },
    data: function() {
        return {
            reponse:[],
            error:[],
            posts:[],
            logined_in:false,
            trigger:null
        }
    },
    created:function(){
            let self=this;
            fetch("/api/posts",{
                method:'GET',
                headers:{
                    "Content-Type": "application/json",
                    'Authorization': 'X-Token ' + localStorage.getItem('token')
                }
            }).then(function(response){
                return response.json();
            }).then(function (response){
                if(response.message == "All posts"){
                    self.logined_in = true;
                    self.posts = response.posts;
                    self.trigger = false;
                }else if(response.message == 'No post'){
                    self.logined_in = true;
                    self.trigger = false;
                }else{
                    self.logined_in = false;
                }
            }).catch(function(error){
                alert(error);
                self.error = error;
            });
        },
    methods:{
        like:function(post_id){
            let self=this;
            fetch("/api/users/"+post_id+"/like",{
                method:'POST',
                headers:{
                    "Content-Type": "application/json",
                    'Authorization': 'X-Token ' + localStorage.getItem('token')
                }
            }).then(function(response){
                return response.json();
            }).then(function (response){
                    if(response.message == "sucess"){
                        fetch("/api/posts",{
                        method:'GET',
                        headers:{
                            "Content-Type": "application/json",
                            'Authorization': 'X-Token ' + localStorage.getItem('token')
                        }
                         }).then(function(response){
                        return response.json();
                        }).then(function (response){
                        if(response.message == "All posts"){
                            self.logined_in = true;
                            self.posts = response.posts;
                            self.trigger = false;
                        }else if(response.message == 'No post'){
                            self.logined_in = true;
                            self.trigger = false;
                        }else{
                            self.logined_in = false;
                        }
                }).catch(function(error){
                    alert(error);
                    self.error = error;
                });
                }
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
       },
       {
           path:'/login/',
           component:Login
       },
        {
           path:'/logout/',
           component:Logout
       },
        {
           path:'/explore',
           component:Explore
       },
        {
           path:'/post/new',
           component:Post
       },
       {
           path:'/users/:user_id',
           component:Profile
       }
        
       
       ]
});


const app = new Vue({
    el:'#project2',
    router
})