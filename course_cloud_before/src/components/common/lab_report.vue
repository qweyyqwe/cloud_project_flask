<template>
    <div>

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

                                    </a>
                                    <span class="user-level"><i>L</i>{{ report.exper | exper_filter }}</span>
                                </div>

                            </div>
                        </div>
                        <!-- <div class="col-xs-4">
                                <div class="pull-right report-item-comments">
                                    <i class="fa fa-comments-o"></i>
                                    0
                                </div>
                                <div class="pull-right report-item-update">
                                    3小时前
                                </div>
                            </div> -->
                    </div>

                </div>
            </div>
        </div>

    </div>
</template>

<script>
import { config } from '../../config'
export default {
    props: ['reportlist'],
    data() {
        return {
            config: ''
        }
    },
    mounted() {
        this.config = config
    },
    methods: {
        userphoto(photo) {
            if (photo === '1.jpg') {
				return config['uploadurl'] + photo
            }else{
				return config['qiniuurl'] + photo
			}
        },
	},
	filters:{
		exper_filter(value){
			return value / 10
		},
		content_filter(value){
			return value.length
		}
	}

}
</script>

<style>
</style>