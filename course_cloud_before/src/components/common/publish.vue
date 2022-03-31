<template>
    <div>

        <div v-if="token">
            <mavon-editor @save="saveDoc" @change="updateDoc" ref="editor" v-model="doc" :toolbars="toolbars" :subfield='false' defaultOpen="edit">
            </mavon-editor>
            <br />
            <Button color='green' @click='submit' v-if="!sid">发表实验评论</Button>
            <Button color='green' @click='submit_report' v-if="sid">发表实验报告</Button>
        </div>
        <div v-else>
            <br />
            <Button color='green'>登录后发表实验评论</Button>
        </div>
    </div>
</template>

<script>
import marked from 'marked'
import { mavonEditor } from 'mavon-editor'
import "mavon-editor/dist/css/index.css";
import { config, formatXml } from '../../config.js';
import { publish_comment_post,report_content_post } from '../axios_api/api';
export default {

    data() {
        return {
            doc: "",
            toolbars: {
                bold: true, // 粗体
                italic: true, // 斜体
                header: true, // 标题
                underline: true, // 下划线
                strikethrough: true, // 中划线
                mark: true, // 标记
                superscript: true, // 上角标
                subscript: true, // 下角标
                quote: true, // 引用
                ol: true, // 有序列表
                ul: true, // 无序列表
                link: true, // 链接
                imagelink: false, // 图片链接
                code: false, // code
                table: true, // 表格
                fullscreen: true, // 全屏编辑
                readmodel: true, // 沉浸式阅读
                htmlcode: true, // 展示html源码
                help: true, // 帮助
                /* 1.3.5 */
                undo: true, // 上一步
                redo: true, // 下一步
                trash: true, // 清空
                save: true, // 保存（触发events中的save事件）
                /* 1.4.2 */
                navigation: true, // 导航目录
                /* 2.1.8 */
                alignleft: true, // 左对齐
                aligncenter: true, // 居中
                alignright: true, // 右对齐
                /* 2.2.1 */
                subfield: true, // 单双栏模式
                preview: true, // 预览
            },
        }
    },
    props: ['token', 'ques_id', 'cid', 'sid'],
    components: {
        mavonEditor,
    },

    methods: {
        // 发表报告
        submit_report() {
            if (this.doc == '') {
                this.$Message('您还未输入报告内容')
                return false
            }
            var data = { content: marked(this.doc), token: localStorage.getItem('token'), cid: this.cid, sid: this.sid }
            report_content_post(data).then(resp => {
                this.$Message('发表成功')
                
            }
            )
            this.reply_opened = []
        },
        // 发表评论
        submit() {
            if (this.doc == '') {
                this.$Message('您还未输入评论内容')
                return false
            }
            var data = { content: marked(this.doc), token: localStorage.getItem('token'), ques_id: this.ques_id }
            publish_comment_post(data).then(resp => {
                this.$Message(resp.message)
                this.$router.go(0)
            }
            )
            this.reply_opened = []
        },
        updateDoc(markdown, html) {
            // 此时会自动将 markdown 和 html 传递到这个方法中
            console.log("markdown内容: " + markdown);
            console.log("html内容:" + markdown);
        },
        saveDoc(markdown, html) {
            // 此时会自动将 markdown 和 html 传递到这个方法中
            console.log("markdown内容:" + markdown);
            console.log("html内容:" + html);
        }
    }
}
</script>

<style>
</style>
