import home from '@/components/home'
const router = new VueRouter({
   routes:[
       {
           path:'/api/user/register',
           name:"Home",
           component:home
       }
       ]
})


const app = new Vue({
    el:'#project2',
    template:"<h1>Hi</h1>",
    router
})