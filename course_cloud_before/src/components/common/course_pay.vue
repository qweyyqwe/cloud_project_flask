<template>
    <div>
        <!-- 注册会员 -->
        <div class="border">
            <div class="title">课程秒杀</div>
            <hr />
            <div class="margin_left">
                <div class="title1">课程名称</div>
                <div class="title-name">{{ course_name }}</div>
                <div class="button">
                    <div class="title1">优惠券:(选填)</div>
                    <div>
                        <input type="text" v-model="pay_code" placeholder="请输入邀请码">
                    </div>
                    <div class="title1">支付方式</div>
                    <Radio v-model="vip_pay" :datas="param_pay" keyName="code" titleName="name" class="vip_pay"></Radio>
                </div>
            </div>
            <hr />
            <div class="margin_left">
                <div>
                    <div style="line-height:60px;text-align:right;">
                        <span class="pay">付款：</span>
                        <span class="font">￥{{ course_price |price_filter }}</span>
                    </div>
                    <div>
                        <Button color="red" style="float:right;width:150px;height:40px;" @click="pay_vip" :disabled="disabled">确认购买</Button>
                    </div>
                    <div class="checkaa">
                        <Checkbox v-model="value" @change="check_value">同意</Checkbox>
                    </div>
                    <div class="aaa">
                        <a href="http://127.0.0.1:8080/privacy" style="margin-top:5px;">购买服务条款</a>
                    </div>
                </div>
            </div>
        </div>
        <!-- 支付确认 -->
        <Modal v-model="consent" :middle="true" :hasCloseIcon="true">
            <div style="width:300px;">
                <span style="font-size:28px;padding-left:105px;">支付确认</span>
                <br /><br />
                <Button color="green" style="font-size:18px;margin-left:50px;" @click="succeed">支付成功</Button>
                <Button color="red" style="font-size:18px;margin-left:10px;" @click="cancel">取消支付</Button>
            </div>
        </Modal>

    </div>
</template>

<script>
import { get_order_mysql_post, get_alipay_get, get_succeed_get, purchase_get } from "../axios_api/api"
import { config, formatXml } from '../../config.js';
export default {
    props: {
        course_price: Number,
        order: String,
		course_name: String,
		cid: Number,
    },
    data() {
        return {
            // 参数
            // 支付方式
            vip_pay: "支付宝",
            // 邀请码
            pay_code: "",
            // 是否同意会员协议，默认不同意
            value: false,
            // 不同意会员协议，无法下单
            consent: false,
            // 显示关闭样式
            disabled: true,
            // 价格
            price: '',
            // 取整
            param_pay: [{ name: '支付宝', code: "支付宝" }, { name: '微信', code: "微信" }],
        }
    },
    mounted() {

    },
    filters: {
        // 价格过滤器
        price_filter(value) {
            value = value / 100
            return value
        },
    },
    methods: {
        // 支付成功
        succeed() {
            let params = { order: this.order, token: localStorage.getItem("token"),cid:this.cid }
            get_succeed_get(params).then(resp => {
                if (resp.code === 200) {
					this.purchase();
                    this.$Message(resp.message)
					this.$router.go(0)
					this.purchase();
                } else {
                    this.$Message("开通失败")
                    this.$router.go(0)
                }
            })
        },
        // 支付成功，名额扣除
        purchase() {
            purchase_get({ cid: this.cid }).then(res => {
                console.log(res.data);
                this.$router.push('/bootcamp');
            })
        },
        // 取消支付
        cancel() {
            alert("取消成功")
            this.$router.go(0)
        },
        // 是否已同意购买协议
        check_value() {
            if (this.value == false) {
                this.disabled = false
            } else {
                this.disabled = true
            }
        },
        // 发起购买请求
        pay_vip() {
            if (this.vip_pay === "支付宝") {
                this.consent = true;
                // 将订单信息传给前端
                this.price = this.course_price / 100
                let data = { token: localStorage.getItem("token"), order: this.order, price: this.price, record: this.cid }
                get_order_mysql_post(data).then(resp => {
                    console.log(resp)
                    if (resp.code === 200) {
                        this.$Message(resp.message)
                        // 跳转后价格单位修改为元
                        get_alipay_get(data).then(resp => {
                            if (resp.code === 200) {
                                // 跳转支付页面
                                // 打开一个新的页面进行跳转
                                window.open(resp.data, '_blank')
                            }
                        })
                    } else {
                        alert(resp.message)
                    }
                })
            } else {
                alert("本网站暂时只支持支付宝付款")
                return false
            }

        },
    }
}
</script>

<style>
.title-name {
    height: 40px;
    font-size: 28px;
    font-weight: bold;
    width: 900px;
    color: gold;
}
.border {
    width: 900px;
    height: 400px;
}
.title {
    height: 40px;
    font-size: 28px;
    font-weight: bold;
    width: 900px;
}
.margin_left {
    margin-left: 20px;
}
.title1 {
    margin: 15px 0 10px 0;
    font-size: 18px;
    font-weight: bold;
}
.button {
    margin: 20px 0 20px 0;
}
.pay {
    font-weight: bold;
    font-size: 15px;
}
.vip_pay {
    margin-bottom: 10px;
}
.font {
    font-size: 24px;
    color: red;
    margin-right: 20px;
}
.checkaa {
    float: right;
    margin-right: -45px;
    margin-top: 50px;
}
.aaa {
    float: right;
    margin-right: -120px;
    margin-top: 52px;
}
</style>
