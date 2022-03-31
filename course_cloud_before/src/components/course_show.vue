<template>
    <div>
        <lab_head />
        <lab_header />

        <div class="container layout layout-margin-top">

            <ol class="breadcrumb">
                <li><a href="/courses/">全部课程</a></li>

                <li class="active">
                    <a href="/courses/1">
                        {{ course_list.name }}
                    </a>
                </li>
            </ol>

            <div class="row">
                <div class="col-md-9 layout-body">

                    <div class="side-image side-image-mobile">
                        <img src="https://dn-simplecloud.shiyanlou.com/ncn1.jpg?imageView2/0/h/300">
                    </div>
                    <div class="content course-infobox">
                        <div class="clearfix course-infobox-header">
                            <h4 class="pull-left course-infobox-title">

                                <span>{{ course_list.name }}</span>

                            </h4>
                            <div class="pull-right course-infobox-follow" data-follow-url="/courses/1/follow" data-unfollow-url="/courses/1/unfollow">
                                <span class="course-infobox-followers">{{course_list.collect_num}}</span>
                                <span>人关注</span>

                                <i class="fa fa-star-o" data-next="/login?next=%2Fcourses%2F1" @click="collect_click(course_list.id)"></i>

                            </div>
                        </div>
                        <div class="clearfix course-infobox-body">
                            <!-- <div class="course-infobox-content">
                                <p>
                                    {{ item.desc }}
                                </p>

                            </div> -->

                            <div class="course-infobox-progress">
                                <div v-for="(item,index) in section_list" :key="index" :class="[learn_list.indexOf(item.id)!=-1? 'course-progress-finished':'course-progress-new']" style="margin:2px"> </div>
                                <span>（{{ learn_list.length | learn_filter }}/{{ section_list.length }}）</span>
                            </div>

                            <div class="pull-right course-infobox-price">

                            </div>

                        </div>

                        <div class="clearfix course-infobox-footer">

                            <div class="pull-right course-infobox-learned">{{ course_list.collect_num }} 人学过</div>
                        </div>

                    </div>
                    <div class="content">
                        <div>
                            <Tabs :datas="types" v-model="type_selected" @change="change_type"></Tabs>
                        </div>
                        <div class="tab-content">
                            <!-- 实验列表 -->
                            <div v-if='type_selected=="list"'>

                                <div class="lab-item ">
                                    <h4 class="lab-item-title">{{ course_list.name }}</h4>
                                </div>

                                <div class="lab-item change_curse" v-for="(item,index) in section_list" :key="index">
                                    <div class="lab-item-status">

                                        <img src="/static/img/lab-not-ok.png">

                                    </div>
                                    <div class="lab-item-index">第{{ index+1 }}节</div>
                                    <div class="lab-item-title" data-toggle="tooltip" data-placement="bottom" title="基本概念及操作">
                                        <a :href="'/section_show/?sid=' + item.id + '&cid=' + course_list.id" target="_blank" rel="noopener noreferrer">{{ item.section_name }}</a></div>
                                    <div class="pull-right lab-item-ctrl">
                                    </div>
                                    <div class="pull-right lab-item-ctrl">
                                    </div>
                                    <!-- </button> -->
                                </div>

                            </div>
                            <!-- 实验评论 -->
                            <div v-if='type_selected=="comment"'>
                                <div class="lab-item ">
                                    <h4 class="lab-item-title">{{ course_list.name }} 实验评论</h4>
                                </div>
                                <div class="comment-box">
                                    <div class="comment-form">
                                        <comment v-for="comment in comment_list" :key="comment.id" :comment='comment' :token='token' :ques_id='ques_id' :res='false' :is_son='"father"'></comment>
                                        <publish :token='token' :ques_id='ques_id'></publish>

                                    </div>
                                    <div class="comment-title">最新评论</div>
                                    <div class="comment-list">
                                    </div>
                                    <div class="pagination-container"></div>
                                </div>
                            </div>
                            <!-- 实验报告 -->
                            <div v-if='type_selected=="report"'>
                                <div class="lab-item ">
                                    <h4 class="lab-item-title">{{ course_list.name }} 实验报告</h4>
                                </div>
                                <div role="tabpanel" class="tab-pane active">
                                    <div class="discovery-list">
                                        <div class="row report-items">
                                            <!-- 在这里循环遍历 -->
                                            <div class="col-md-3 report-item clearfix" v-for="(report,index) in reportlist" :key="index">
                                                <a href="/courses/reports/1255351">
                                                    <div class="report-item-course">

                                                        {{ report.name }}
                                                    </div>
                                                    <div class="report-item-lab">第{{ report.sid }}章</div>

                                                    <div class="report-item-count">
                                                        <span>{{ report.content | content_filter}} 字</span>
                                                        <div class="report-item-arrow">
                                                            <div class="report-item-arrow-line"></div>
                                                        </div>
                                                    </div>
                                                </a>
                                                <div class="col-xs-8">
                                                    <div class="report-item-author">

                                                        <div class="user-avatar report-item-avatar">
                                                            <a class="avatar" href="/user/350045" target="_blank">
                                                                <img :src="userphoto(report.photo)">
                                                            </a>

                                                        </div>

                                                        <div class="user-username ">
                                                            <a class="username" href="/user/350045" target="_blank">
                                                                {{ report.username }}
                                                                <span class="user-level">
                                                                    <i>L</i>{{ report.exper | exper_filter }}
                                                                </span>
                                                            </a>
                                                        </div>

                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- 实验问答 -->
                            <div v-if='type_selected=="course"'>
                                <div class="lab-item ">
                                    <h4 class="lab-item-title">{{ course_list.name }} 实验问答</h4>
                                </div>
                                <a class="btn btn-success" data-toggle="modal" data-target="#askquestion">我要提问</a>
                                <hr>
                                <ul class="row question-items"></ul>
                                <div class="pagination-container"></div>
                            </div>
                        </div>
                    </div>

                </div>

                <lab_sidebar :course_list='course_list' v-if='course_list'></lab_sidebar>
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
import lab_sidebar from './common/lab_sidebar';
import comment from './common/comment';
import publish from './common/publish';
import { get_comments_get, get_questions_get, course_show_get, auth_info_get, user_lean_get, report_list_get } from './axios_api/api';
import { config, formatXml } from '../config.js';
export default {
    data() {
        return {
            // 分类
            types: {
                list: '实验列表',
                comment: '实验评论',
                report: '实验报告',
                course: '实验问答',
            },
            type_selected: 'comment',
            ques_id: 0,
            id: 0,
            comment_list: [],
            course_list: [],
            section_list: [],
            learn_list: [],
            token: '',
            reportlist: [],
        }
    },
    beforeMount() {
    },
    created() {
    },
    mounted() {
        this.id = this.$route.query.id
        this.get_course_info()
        this.get_lean_msg()
        this.token = localStorage.getItem('token')
        this.get_comments()
    },
    methods: {
        // 用户头像
        userphoto(photo) {
            if (photo === '1.jpg') {
                return config['uploadurl'] + photo
            } else {
                return config['qiniuurl'] + photo
            }
        },
        collect_click(id) {
            this.$Message(id)
        },
        // 加载实验评论
        get_comments() {
            console.log('加载实验评论')
            var params = { type: 'comment', cid: this.id }
            get_questions_get(params).then(resp => {
                console.log(resp.data)
                this.ques_id = resp.data[0].id
                var params2 = { ques_id: resp.data[0].id }
                // 已登录展示收藏情况
                var token = localStorage.getItem('token')
                if (token)
                    params2.token = token
                console.log(params2)
                get_comments_get(params2).then(resp => {
                    this.comment_list = resp.data
                })
            })
        },

        // 切换分类
        change_type() {
            if (this.type_selected === 'report') {
                let params = { cid: this.$route.query.id }
                report_list_get(params).then(resp => {
                    this.reportlist = resp.reportlist
                    console.log(this.reportlist)
                })
            }
        },
        // 获取课程信息
        get_course_info() {
            let cid = this.$route.query.id;
            // console.log(cid);

            // let cid = 3;
            var token = { token: localStorage.getItem('token') }
            course_show_get({ cid: cid, token: token }).then(res => {
                // console.log(res)
                this.course_list = res.course_ser;
                this.section_list = res.section_ser;
            })
        },
        // 获取学习状态
        get_lean_msg() {
            let token = localStorage.getItem('token');
            let cid = this.$route.query.id
            if (token) {
                user_lean_get({ token: token, cid: cid }).then(res => {

                    for (var i = 0; i < res.data.length; i++) {
                        this.learn_list.push(res.data[i].sid)
                    }
                })
            }
        }


    },
    filters: {
        learn_filter(num) {
            if (num) {
                return num
            } else {
                return 0
            }
        },
        exper_filter(value) {
            return value / 10
        },
        content_filter(value) {
            return value.length
        },

    },
    components: {
        comment,
        lab_head,
        lab_header,
        lab_footer,
        user_info,
        last_paths,
        QR_code,
        lab_sidebar,
        publish,
    }
}
</script>

<style>
</style>