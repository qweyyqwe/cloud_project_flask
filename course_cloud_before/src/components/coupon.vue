<template>
    <div>

        <lab_head />
        <lab_header />

        <div style="margin-top:50px;margin-bottom:70px;">
            <img src="../../static/img/coupon_heng.png" class="cover-image">
            <div class="coupon-blan">
                <span>您的实验豆剩余：<span class="coupon-blan-span">{{ bean }}</span></span>
            </div>
        </div>
        <section>
            <div class="tab-content" style="width:1300px;margin:auto;">
                <div role="tabpanel" class="tab-pane active">
                    <div class="row">
                        <div class="col-md-4 col-sm-6  course" style="float:left;" v-for="(data,index) in datas" :key="index">
                            <a class="course-box" href="javascript:void(0)" @click="opened(data)" style="width:350px;margin-top:20px;">
                                <div class="sign-box">

                                </div>
                                <div>
                                    <!-- 封面 -->
                                    <img alt="20元会员优惠券" :src="get_img(data.src)" class="course_img">
                                </div>

                                <div class="course-body">
                                    <!-- 标题 -->
                                    <span class="course-title" data-toggle="tooltip" data-placement="bottom" title="20元「会员」优惠券">{{ data.title }}</span>
                                    <span class="course-title" style="font-size:14px;color:#f66" data-toggle="tooltip" data-placement="bottom" title="20实验豆">{{ data.bean }}实验豆</span>
                                </div>
                            </a>
                        </div>

                    </div>
                </div>
            </div>
            <Modal v-model="open" class="modal-model">
                <div>
                    <div class="header-title">{{ value.title }}</div>
                    <div class="comment-con" v-if="value.name === '会员'">
                        购买会员时可抵扣现金¥{{value.bean }}，领取后30天内有效；优惠码仅限个人使用，禁止转用和售卖。
                    </div>
                    <div class="comment-con" v-if="value.name === '训练营'">
                        购买训练营课程时可抵扣现金¥{{value.bean }}，领取后30天内有效；优惠码仅限个人使用，禁止转用和售卖。
                    </div>
                    <div class="comment-bean">
                        <span>
                            消耗实验豆：{{ value.bean }} 个
                            <span class="total-bean" v-if="show_bean < 0">
                                (剩余实验豆：{{ bean }}个)
                            </span>
                            <span class="total-bean2" v-if="show_bean >= 0">
                                (剩余实验豆：{{ bean }}个)
                            </span>
                        </span>
                    </div>
                    <div class="footer-button">
                        <Button color="primary" @click="modalConfirm" v-if="show_bean < 0" :disabled="true">立即兑换</Button>
                        <Button color="primary" @click="modalConfirm" v-if="show_bean >= 0" :disabled="false">立即兑换</Button>
                    </div>
                </div>
            </Modal>
        </section>
        <br />
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
import { coupon_list_get, get_bean, create_coupon_get } from './axios_api/api';
import { config, formatXml } from '../config.js';
export default {
    data() {
        return {
            open: false,
            datas: [
                { name:'会员',title: '20元「会员」优惠券', bean: '20', src: 'coupon_hui20.png' },
                { name:'会员',title: '50元「会员」优惠券', bean: '50', src: 'coupon_hui50.png' },
                { name:'训练营',title: '5元「训练营课程」优惠券', bean: '5', src: 'coupon_xun5.png' },
                { name:'训练营',title: '10元「训练营课程」优惠券', bean: '10', src: 'coupon_xun10.png' },
                { name:'训练营',title: '15元「训练营课程」优惠券', bean: '15', src: 'coupon_xun15.png' },
            ],
            value: '',
            bean: 0,
            show_bean: 0,
        };
    },
    mounted() {
		this.get_blan();
		this.config = config
    },
    methods: {
        get_img(src){
            return config['uploadurl'] + src
        },
        opened(data) {
            this.open = true;
            this.value = data;
            this.show_bean = this.bean - this.value.bean
        },
        modalConfirm() {
            let params = { token: localStorage.getItem('token'), price: this.value.bean, title: this.value.title, img: this.value.src }
			console.log(params)
			create_coupon_get(params).then(resp => {
				if (resp.code === 200) {
					this.$Message('兑换成功')
					this.$router.push('/user_profile')
				}
                console.log(resp)
            })
        },
        // 获取剩余实验豆
        get_blan() {
            let params = { token: localStorage.getItem('token') }
            get_bean(params).then(resp => {
                if (resp.code === 200) {
                    this.bean = resp.bean
                    console.log(resp)
                }
            })
        },
        // 获取优惠券
        get_coupon() {
            let params = { token: localStorage.getItem('token') }
            coupon_list_get(params).then(resp => {
                if (resp.code === 200) {
                    this.couponlist = resp.couponlist
                    console.log(resp.couponlist)
                }
            })
        },
    },
    components: {
        lab_head,
        lab_header,
        lab_footer,
        user_info,
        last_paths,
        QR_code,
    }
}
</script>

<style>
.course_img {
    width: 350px;
    height: 210px;
}
.coupon-blan {
    font-size: 18px;
    margin-left: 900px;
    margin-top: -85px;
    color: white;
    font-weight: bold;
}
.coupon-blan-span{
	font-size: 24px;
	color: green;
}
.modal-model {
    width: 1000px;
    height: 200px;
}
.comment-con {
    width: 970px;
    height: 50px;
    background: #f1f1f1;
    font-size: 18px;
    padding: 5px 0 0 15px;
}
.comment-bean {
    margin-top: 30px;
    font-size: 15px;
}
.header-title {
    font-size: 24px;
    margin-bottom: 10px;
}
.footer-button {
    text-align: right;
}
.total-bean {
    padding-left: 50px;
    color: #f66;
}
.total-bean2 {
    padding-left: 50px;
    color: #45b984;
}
</style>
