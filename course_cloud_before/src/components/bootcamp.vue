<template>
    <div>
        <lab_head />

        <lab_header :order='order' />
        <div class="bootcamp-description layout-no-margin-top">
            <div>
                <h1>来一场高效又实战的训练</h1>
                <h4>资深工程师指导学习，实战中融会贯通IT技术</h4>
                <button class="btn">立即加入</button>
            </div>
        </div>

        <div class="bootcamp-features">
            <div class="container">
                <div class="row">
                    <div class="col-md-3">
                        <img src="/static/img/bootcamp-project.png">
                        <div class="bootcamp-features-description">
                            <span>优秀项目</span>
                            <span>专注实战</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <img style=" padding-left: 24px;" src="/static/img/bootcamp-teacher.png">
                        <div class="bootcamp-features-description">
                            <span>技术大牛</span>
                            <span>有问必答</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <img src="/static/img/bootcamp-comment.png">
                        <div class="bootcamp-features-description">
                            <span>实验报告</span>
                            <span>悉心点评</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <img src="/static/img/bootcamp-certificate.png">
                        <div class="bootcamp-features-description">
                            <span>完成课程</span>
                            <span>获得证书</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="bootcamp-courses">
            <div class="container">
                <div class="bootcamp-courses-header">
                    <h4 class="bootcamp-courses-title">训练营课程</h4>
                    <div class="bootcamp-courses-description">
                        动手实践，激发创新实力
                    </div>
                </div>
                <div class="bootcamp-courses-body" v-for="(seckill,index) in seckill_list" :key="index">
                    <h2>
                    {{seckill.title}}
                    {{seckill.time}}
                    </h2>
                    <div v-for="(item, index) in seckill.courses" :key="index">
                    <div class="media bootcamp-courses-item">
                        <div class="media-left bootcamp-courses-media">
                            <img class="media-object" :src="course_img(item.img)">
                        </div>
                        <div class="media-body bootcamp-courses-body">
                            <div class="bootcamp-courses-info">
                                <div style='float:left'>
                                    <h4>
                                    <span v-if="item.is_online == 1">已上线</span>
                                    <span v-else>即将上线</span>
                                    {{item.name}}
                                    </h4>
                                </div>
                                <div style="float:right; margin:0 20px 5px 0;">
                                    <span style=' font-size:21px; color:#666'>剩余名额：</span>
                                    <span style=' font-size:34px; color:#ba1b21'>{{ item.stock }}</span>
                                </div>
                                <div style="clear:both"></div>
                                <hr  />
                                <div>
                                    <p>{{item.desc}}</p>
                                </div>
                                <div>推荐先学：<a href="https://www.shiyanlou.com/courses/1" target="_blank">Linux基础入门</a></div>
                                <div>
                                    <p><a class="tagStyle2">Kali</a><a class="tagStyle2">渗透测试</a><a class="tagStyle2">Linux</a></p>
                                </div>
                            </div>
                            <div class="bootcamp-courses-subscribe">
                                <div class="pull-right bootcamp-courses-order">
                                    <div class="pull-left">
                                        <span style="margin-bottom: -8px;">￥{{item.price | price_filter}}</span>
                                        <span class="member-price" data-container="body" data-toggle="popover" data-placement="top" data-original-title="会员优惠" data-html="true" data-content="普通会员(<span class='price-number'>8折</span>)：<span class='price-number'>￥103.2</span><br>高级会员(<span class='price-number'>5折</span>)：<span class='price-number'>￥64.5&nbsp;&nbsp;</span>">
                                            <a href="/vip" title="">会员最低5折</a>
                                        </span>
                                    </div>
                                    <router-link :to="{path:'/courses/course_show/',query:{id:item.id}}">查看详情</router-link>
                                    <a v-if='item.stock>0' class="btn pull-right" style="background:#f66" href="javascript:void(0);" @click="join(item.price,item.name,item.id)">立即秒杀</a>
                                    <a v-else class="btn pull-right" style="background:#aaa" href="javascript:void(0);">座无虚席</a>
                                </div>
                            </div>
                        </div>
                    </div>

                    <hr>
                </div>
                </div>
            </div>
        </div>
        <div class="bootcamp-faq">
            <div class="container">
                <div class="bootcamp-faq-header">
                    <h4 class="bootcamp-faq-title">训练营FAQ</h4>
                </div>
                <div class="bootcamp-faq-body">
                    <div class="bootcamp-faq-question">
                        WHAT：实验楼训练营是什么？
                    </div>
                    <div class="bootcamp-faq-answer">
                        <img src="/static/img/bootcamp-answer.png">：训练营是一系列有教师服务（有问必答，实验报告点评等）的实验课。您将在教师指导下，在实验楼中完成一个可上线运行的产品原型或一系列编程任务，项目实战中融会贯通2-3门IT技术及开发流程。
                    </div>
                    <div class="bootcamp-faq-question">
                        WHY：为什么选择实验楼训练营课程？
                    </div>
                    <div class="bootcamp-faq-answer">
                        <img src="/static/img/bootcamp-answer.png">：实战，实战，实战！课程教师是具备多年研发经验的资深工程师，课程选题来自优秀的开源技术或仿知名网站。非常适合已学基础技术却迷茫不知道如何运用的同学，零基础的同学可按课程要求学习推荐的先学课程。
                    </div>
                    <div class="bootcamp-faq-question">
                        HOW：训练营课程学习流程是怎样的？
                    </div>
                    <div class="bootcamp-faq-answer">
                        <img src="/static/img/bootcamp-answer.png">：按实验文档依次完成实验，公开实验报告，实验中的问题随时在问答中提交，教师24小时内回复问答。完成所有实验并认真提交实验报告，可获得GOOD或PASS课程证书。
                    </div>
                </div>
                <div class="bootcamp-faq-footer">
                    <a class="bootcamp-faq-more" href="/questions/" target="_blank">更多疑问，查看这里>></a>
                </div>
            </div>
        </div>

        <Modal v-model="course_pay" :middle="true" :hasCloseIcon="true">
            <course_pay :course_price="course_price" :course_name="course_name" :cid='cid' :order="order" />
        </Modal>

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
import course_pay from './common/course_pay';
import { drillcourse } from './axios_api/api'
import { config, formatXml } from '../config.js';
import { seckill_data_get, get_vip_list_get, get_vip_order_get } from './axios_api/api'
export default {
    data() {
        return {
            seckill_list: [],
            course_price: '',
            course_name: '',
            order: '',
            course_pay: false,
            cid: '',
        }
    },
    mounted() {
        this.get_course(),
            this.imgsrc = config['uploadurl']
    },
    methods: {
        // 显示支付model
        join: function (price, name, cid) {
            let params = { token: localStorage.getItem("token") }
            // 发送请求到后端
            get_vip_order_get(params).then(resp => {
                if (resp.code === 200) {
                    this.course_price = price
                    this.course_name = name
                    this.cid = cid
                    this.course_pay = true;
                    this.order = resp.order
                } else {
                    alert(resp.message)
                    window.location.href = "/"
                }
            })
        },
        course_img(img) {
            if (img == 'course.jpg') {
                return config['baseurl'] + 'static/upload/' + img
            } else {
                return config['qiniuurl'] + img
            }
        },
        // 获取秒杀课程
        get_course() {
            seckill_data_get().then(res => {
                this.seckill_list = res.data;
                console.log(res);
            })
        },

    },
    filters: {
        price_filter(value) {
            return value / 100
        },
    },
    components: {
        lab_head,
        lab_header,
        lab_footer,
        user_info,
        last_paths,
        QR_code,
        course_pay,
    }
}
</script>
<style>

</style>