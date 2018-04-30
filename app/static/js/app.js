/*global Vue*/
const app = new Vue({
    el:'#Project2',
    data:{
        result:'',
        token:''
        
    },
    methods:{
        register(){
            fetch("api/user/register",{
                "header":{"x-token-access":localStorage.getItem('token')+''},
                "data":{
                    "firstname":document.getElementById('firstname').value,
                    "lastname":document.getElementById('lastname').value,
                    "username":document.getElementById('username').value,
                    "password":document.getElementById('password').value,
                    "email":document.getElementById('email').value,
                    "location":document.getElementById('location').value,
                    "bio":document.getElementById('bio').value,
                    "photo":document.getElementById('photo').value
                }
            }).then(function (response) {
                    return response.json();
                })
                .then(function (response) {
                    let result = response.data;
                    alert('{$result.message}');
                })
                .catch(function (error) {
                    alert('There was an error')
                })
        }

    }
})

    alert('yes');
