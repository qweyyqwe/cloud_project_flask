<template>
    <div>
        <lab_head  />

            <lab_header :title='"学习路径 - 实验楼"'  />

        <div class="container layout layout-margin-top">
        
        
        <div class="row">
            <div class="col-md-9 layout-body">
                
        <div class="content">
            <div class="row">
            
                <div class="col-sm-6" v-for="(item,index) in datalist" :key='index'>
                    <router-link :to="{path:'/courses/course_show/',query:{id:item.pk}}">
                        <div class="path-item">
                            <div class="col-xs-5 col-md-4  path-img">
                                <img :src="path_img(item.img)">
                            </div>
                            <div class="col-xs-7 col-md-8">
                                <div class="path-name">{{item.name}}</div>
                                <div class="path-course-num"><span>{{item.category}}</span></div>
                            </div>
                            <div class="desc-layer">
                                <div class="center">{{item.desc}}</div>
                            </div>
                        </div>
                         </router-link>
                </div>
            </div>
        </div>

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




import {config,formatXml} from '../config.js';
export default {
    data(){
        return{
            datalist:''
        }
        },
    components:{
        lab_head,
        lab_header,
        lab_footer,
    },
    mounted:function(){
        this.datalist = this.$route.query.data
        console.log(this.datalist)
    },
    methods:{
         path_img(img){
            if(img == '1471513769430.png'){
                return config['baseurl']+'static/upload/' + img
            }else{
                return config['qiniuurl'] + img
            }
        },

    },
}
</script>

<style>
</style>
