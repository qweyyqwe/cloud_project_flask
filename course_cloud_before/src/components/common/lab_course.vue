<template>
    <div>
        <div class="tab-content">
            <div role="tabpanel" class="tab-pane active">
                <div class="row">
                    <div class="col-md-4 col-sm-6  course" v-for="(course,index) in courselist" :key="index">
                        <a class="course-box" :href="'/courses/course_show/?id=' + course.id">
                            <div class="sign-box">

                            </div>
                            <div class="course-img">
                                <!-- 封面 -->
                                <img :alt="course.name" :src="course.img">

                            </div>

                            <div class="course-body">
                                <!-- 标题 -->
                                <span class="course-title" data-toggle="tooltip" data-placement="bottom" title="Hadoop部署及管理">{{ course.name }}</span>
                            </div>
                            <div class="course-footer">
                                <span class="course-per-num pull-left">
                                    <i class="fa fa-users"></i>
                                    <!-- 收藏数 -->
                                    {{ course.collect_num }}
                                </span>
                                <!-- 免费 & 限免 & 会员 & 训练营 -->
                                <span class="course-money pull-right" v-if="course.category === '限免' | '会员'">{{ course.category }}</span>
                                <span class="course-money pull-right" style="background:#FF6666" v-if="course.category === '训练营'">{{ course.category }}</span>
                            </div>
                        </a>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ['courselist'],
}
</script>

<style>
.course-box {
    background: FF6666;
}
</style>