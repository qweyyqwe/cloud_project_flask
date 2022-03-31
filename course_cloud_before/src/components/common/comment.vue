<template>
    <div>
            <div :class='is_son'>
            <div style='float:left; width:70px'>
                <div class="user-avatar ">
                <a class="avatar" href="/user_profile" target="_blank">
                    <!-- <img :src="img"> -->
                    <router-link :to="{name: 'users', query: {id: comment.user_info.id }}"><img :src="config['qiniuurl'] + comment.user_info.photo"></router-link>
                </a>

                <a class="member-icon" href="/vip" target="_blank">

                <img v-if='comment.user_info.vid==1' src="/static/img/vip0-icon.png">
                <img v-if='comment.user_info.vid==2' src="/static/img/vip-icon.png">
                <img v-if='comment.user_info.vid==3' src="/static/img/vip2-icon.png">

                </a>
                
            </div>
            </div>
            <div>
                    <div class='username'>
                        <a href="javascript:void(0);">
                            <span style="font-size:16px">{{ comment.user_info.username }}</span>
                        </a>
                        &nbsp;&nbsp;
                        <span style='font-size:14px;color:#c93'>{{ comment.user_info.experience/10 }} 楼</span>
                        
                    <div v-show="res" class='isres'>
                        回复 <a href="javascript:void(0);">{{ upgrade }}</a>
                        <br  />
                    </div>
                    </div>
                    
                    <div class='favorite'>
                    <a href="javascript:void(0);" @click='favo'>
                        <img v-if="comment.is_favorite==0" src="/static/img/favoritebefore.svg" width="22px" alt="">
                        <img v-else src="/static/img/favorited.svg" width="22px" alt="">
                    </a>
                    
                    {{ comment.favorate }}
                    回复
                    {{ comment.count }}
                    </div>
                    <div style='clear:both'></div>
                <div class='comment_content'>
                    
                    <div style="font-size:14px" v-html="comment.content">
                    </div>
                    <!-- {{ comment }} -->
                    
                <p>
                    <span style='font-size:12px;color:#888'>
                        {{ comment.create_time|date_time }}
                    </span>
                </p>
                <div style='float:left'>
                    <a href="javascript:void(0);" @click="show_res_mtd" v-if="comment.childlist && comment.childlist.length>0">{{ show_res_msg }}</a>
                </div>
                <div style='float:right'>
                    <a href="javascript:void(0);" @click="open_reply"  style='font-size:12px;color:#c93'>
                        回复
                    </a>
                </div>

                <div style='clear:both'></div>
                <div v-show='reply_opened' class="comment_reply">
                    
                    <mavon-editor
                        @save="saveDoc"
                        @change="updateDoc"
                        ref="editor"
                        v-model="doc2"
                        :toolbars="toolbars"
                        :toolbarsFlag='false'
                        :subfield='false'
                        defaultOpen='edit'
                        :placeholder='"回复 "+comment.user_info.username + ":"'
                        style="min-height:100px"
                    >   
                    </mavon-editor>
                    <br  />
                    <Button text-color="primary" @click='cancel'>取消</Button>
                    <Button color='green' @click='submit2(comment.id)'>提交</Button>
                </div>
                </div>
            </div>
            <div style='clear:both'></div>
            <hr  />
            </div>
            <div v-if="comment.childlist && comment.childlist.length>0" v-show="show_res">
                <comment v-for="child in comment.childlist" :key="child.id" :comment='child' :token='token' :ques_id='ques_id' :res='true' :upgrade='comment.user_info.username' :is_son='"son"'></comment>
            </div>
        
    </div>
</template>

<script>
import marked from 'marked'
import {mavonEditor} from 'mavon-editor'
import "mavon-editor/dist/css/index.css";
import { favorite_comment_post, publish_comment_post } from '../axios_api/api';
import {config,formatXml} from '../../config.js';
export default {
    name:'comment',
    components:{
        mavonEditor,
    },
    data() {
        return {
            config:{},
            show_res:false,
            show_res_msg:'查看所有回复',
            doc2:'',
            reply_opened:false,
            toolbars: {
                bold: true, // 粗体
                italic: true, // 斜体
                header: true, // 标题
                underline: true, // 下划线
                strikethrough: true, // 中划线
                mark: true, // 标记
                superscript: true, // 上角标
                subscript: true, // 下角标
                quote: true, // 引用
                ol: true, // 有序列表
                ul: true, // 无序列表
                link: true, // 链接
                imagelink: false, // 图片链接
                code: false, // code
                table: true, // 表格
                fullscreen: true, // 全屏编辑
                readmodel: true, // 沉浸式阅读
                htmlcode: true, // 展示html源码
                help: true, // 帮助
                /* 1.3.5 */
                undo: true, // 上一步
                redo: true, // 下一步
                trash: true, // 清空
                save: true, // 保存（触发events中的save事件）
                /* 1.4.2 */
                navigation: true, // 导航目录
                /* 2.1.8 */
                alignleft: true, // 左对齐
                aligncenter: true, // 居中
                alignright: true, // 右对齐
                /* 2.2.1 */
                subfield: true, // 单双栏模式
                preview: true, // 预览
            },
        };
    },
    props:['token', 'ques_id', 'comment', 'res', 'upgrade', 'is_son'],
    mounted(){
        this.config = config
    },
    methods: {
        // 判断父子组件
        judge_son(){
        },
        // 展开回复
        show_res_mtd(){
            if(this.show_res== false){
                this.show_res = true
                this.show_res_msg = '收起所有回复'
            }else{
                this.show_res = false
                this.show_res_msg = '查看所有回复'
            }
        },
        // 收藏
        favo(){
            var data = {com_id: this.comment.id, receive_id:this.comment.uid, token: localStorage.getItem('token')}
            favorite_comment_post(data).then(resp=>{
                // this.$Message(resp.message)
                if(this.comment.is_favorite==0){
                    this.comment.is_favorite ++
                    this.comment.favorate ++
                }else{
                    this.comment.is_favorite --
                    this.comment.favorate --
                }
                
            })

        },
        

        // 取消发表
        cancel(){
            this.reply_opened = false
        },
        // 发表回复
        submit2(id){
            var data={content:marked(this.doc2), token:localStorage.getItem('token'), ques_id: this.ques_id, reply: id}
            
            publish_comment_post(data).then(resp=>{
                this.$Message(resp.message)
                this.reply_opened = false
                this.$router.go(0)
                }
            )
        },
        // 打开回复框
        open_reply(index){
            if(this.reply_opened){
                this.reply_opened = false
            }else{
                this.reply_opened = true
            }
        },
        updateDoc(markdown, html) {
            // 此时会自动将 markdown 和 html 传递到这个方法中
            console.log("markdown内容: " + markdown);
            console.log("html内容:" + markdown);
        },
        saveDoc(markdown, html) {
            // 此时会自动将 markdown 和 html 传递到这个方法中
            console.log("markdown内容:" + markdown);
            console.log("html内容:" + html);
        }
    },
    filters:{
    date_time(value){
      return value.split('T').join(' ').split('.')[0]
    },
  }
}
</script>

<style>
.son{
    margin-left:50px
}
.isres{
    margin-top: 3px;
}
.username{
    float:left;
    width:250px;
    /* height:50px; */
    /* border:1px solid #F00 */
}
.favorite{
    float:right;
    width:80px;
    /* height:50px; */
    /* border:1px solid #F00 */
    }
.comment_content{
    width:92%;
    margin-left:8%;
    padding:0 10px 10px 10px;
    line-height: 23px;
}
.comment_reply{
    background-color: #eef;
    padding:15px;
}
</style>
