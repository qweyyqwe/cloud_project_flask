<template>
    <div>
        <video id="video" :src="video" width="720" height="540" autoplay controls>
            Video player not available.
        </video>

        <br>
        <h3>发表实验报告</h3>
        <div>
            <publish :token='token' :cid='cid' :sid='sid'></publish>
        </div>
    </div>
</template>
<script>
import lab_head from './common/lab_head';
import lab_header from './common/lab_header';
import lab_footer from './common/lab_footer';
import user_info from './common/user_info';
import last_paths from './common/last_paths';
import QR_code from './common/QR_code';
import lab_sidebar from './common/lab_sidebar';
import publish from './common/publish'
import { courserecord, sectionvideo_get } from './axios_api/api';
import { config, formatXml } from '../config.js';
export default {
    data() {
        return {
            video: '',
            token: '',
            cid: '',
            sid: '',
        }
    },
    beforeMount() {
    },
    created() {
    },
    mounted() {
        this.get_course();
        this.get_video();
        this.token = localStorage.getItem('token');
        this.cid = this.$route.query.cid;
		this.sid = this.$route.query.sid;
		console.log(this.cid)
    },
    methods: {
        get_video() {
            var sid = this.$route.query.sid;
            var params = { sid: sid }
            sectionvideo_get(params).then(resp => {
                this.video = config['qiniuurl'] + resp.video
            })
        },
        get_course() {
            var token = localStorage.getItem('token');
            var sid = this.$route.query.sid;
            courserecord({ sid: sid, token: token }).then(res => {
                console.log(res)
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
        lab_sidebar,
        publish,
    }
}
</script>

<style>
</style>