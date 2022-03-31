//将我们http.js中封装好的  get,post.put,delete  导过来

import { axios_get, axios_post, axios_delete, axios_put } from './http.js'


//按照格式确定方法名
export const jwt_send_get = p => axios_post("/api/login", p)

export const login_post = p => axios_post("/api/course_login", p)

export const register_post = p => axios_post("register", p)

export const getcourses_get = p => axios_get('/getcourses/', p)

export const getcourses1_get = p => axios_get('/getcourses1/', p)

export const get_course_info_get = p => axios_get('/courseinfo/', p)

export const gettags_get = p => axios_get('/get_tags/', p)

export const user_info_get = p => axios_get('/user_info/', p)

export const user_info_post = p => axios_post('/user_info/', p)

export const send_phone_code_post = p => axios_post('/api/sendalysms/', p)

export const verif_post = p => axios_post("/verif/", p)


//获取路径列表信息
export const getpaths_get = p => axios_get('/getpath/', p)

//获取单个路径信息
export const get_path_info_get = p => axios_get('getpathinfo/', p)

//获取热门路径信息
export const get_hot_path_get = p => axios_get('gethotpath/', p)

//路径关注 / 取关接口
export const path_follow_get = p => axios_get('pathfollow/', p)

//进入路径页面判断用户是否已经关注
export const is_path_follow_get = p => axios_get('ispathfollow/', p)




// 获取单个商品信息
export const course_show_get = p => axios_get("/courseinfo/", p)

// 获取作者信息
export const auth_info_get = p => axios_get("/authinfo/", p)
// 获取作者作品总数
export const course_count_get = p => axios_get("/coursecount/", p)
// 获取用户学习状态信息
export const user_lean_get = p => axios_get("/learninfo/", p)
// 用户添加课程
export const insert_learn_get = p => axios_get("/insertlearn/", p)

// 会员页面展示---请求会员列表接口
export const get_vip_list_get = p => axios_get('/vip_list/', p)

// 会员订单接口
export const get_vip_order_get = p => axios_get('/create_order/', p)

// 沙箱支付接口
export const get_alipay_get = p => axios_get('/alipay/', p)

// 订单入库库接口
export const get_order_mysql_post = p => axios_post('/alipay/', p)

// 支付成功后，请求后端修改数据库参数
export const get_succeed_get = p => axios_get('/get_alipy/', p)

// 获取七牛云token
export const get_uptoken = p => axios_get('/uptoken/', p)

// 获取用户信息
export const user_get = p => axios_get('/getuser/', p)

// 学习记录
export const courserecord = p => axios_get('/courserecord/', p)

// 获取评论
export const get_comments_get = p => axios_get('/get_comments/', p)

// 获取帖子
export const get_questions_get = p => axios_get('/get_questions/', p)

// 点赞评论
export const favorite_comment_post = p => axios_post('/favorite_comment/', p)

// 发表评论
export const publish_comment_post = p => axios_post('/publish_comment/', p)

// 训练营详情
export const drillcourse = p => axios_get('/drillcourse/', p)

// 获取视频
export const sectionvideo_get = p => axios_get('/sectionvideo/', p)

// 获取用户(实验课程(学习的 & 关注的 & 发布的) & 实验报告 & 实验讨论)
export const learn_get = p => axios_get('/learnview/', p)

// 访客添加接口
export const add_visitor_post = p => axios_post('/visitor/', p)

// 获取访客
export const get_visitor = p => axios_get('/visitor/', p)
// 生成优惠券
export const create_coupon_get = p => axios_get('/create_coupon/', p)

// 获取优惠券
export const coupon_list_get = p => axios_get('/coupon_list/', p)

// 获取实验豆
export const get_bean = p => axios_get('/getblan/', p)

// 秒杀购买成功后数量处理请求
export const purchase_get = p => axios_get('/purchase/', p)

// 活动页面加载
export const seckill_data_get = p => axios_get('/seckill_data/', p)

// 全局搜索
export const search_data_get = p => axios_get('/abc/', p)
// 课程推荐
export const reco_course_get = p => axios_get('/reco_course/', p)

// 发表报告
export const report_content_post = p => axios_post('/add_report/', p)

// 展示实验报告
export const report_list_get = p => axios_get('/repor_tlist/', p)
