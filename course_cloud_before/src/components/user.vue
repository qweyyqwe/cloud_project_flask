<template>
    <div>

        <lab_head />
        <lab_header />

        <div class="userinfo-banner layout-no-margin-top">
            <div class="container layout">
                <div class="row">
                    <div class="col-md-9 clearfix">
                        <div class="pull-left userinfo-banner-avatar">

                            <div class="user-avatar ">
                                <a class="avatar" href="/user_profile" target="_blank">
                                    <img :src="src">
                                </a>

                                <a class="member-icon" href="/vip" target="_blank">

                                    <img v-if='vip==1' src="/static/img/vip0-icon.png">
                                    <img v-if='vip==2' src="/static/img/vip-icon.png">
                                    <img v-if='vip==3' src="/static/img/vip2-icon.png">

                                </a>

                            </div>

                        </div>
                        <div class="pull-left userinfo-banner-details">
                            <div class="userinfo-banner-meta">

                                <div class="user-username ">
                                    <a class="username" href="/user_profile" target="_blank">

                                        {{ username }}

                                    </a>
                                    <span class="user-level"><i>L</i>{{ experience | lou }}</span>
                                </div>

                            </div>
                            <div class="userinfo-banner-status">

                                <span>{{ occupation }}</span>

                                <a href="/edu/1" target="_blank">{{ school }}</a>

                            </div>
                        </div>
                    </div>
                    <div class="col-md-3 userinfo-banner-labinfo">
                        <div class="userinfo-banner-level">
                            <img src="/static/img/lou-level.png">
                            <div class="userinfo-current-level"><span>{{ experience | lou }}</span> 楼</div>
                            <div class="userinfo-level-more" data-toggle="tooltip" data-placement="bottom" title="在实验环境中动手输入代码或命令时才计入有效学习时间">

                                距 {{ experience+10  | lou}} 楼还需 {{ experience | lou }} 分钟有效学习时间
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="container layout">
            <div class="row">
                <div class="col-md-9 layout-body">

                    <div class="content" role="tabpanel">

                        <Tabs :datas="param" class-name="h-tabs-card" v-model="selected" @change="changeValue" class="tabs"></Tabs>
                        <div v-if="selected === '实验课程'">
                            <SwitchList v-model="type" :datas="datas" small @change="changeValue" class="switchlist"></SwitchList>
                        </div>
                        <!-- 实验课程 -->
                        <div v-if="selected === '实验课程'">
                            <lab_course :courselist="this.courselist" />
                        </div>

                        <!-- 实验报告 -->
                        <div v-if="selected === '实验报告'">
                            <lab_report :reportlist="this.reportlist" />
                        </div>

                        <!-- 实验讨论 -->
                        <div v-if="selected === '实验讨论'">
                            <lab_question :questionlist="this.questionlist" :src='this.src' />
                        </div>
                    </div>

                </div>
                <div class="col-md-3 layout-side">

                    <a class="side-sda apply-git" href="http://git.shiyanlou.com/shilei" target="_blank">
                        <img src="/static/img/my-git.png">
                        <span>代码库</span>
                    </a>

                    <div class="sidebox user-visitors">
                        <div class="sidebox-header">
                            <h4 class="sidebox-title">最近来访</h4>
                        </div>
                        <div class="sidebox-body">

                            <div>
                                <visitor :data="data" />
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="modal fade" id="message-modal" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                        <h4 class="modal-title">发送消息给 石头山</h4>
                    </div>
                    <div class="modal-body">
                        <textarea style="width:100%; min-height:100px; max-width:100%;"></textarea>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-default" data-dismiss="modal">取消</button>
                        <button class="btn btn-primary send-btn">发送</button>
                    </div>
                </div>
            </div>
        </div>
        <lab_footer />

    </div>
</template>

<script>
import lab_head from './common/lab_head';
import lab_header from './common/lab_header';
import lab_footer from './common/lab_footer';
import user_info from './common/user_info';
import last_paths from './common/last_paths';
import QR_code from './common/QR_code';
import visitor from './common/visitor'
import lab_course from './common/lab_course'
import lab_report from './common/lab_report'
import lab_question from './common/lab_question'
import { user_info_get, learn_get ,get_visitor} from './axios_api/api';
import { config } from '../config'
export default {
    data() {
        return {
            // 父传子
            data:[

            ],
            // 实验课程&实验报告&实验讨论选项变量
            param: {
                实验课程: '实验课程',
                实验报告: '实验报告',
                实验讨论: '实验讨论'
            },
            // 绑定选择：实验课程&实验报告&实验讨论
            selected: '实验课程',
            datas: {
                学过的: '学过的',
				关注的: '关注的',
				购买的: '购买的',
                发布的: '发布的'
            },
            type: '学过的',
            // 课程列表
            courselist: [],
            // 报告列表
            reportlist: [],
            // 帖子列表
            questionlist: [],
            username: "",
            date_joined: "",
            email: "",
            phone: "",
            src: '',
            occupation: "",
            school: "",
            vip: 3,
            vip_time: "",
            experience: "0",
            user_data: {},
            config: '',
            uid: '',
        }
    },
    beforeMount() {
        this.changeValue();
        this.get_user_info();
        this.config = config;
    },
    mounted:function(){
        this.uid = localStorage.getItem('uid')
        this.get_vis()
    },
    methods: {
        // 按条件查询(实验课程(学过的 & 关注的 & ) & 实验报告 & 实验讨论)
        changeValue() {
            let params = { token: localStorage.getItem('token'), type: this.type, selected: this.selected }
            learn_get(params).then(resp => {
                if (this.selected === '实验课程') {
                    this.courselist = resp.courselist
                    console.log(this.courselist)
                    for (let i = 0; i < this.courselist.length; i++) {
                        if (this.courselist[i].img === 'course.jpg') {
                            this.courselist[i].img = config['uploadurl'] + this.courselist[i].img
                        } else {
                            this.courselist[i].img = config['qiniuurl'] + this.courselist[i].img
                        }
                    }
                } else if (this.selected === '实验报告') {
                    this.reportlist = resp.reportlist
                    console.log(this.reportlist)
                } else if (this.selected === '实验讨论') {
                    this.questionlist = resp.questionlist
                    console.log(this.questionlist)
                }
            })
        },
        // 获取访客
        get_vis() {
            var params = { uid: this.uid }
            get_visitor(params).then(res => {
                console.log(res)
                this.data = res.data
            })
        },

        // 获取用户信息
        get_user_info() {
            var params = { token: localStorage.getItem('token') }
            user_info_get(params).then(resp => {
                if (resp.code == 200) {
                    this.user_data = resp.data;
                    this.username = resp.data.username;
                    this.date_joined = resp.data.date_joined;
                    this.email = resp.data.email;
                    this.phone = resp.data.phone;
                    this.occupation = resp.data.occupation;
                    this.school = resp.data.school;
                    this.vip = resp.data.vid;
                    this.vip_time = resp.data.vip_time;
                    this.experience = resp.data.experience;
                    if (resp.data.photo === '1.jpg') {
                        this.src = '../../static/img/' + resp.data.photo
                    } else {
                        this.src = config['qiniuurl'] + resp.data.photo
                    }
                } else {
                    console.log(resp)
                    this.$Message(resp.message)
                    this.$router.push('/')
                }
            })
        }

    },
    filters: {
        lou(value) {

            value = Math.round(value / 10)
            return value
        }
    },
    components: {
        lab_head,
        lab_header,
        lab_footer,
        user_info,
        last_paths,
        QR_code,
        lab_course,
        lab_report,
        lab_question,
        visitor,
    },
}
</script>

<style>
.tabs {
    font-size: 18px;
}
.switchlist span {
    margin-top: 10px;
    border: 0;
}
</style>
