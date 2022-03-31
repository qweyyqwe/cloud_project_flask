<template>
    <div>
        <div class="col-dm-12" v-for="(item,index) in data" :key="index">
            <a class="row" href="javascript:void(0);">
                <div class="col-xs-2">
                    <img :src="get_photo(item.img)">
                </div>
                <div class="col-xs-10">
                    <div>{{item.username}}-<i>L{{item.exp}}</i></div>
                    <div>{{item.time}}</div>
                </div>
            </a>
        </div>

    </div>

</template>

<script>
import {config} from '../../config'
export default {
    data() {
        return {
            config: '',
        }
    },
    beforeMount() {
		this.config = config
    },
    props: ['data'],
    mounted: function () {
    },
    methods: {
        get_photo(img) {
            if (img == '1.jpg') {
                return require('../../../static/img/1.jpg')
            } else {
                // return img 返回七牛云图片链接
                return config['qiniuurl'] + img
            }
        },
    },


}
</script>

<style>
.tabs {
    font-size: 18px;
}
.switchlist span {
    margin-top: 10px;
    border: 0;
}
</style>
