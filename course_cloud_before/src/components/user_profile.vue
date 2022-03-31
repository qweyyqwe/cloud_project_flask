<template>
    <div>

        <lab_head />
        <lab_header />
        <section>
            <div style="height:1000px;background-color:#eee">

            </div>
            <div id='main_board' style="clear:both">
                <div class="left_board">
                    <div class='board_item'><a href='javascript:void(0)' class='board_link' @click='change_mod(1)'> 基本信息</a></div>
                    <div class='board_item'><a href='javascript:void(0)' class='board_link' @click='change_mod(2)'> 账号密码</a></div>
                    <div class='board_item'><a href='javascript:void(0)' class='board_link' @click='change_mod(3)'> 邮件通知</a></div>
                    <div class='board_item'><a href='javascript:void(0)' class='board_link' @click='change_mod(4)'> 兑换码</a></div>
                    <div class='board_item'><a href='javascript:void(0)' class='board_link' @click='change_mod(5)'> 优惠券</a></div>
                </div>
                <div class='right_board'>

                    <div v-if='mod==1' class='board_content'>

                        <table style="border:1px solid #fff" cellpadding='50px'>

                            <tr>
                                <td>
                                    <div class='board_ele'>头像</div>
                                </td>
                                <td>
                                    <div class='board_ele'>
                                        <Avatar v-show="src" :src='src' :width='150' fit='fill'></Avatar>
                                    </div>
                                </td>
                                <td>
                                    <div class='board_ele'><input type="file" @change="upload_qiniu"></div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <div class='board_ele'>昵称</div>
                                </td>
                                <td>
                                    <div class='board_ele'><input type="text" v-model="username"></div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <div class='board_ele'>我的职业</div>
                                </td>
                                <td>
                                    <div class='board_ele'><input type="text" v-model="occupation"></div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <div class='board_ele'>我的学校</div>
                                </td>
                                <td>
                                    <div class='board_ele'><input type="text" v-model="school"></div>
                                </td>
                            </tr>

                        </table>

                        <div style="padding:30px">
                            <Button class="h-btn-blue h-btn-text-white h-btn-block" @click="submit">保存修改</Button>
                        </div>
                    </div>
                    <div v-if='mod==2' class='board_content'>
                        <table style="border:1px solid #fff" cellpadding='50px'>

                            <tr>
                                <td>
                                    <div class='board_ele'>手机</div>
                                </td>
                                <td>
                                    <div class='board_ele'>{{ phone }}</div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <div class='board_ele'>邮箱</div>
                                </td>
                                <td>
                                    <div class='board_ele'>{{ email }}</div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <div class='board_ele'>密码</div>
                                </td>
                                <td>
                                    <div class='board_ele'><a>修改密码</a></div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <div class='board_ele'>账号绑定</div>
                                </td>
                                <td>
                                    <div class='board_ele'></div>
                                </td>
                            </tr>

                        </table>

                        <div style="padding:30px">
                            <Button class="h-btn-blue h-btn-text-white h-btn-block">保存修改</Button>
                        </div>
                        <table style="clear:both"></table>
                    </div>
                    <div v-if='mod==3' class='board_content'>
                        <table style="border:1px solid #fff" cellpadding='50px'>

                            <tr>
                                <td>
                                    <div class='board_ele'>提醒邮件</div>
                                </td>
                                <td>
                                    <div class='board_ele'></div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <div class='board_ele'>官方邮件</div>
                                </td>
                                <td>
                                    <div class='board_ele'></div>
                                </td>
                            </tr>

                        </table>

                        <div style="padding:30px">
                            <Button class="h-btn-blue h-btn-text-white h-btn-block">保存修改</Button>
                        </div>
                    </div>
                    <div v-if='mod==4' class='board_content'>
                        <table style="border:1px solid #fff" cellpadding='50px'>

                            <tr>
                                <td>
                                    <div class='board_ele'>兑换码</div>
                                </td>
                                <td>
                                    <div class='board_ele'></div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <div class='board_ele'>
                                        <div class="h-input-group" v-width="500">
                                            <input type="text" placeholder="输入" />
                                            <Button color="blue">确定</Button>
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <div class='board_ele'></div>
                                </td>
                            </tr>

                        </table>

                        <div style="padding:30px">
                            <Button class="h-btn-blue h-btn-text-white h-btn-block">保存修改</Button>
                        </div>
                    </div>
                    <!-- 展示优惠券 -->
                    <div v-if='mod==5' class='board_content'>
                        <table cellpadding='50px' class="coupon-table" v-for="(coupon,index) in couponlist" :key="index">
							<br>
                            <tr>
                                <td class='coupon_ele'>
                                    <img :src="config['uploadurl'] + coupon.img" class="imgsrc">
                                    <div class="coupon-code">
                                        优惠券码：
                                        <span class="coupon-content">
                                            {{ coupon.coupon }}
                                        </span>
                                    </div>
                                    <span class="coupon-name">{{ coupon.title }}</span>
                                </td>
                                <td class='coupon_ele1'>
                                    剩余过期时间：
                                    <span class="coupon-days">
                                        {{ coupon.days }} 天
                                    </span>
                                </td>
                                <td class='coupon_ele2' v-if="coupon.state === '待使用'">
                                    <Button color="green">可使用</Button>
                                </td>
                                <td class='coupon_ele2' v-if="coupon.state === '已过期'">
                                    <Button color="green" :disabled="true">已过期</Button>
                                </td>
                            </tr>
							<br>
							<tr>
								<td colspan="4" class="coupon-tr"></td>
							</tr>
                            
                        </table>

                        <div style="text-align:center;margin-top:50px;">
                            <Button color="blue" @click="routerpush">兑换优惠券</Button>
                        </div>

                    </div>

                </div>
            </div>
        </section>
        <table style="clear:both">
        </table>

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
import { user_info_get, user_info_post, get_uptoken, coupon_list_get } from './axios_api/api';
import { config, formatXml } from '../config.js';
export default {
    data() {
        return {
            // 七牛云token
            uptoken: '',
            // 七牛云头像展示
            src: '',
            // 七牛云头像key
            imgkey: '',
            username: "",
            date_joined: "",
            email: "",
            phone: "",
            photo: "1.jpg",
            occupation: "",
            school: "",
            vip: 3,
            vip_time: "",
            experience: "0",
            user_data: {},
            occupation: '',
            school: '',
            mod: 1,
            data: [
                {
                    title: '首页',
                    key: 'welcome',
                    icon: 'h-icon-home'
                },
                {
                    title: '查询',
                    key: 'search',
                    icon: 'h-icon-search'
                },
                {
                    title: '收藏',
                    key: 'favor',
                    icon: 'h-icon-star',
                },
                {
                    title: '任务',
                    icon: 'h-icon-task',
                    key: 'task',
                }
            ],
            couponlist: '',
        };
    },
    beforeMount() {
        this.get_user_info()
        this.src = config['qiniuurl'] + localStorage.getItem('img')
    },
    mounted: function () {
        // 调用接口
        // 获取token
        this.get_uptoken();
        // 获取优惠券
        this.get_coupon();
        this.config = config
    },
    methods: {
        // 跳转到兑换优惠券页面
        routerpush() {
            this.$router.push('/coupon')
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
        // 上传七牛
        upload_qiniu(e) {
            // 获取文件对象
            let file = e.target.files[0];
            // 声明变量
            let param = new FormData();
            // 将上传凭证添加参数
            param.append('token', this.uptoken);
            // 添加文件
            param.append('file', file);
            // 定制化axios
            const axios_qiniu = this.axios.create({ withCredentials: false });
            // 发送请求
            axios_qiniu({
                method: 'POST',
                url: 'http://up-z1.qiniu.com',
                data: param,
                timeout: 30000
            }).then(res => {
                console.log(res)
                this.src = config['qiniuurl'] + res.data.key
                this.imgkey = res.data.key
            })
        },
        // 修改数据库中的头像

        // 获取七牛云凭证
        get_uptoken() {
            get_uptoken().then(res => {
                this.uptoken = res.token
            })
        },

        // 保存修改
        submit() {
            var data = { token: localStorage.getItem('token'), username: this.username, occupation: this.occupation, school: this.school, img: this.imgkey }
            user_info_post(data).then(resp => {
                this.$Message(resp.message)
                if (resp.code == 200) {
                    // this.$router.push('/user')
                }
            })
        },
        // 获取用户信息
        get_user_info() {
            var params = { token: localStorage.getItem('token') }
            user_info_get(params).then(resp => {
                if (resp.code == 200) {
                    console.log(resp)
                    this.user_data = resp.data;
                    this.username = resp.data.username;
                    this.date_joined = resp.data.date_joined;
                    this.email = resp.data.email;
                    this.phone = resp.data.phone;
                    this.photo = resp.data.photo;
                    this.occupation = resp.data.occupation;
                    this.school = resp.data.school;
                    this.vip = resp.data.vid;
                    this.vip_time = resp.data.vip_time;
                    this.experience = resp.data.experience;
                    console.log(resp.data.photo)
                    localStorage.setItem('img', resp.data.photo)
                } else {
                    this.$Message(resp.message)
                    this.$router.push('/')
                }
            })
        },
        // 换页
        change_mod(value) {
            this.mod = value
        }
    },
    filters: {
        price_filter(value) {
            value = value / 100
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
    }
}
</script>

<style>
.coupon-tr {
    border-bottom: 2px solid #eeeeee;
}
.coupon-days {
    color: red;
}
.coupon-name {
    font-size: 15px;
}
.coupon-content {
    color: gold;
    font-weight: bold;
}
.coupon-code {
    margin-top: -20px;
    margin-bottom: 5px;
}
.imgsrc {
    width: 250px;
    height: 150px;
}
.coupon-table {
    font-size: 14px;
    width: 600px;
    text-align: center;
}
.coupon_ele {
    /* width: 25%; */
    text-align: center;
    margin-bottom: 5px;
}
.coupon_ele1 {
    /* width: 20%; */
    text-align: center;
    margin-bottom: 5px;
}
.coupon_ele2 {
    /* width: 25%; */
    text-align: center;
    margin-bottom: 5px;
}
.board_ele {
    padding: 30px 20px;
    width: 150px;
}
.inner_left {
    float: left;
    width: 200px;
    padding-top: 130px;
}
#main_board {
    position: absolute;
    top: 0%;
    left: 50%;
    margin-top: 430px;
}
.left_board {
    width: 400px;
    height: 600px;
    margin: -350px 0px 50px -600px;
    padding: 30px;
    float: left;
    background-color: #eee;
    font-size: 24px;
    color: #444;
}
.right_board {
    width: 800px;
    height: 600px;
    margin: -350px 0px 50px -200px;
    padding: 30px;
    float: left;
    background-color: #eee;
    font-size: 20px;
    color: #444;
}
.board_item {
    background-color: #fff;
    padding: 40px 20px;
    width: 370px;
    display: flex;

    align-items: center;

    justify-content: center;
}
.board_link {
    text-decoration-line: none;
}
.board_content {
    background-color: #fff;
    padding: 60px;
    width: 720px;
}
</style>
