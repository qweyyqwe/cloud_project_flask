// import axios from 'axios'
const axios = require('axios');
axios.defaults.baseURL = "http://127.0.0.1:5000";
export const base_url = "http://127.0.0.1:5000/"
// const axios = require('axios');
// axios.defaults.baseURL = 'http://127.0.0.1:5000/';
//全局设置网络超时
axios.defaults.timeout = 10000;

// axios.defaults.withCredentials = true;
//设置请求头信息
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.put['Content-Type'] = 'application/json';



axios.interceptors.request.use(
    config => {
        // 每次发送请求之前判断是否存在token，如果存在，则统一在http请求的header都加上token，不用每次请求都手动添加了
        var token = localStorage.getItem("token")
        if (token) {
            config.headers.Authorization = 'JWT ' + token
        }
        return config;
    },
    error => {
        return Promise.error(error);
    })

/**
 * 响应拦截器（当后端返回数据的时候进行拦截）
 * 例1：当后端返回状态码是401/403时，跳转到 /login/ 页面
 */
 axios.interceptors.response.use(response => {
  // 当响应码是 2xx 的情况, 进入这里
  // debugger
  return response.data;
}, error => {
  // 当响应码不是 2xx 的情况, 进入这里
  // debugger
  return error
});


// axios.interceptors.response.use(
//     // 请求成功
//     res => res.status === 200 ? Promise.resolve(res) : Promise.reject(res),

//     // 请求失败
//     error => {
//         if (error) {
//             // 判断一下返回结果的status == 401？  ==401跳转登录页面。  ！=401passs
//             console.log('err', error)
//             if (error.status === 401) {
//                 // 跳转不可以使用this.$router.push方法、
//                 // this.$router.push({path:'/login'})
//                 window.location.href = "http://192.168.1.119:5000/login"
//             } else {
//                 // errorHandle(response.status, response.data.message);
//                 return Promise.reject(error);
//             }
//             // 请求已发出，但是不在2xx的范围
//         } else {
//             // 处理断网的情况
//             // eg:请求超时或断网时，更新state的network状态
//             // network状态在app.vue中控制着一个全局的断网提示组件的显示隐藏
//             // 关于断网组件中的刷新重新获取数据，会在断网组件中说明
//             // store.commit('changeNetwork', false);
//             return Promise.reject(error);
//         }
//     });


// 封装xiaos请求

// 封装get请求
export function axios_get(url, params, headers) {
    return new Promise(
        (resolve, reject) => {
            axios.get(url, { params, headers })
                .then(res => {
                    // console.log("封装信息的的res", res)
                    resolve(res)
                }).catch(err => {
                    reject(err)
                })
        }
    )
}

// 封装post请求
export function axios_post(url, params, headers) {
    return new Promise(
        (resolve, reject) => {
            axios.post(url, params, headers)
                .then(res => {
                    resolve(res)
                }).catch(err => {
                    reject(err)
                })
        }
    )
}

// 封装put请求
export function axios_put(url, params, headers) {
    return new Promise(
        (resolve, reject) => {
            axios.put(url, params, headers)
                .then(res => {
                    resolve(res)
                }).catch(err => {
                    reject(err)
                })
        }
    )
}

// 封装delete请求
export function axios_delete(url, params, headers) {
    return new Promise(
        (resolve, reject) => {
            axios.delete(url, { params: data , headers})
                .then(res => {
                    // console.log("封装信息的的res", res)
                    resolve(res)
                }).catch(err => {
                    reject(err)
                })
        }
    )
}

// export default axios;
