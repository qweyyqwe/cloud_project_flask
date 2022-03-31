
<template>
  <div>
    账号：<input v-model="account" placeholder="账号"><br/>
    密码：<input v-model="password" type="password" placeholder="密码"><br/>
    <!-- 获取图形验证码 -->
    <!-- <input type="text" class="form_control" name='graph_captcha' placeholder="图形验证码" v-model="imgcode">
    <span class="input-group-addon captcha-addon">  加一个类captcha-addon
      <img @click="getImage" id="captcha-img" :src="image_url">加一个id  captcha-img
    </span> -->
    图片验证码
    <img id="captcha_img" :src="image_url" @click="getImage"><br><br>
    <button @click="resetForm">登录</button>
  </div>
</template>

<script>
import { post } from "../../utils/request";
// import { base_url } from '@components/axios_api/http.js';
import { v4 } from "uuid"
export default {
  name: "Login",
  data() {
    return {
      ruleForm: {
        phone: "",
        account: "",
        password: "",
        uuid: v4(),
        image_url: "http://127.0.0.1:5000/" + 'api/verification_code?uuid=' + this.uuid,
      },
    };
  },
  methods: {
    getImage() {
      this.uuid = v4()
      this.image_url = "http://127.0.0.1:5000/" + 'api/verification_code?uuid=' + this.uuid

      // post("api/verification_code/", { mobile: formName })
      //   .then((resp) => {
      //     console.log(resp.data);
      //   })
      //   .catch((err) => {
      //     console.log(err);
      //   });
    },
    resetForm() {
      post("api/course_login", {"account":this.account,"password":this.password,"uuid":this.uuid})
        .then((resp) => {
          console.log(resp.data)
          if(resp.data.code == "200"){
            alert("登录成功")
            this.$router.push('home')
          }
          if(resp.data.code != "200"){
              alert("登录失败")
              this.get_amg()            
              }
          })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
