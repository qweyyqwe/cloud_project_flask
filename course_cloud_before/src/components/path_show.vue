<template>
    <div>
        <lab_head :title='"路径名称 - 实验楼"'  />
        <body>
            
            <lab_header  />


            <div class="container layout layout-margin-top">
    
<ol class="breadcrumb">
    <li><a href="/paths/">学习路径</a></li>
    <!-- <li class="active"><a href="/paths/newhand">{{pathlist.name}}</a></li> -->
    <li class="active"><a href="">{{pathlist.name}}</a></li>
</ol>

    <div class="row">
        <div class="col-md-9 layout-body">
            
    <div class="content" style="padding:0px">
        <div class="path-description" style="margin:0px">
            <div class="path-desc-top clearfix" style="background: url('/static/img/1471513740139.png') no-repeat;background-size: cover;">
                <div class="name-total-box clearfix">
                    <div class="col-md-6 col-sm-6 col-md-offset-1 path-name">
                        <h4>{{pathlist.name}}</h4>
                    </div>
                    <div class="col-md-3 col-sm-6 col-md-offset-1 path-total-courses">
                        <span class="total-courses-box">课程 <span class="num">{{pathlist.section_sum}}</span></span>
                    </div>
                </div>
                <div class="col-md-10 col-md-offset-1 path-desc-text">{{pathlist.desc}}</div>
            </div>
            <div class="path-desc-btm" >
                <div class="col-sm-12 col-md-4 clearfix learn-time-div">
                    <div class="col-md-12 text-left need-learn-time">预计需要 <span class="num">{{pathlist.study_time}}</span> 小时学习</div>
                </div>
                <div class="col-sm-12 col-md-8  clearfix text-right" style="padding-top:0px">
                    <div class="col-xs-12">
                        <span>{{pathlist.add_sum}}</span>人已加入  &nbsp;&nbsp;&nbsp;&nbsp;
                        <Button class="btn btn-path-operation btn-join-path" data-sign="signin" href="#sign-modal" data-toggle="modal" @click="path_follow">{{followcontent}}</Button>
                        
                        <p style="font-size:10px;margin-top:5px">加入获得路径课程更新提醒</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="content">
        <ul class="nav nav-tabs" role="tablist">
            <li role="presentation" class="active">
                <a href="#path-details" aria-controls="path-details" role="tab" data-toggle="tab">路径详情</a>
            </li>
            <li role="presentation">
            <a href="#path-comments" aria-controls="path-comments" role="tab" data-stat="path_comments" data-toggle="tab">路径评论(<span class="comments-count">0</span>)</a>
            </li>
        </ul>
        <div class="tab-content">
            <div role="tabpanel" class="tab-pane path-details active" id="path-details">
                <div class="details-box">    
                    <a href="/courses/63" class="btn start-btn">开始学习</a>


<div>


    <div class="clearfix text-center path-title-box" v-for="(item,index) in stagelist" :key="index">
        <span class="line hidden-xs"></span>
        <span>{{item.stage}}:{{item.stage_name}}</span>
        <span class="line hidden-xs"></span>
        <div class="row">
                        
        <div class="col-md-4 col-sm-6  course"  v-for="(i,index) in item.coursedata" :key="index">

            <a class="course-box" :href="'/courses/course_show/?id='+i.id+''">
                <div class="sign-box">
 
                    <i class="fa fa-star-o course-follow pull-right"
                        data-follow-url="/courses/63/follow"
                        data-unfollow-url="/courses/63/unfollow"  style="display:none"  ></i>
                </div>
                <div class="course-img">
                    
                    <img :alt="item.name" :src="course_img(i.img)">
                </div>
                <div class="course-body">
                    <span class="course-title" data-toggle="tooltip" data-placement="bottom" :title="i.name">{{i.name}}</span>
                </div>
                <div class="course-footer">
                      <span class="course-per-num pull-left">
                            <i class="fa fa-users"></i>{{i.collect_num}}
                        
                            <i class="fa fa-tags"></i>{{i.category }}
                        </span>  
                </div>
            </a>
        </div>

    </div>
    </div>
    
</div>
                  
                    
                    <div class="btn end-pin">完成学习</div>
                </div>
            </div>
            <div role="tabpanel" class="tab-pane path-comment" id="path-comments">
              <div class="comment-box">
                    <div class="comment-form">
                        
                        <div class="comment-form-unlogin">                                
                            请
                            <a href="#sign-modal" data-toggle="modal" data-sign="signin"> 登录 </a>
                            后发表评论
                        </div>
                        
                    </div>
                    <div class="comment-title">最新评论</div>
                    <div class="comment-list"></div>
                    <div class="pagination-container"></div>
              </div>
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

        </body>
    </div>
</template>

<script>
import lab_head from './common/lab_head';
import lab_header from './common/lab_header';
import lab_footer from './common/lab_footer';
import user_info from './common/user_info';
import last_paths from './common/last_paths';
import QR_code from './common/QR_code';
import {get_path_info_get,path_follow_get,is_path_follow_get} from './axios_api/api'



import {config,formatXml} from '../config.js';
export default {
    data(){
    return{
        pathlist:[],
        stagelist:[],
        followcontent:'',
        type:localStorage.getItem('type'),

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
    mounted(){
        this.id = this.$route.query.id
        this.get_path_info();
        this.is_path_follow();

    },
    methods:{
        is_path_follow:function(){
            is_path_follow_get({pid:localStorage.getItem('pid'),uid:localStorage.getItem('uid')}).then(resp=>{
                localStorage['type']=resp.type
                if (this.type == '1') {
                this.followcontent = '已加入'
              
                }
                else if(this.type == '0'){
                this.followcontent = '加入路径'
                
                }
            })

        },
        path_follow:function(){
            if (this.type == '0') {
                this.followcontent = '已加入'
                this.type = '1'
                this.pathlist.add_sum +=1
            }
            else if(this.type == '1'){
                this.followcontent = '加入路径'
                this.type = '0'
                this.pathlist.add_sum -=1
            }
            path_follow_get({pid:localStorage.getItem('pid'),uid:localStorage.getItem('uid'),type:this.type}).then(resp=>{
   
            })
        },
        course_img(img){
            if(img == 'course.jpg'){
                return config['baseurl']+'static/upload/' + img
            }else{
                return config['qiniuurl'] + img
            }
        },
        //获取路径信息
      
        get_path_info(){
            let pid = this.$route.query.id;
            localStorage['pid'] = pid
            get_path_info_get({pid:pid}).then(resp=>{
            console.log(resp.pathdata)
            console.log(resp.stagedata)
            console.log(resp.stagecoursedata)
            this.pathlist = resp.pathdata
            this.stagelist = resp.stagedata
          
            })
        },

    },
}
</script>

<style>
    
</style>
