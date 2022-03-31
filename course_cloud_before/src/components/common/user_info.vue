<template>

    <div class="panel panel-default panel-userinfo">
        <div class="panel-body body-userinfo">
            <div class="media userinfo-header">
                <div class="media-left">
                    <div class="user-avatar">
                        
                        <a class="avatar" href="#sign-modal" data-toggle="modal" data-sign="signin">
                            <img class="circle" src="/static/img//logo-grey.png">
                        </a>
                        
                    </div>
                </div>
                <div class="media-body">
                    
                    <span class="media-heading username">欢迎来到实验楼</span>
                    <p class="vip-remain">做实验，学编程</p>
                    
                </div>
            </div>

            <div class="row userinfo-data" v-if="username == ''">
                
                <hr>
                <div class="btn-group-lr">
                <a href="#sign-modal" type="button" class="btn btn-success col-md-5 col-xs-6 login-btn" data-toggle="modal" data-sign="signin">登录</a>
                <a href="#sign-modal" type="button" class="btn btn-success col-md-5 col-xs-6 col-md-offset-1 register-btn" data-toggle="modal" data-sign="signup">注册</a>
                </div>

            </div>

            <div v-else>
                    <!-- <img :src="http://127.0.0.1:8080/static/img/1.jpg"> -->
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <img :src="myimg" alt="" width="30px" height="30px">

                
                    欢迎您：<a class="btn btn-default navbar-btn sign-in" data-sign="signin" data-toggle="modal" href='/user'>{{ username }}</a>
                
            </div>

            <div class="userinfo-footer row">
                <div class="col-md-6 col-xs-6 pos-left">
                    
                    <a href="#sign-modal" data-toggle="modal" data-sign="signin"><span class="glyphicon glyphicon-bookmark"></span> 加入私有课</a>
                    
                </div>
                <div class="col-md-6 col-xs-6 pos-right">
                    <a href="/contribute" target="_blank"><span class="glyphicon glyphicon-send"></span> 我要投稿</a>
                </div>

                <div id="join-private-course" class="modal fade words-ctrl" tabindex="-1" role="dialog">
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h4 class="modal-title">加入私有课</h4>
                            </div>
                            <div class="modal-body">
                                <div style="margin:15px 0; font:16px;">输入教师提供的私有课程码可以加入教师的私有课程。</div>
                                <form id="private-course-form" method="POST" action="/courses/join">
                                    <div class="form-group">
                                        <label for="code">邀请码</label>
                                        <input class="form-control" id="code" name="code" type="text" value="">
                                        <input name="_csrf_token" type=hidden value="1483786710##0229e038fd44e98fbb3031ffe65d41ef52368b10">
                                    </div>
                                </form>

                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
                                <button type="button" class="btn btn-primary" onclick="document.getElementById('private-course-form').submit();">确定</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>


    </div>
</template>

<script>

import {user_get} from '../axios_api/api'
import {config,formatXml} from '../../config.js';
export default {
        data(){
        return{
            username:"",
            img:'',
            imgsrc:"",
            userimg:"",

            // 头像
            myimg:""
        }
    },
    beforeMount(){
        this.check_login()
    },
    mounted(){
        this.check_login()
    },
    methods:{
         // 检查登录状态
        check_login(){
            var uname = localStorage.getItem('username');
            var img = localStorage.getItem("img");
            if(img == '1.jpg'){
                this.myimg = config['vueurl'] + 'static/img/1.jpg'
            }else{
                this.myimg = config['qiniuurl'] + img
            }
            var data = {uid:localStorage.getItem('uid')}
                user_get(data).then(res=>{
                    this.img = res.img
                    this.imgsrc = config['baseurl']+'static/upload/'+res.img;
                })
                if(uname==null){
                    this.username = ""
                }else{
                    this.username = uname
                }
                console.log(this.username)

        },

    }

}
</script>

<style>
    @font-face {
        font-family: "lantingxihei";
        src: url("/static/fonts/FZLTCXHJW.TTF");
    }

    /* modal 模态框*/
    #invite-user .modal-body {
        overflow: hidden;
    }
    #invite-user .modal-body .form-label {
        margin-bottom: 16px;
        font-size:14px;
    }
    #invite-user .modal-body .form-invite {
        width: 80%;
        padding: 6px 12px;
        background-color: #eeeeee;
        border: 1px solid #cccccc;
        border-radius: 5px;
        float: left;
        margin-right: 10px;
    }
    #invite-user .modal-body .msg-modal-style {
        background-color: #7dd383;
        margin-top: 10px;
        padding: 6px 0;
        text-align: center;
        width: 100%;
    }
    #invite-user .modal-body .modal-flash {
        position: absolute;
        top: 53px;
        right: 74px;
        z-index: 999;
    }
    /* end modal */

    .en-footer {
        padding: 30px;
        text-align: center;
        font-size: 14px;
    }
</style>
