<template>
  <div>
    <p>欢迎来到注册界面</p>
    账号：<input type="text" v-model="account" /><br />
    密码：<input type="text" v-model="password" /><br />
    手机号：<input type="text" v-model="phone" /><br />
    <!-- uuid：<input type="text" v-model="uuid"><br> -->
    图片验证码：<input type="text" v-model="code" /><br />
    <h3>看不清图片点击换取一张</h3>
    <img id="captcha_img" :src="image_url" @click="get_amg" /><br />
    <!-- <button @click="get_amg">获取图片验证码</button><br> -->
    <button @click="login">注册</button>
  </div>
</template>

<script>
import { v4 } from "uuid";
import Axios from "axios";
export default {
  name: "Login",
  data() {
    return {
      account: "",
      password: "",
      phone: "",
      code: "",
      uuid: v4(),
      image_url: "http://127.0.0.1:5000/" + "user/code?uuid=" + this.uuid,
    };
  },
  methods: {
    get_amg() {
      this.uuid = v4();
      this.image_url = "http://127.0.0.1:5000/" + "user/code?uuid=" + this.uuid;
    },
    login() {
      Axios.post("user/register_users", {
        account: this.account,
        password: this.password,
        uuid: this.uuid,
        code: this.code,
        phone: this.phone,
      })
        .then((resp) => {
          console.log(resp.data);
          if (resp.data.code == "200") {
            alert("注册成功");
            this.$router.push("/login");
          }
          if (
            this.account == null ||
            this.phone == null ||
            this.password == null
          ) {
            alert("信息不完整");
            return false;
          }
          if (resp.data.code != "200") {
            alert("注册失败");
            this.get_amg();
          }
        })
        .catch();
    },
  },
};
</script>

<style>
</style>