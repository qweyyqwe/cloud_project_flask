<template>
    <div>
        <div class="sidebox">
        
            <div class="sidebox-header">
                <h4 class="sidebox-title">最热路径</h4>
            </div>
            <div class="sidebox-body course-content side-list-body" v-for="(item,index) in hotpathlist" :key='index'>
                <a :href="'/paths/path_show/?id='+item.id"><img style="width:25px;height:25px" :src="path_img(item.img)"> {{item.name}}
              </a>
            </div>
        
        </div>
    </div>
</template>

<script>

import {get_hot_path_get} from '../axios_api/api';
import {config,formatXml} from '../../config.js';
export default {
    data(){
        return{
            hotpathlist:'',

        }
        },

    mounted:function(){

    this.get_hot_paths();


    },
    methods:{
        path_img(img){
            if(img == '1.jpg'){
                return config['baseurl']+'static/upload/' + img
            }else{
                return config['qiniuurl'] + img
            }
        },
        //获取所有路径
        get_hot_paths(){
            get_hot_path_get().then(resp=>{
            console.log(resp.data)
            this.hotpathlist = resp.data
            })
        },

    },
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
