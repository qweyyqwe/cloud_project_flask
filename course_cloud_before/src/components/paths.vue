<template>
    <div>
        <lab_head  />

            <lab_header :title='"学习路径 - 实验楼"'  />

        <div class="container layout layout-margin-top">
        
        
        <div class="row">
            <div class="col-md-9 layout-body">
                
        <div class="content">
            <div class="row">
            
                <div class="col-sm-6" v-for="(item,index) in pathlist" :key='index'>
                    <!-- <a :href="'/paths/path_show/'+item.name" target="_blank"> -->
                    <router-link :to="{path:'/paths/path_show/',query:{id:item.id}}">
                        <div class="path-item">
                            <div class="col-xs-5 col-md-4  path-img">
                                <img :src="path_img(item.img)">
                            </div>
                            <div class="col-xs-7 col-md-8">
                                <div class="path-name">{{item.name}}</div>
                                <div class="path-course-num"><span>{{item.section_sum}}</span> 门课程</div>
                            </div>
                            <div class="desc-layer">
                                <div class="center">{{item.desc}}</div>
                            </div>
                        </div>
                         </router-link>
                    <!-- </a> -->
                </div>
                
      
            
            </div>
        </div>

            </div>
                <div class="col-md-3 layout-side">
            

                    <user_info  />
                    <last_paths  />
                    <QR_code  />

                </div>
            </div>
        </div>

        <lab_footer  />

    </div>
</template>

<script>
import lab_head from './common/lab_head';
import lab_header from './common/lab_header';
import lab_footer from './common/lab_footer';
import user_info from './common/user_info';
import last_paths from './common/last_paths';
import QR_code from './common/QR_code';
import {getpaths_get} from './axios_api/api'



import {config,formatXml} from '../config.js';
export default {
    data(){
        return{
            pathlist:'',

        }
        },
    components:{
        lab_head,
        lab_header,
        lab_footer,
        user_info,
        last_paths,
        QR_code,
    },
    mounted:function(){

    this.get_paths();


    },
    methods:{

        path_img(img){
            if(img == '1471513769430.png'){
                return config['baseurl']+'static/upload/' + img
            }else{
                return config['qiniuurl'] + img
            }
        },
        //获取所有路径
        get_paths(){
            getpaths_get().then(resp=>{
            console.log(resp.data)
            this.pathlist = resp.data
            })
        },

    },
}
</script>

<style>
</style>
