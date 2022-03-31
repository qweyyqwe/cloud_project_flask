<template>
    <div>
        <div id="terminal" style="width: 500px; height: 300px;"></div>
    </div>
</template>

<script>
import { Terminal } from 'xterm';
import * as fit from 'xterm/lib/addons/fit/fit'
import * as attach from 'xterm/lib/addons/attach/attach'
Terminal.applyAddon(fit)
export default {
    data(){
        return {
            terminalSocket: null,
            term: null,
            order: ''
        }
    },
   // 页面创建钩子函数中添加事件监听
   created() {

   },
   mounted() {
    //    实例化一个websicket
       this.terminalSocket = new WebSocket('ws://127.0.0.1:8000/web/');
       this.terminalSocket.onmessage = (res) => {
           console.log(res.data);
           this.term.writeln('\r\n' + res.data);
           this.order = ''
           this.term.write('---------------------------------------------------------------\r\n~$ ');
       }
       let terminalContainer = document.getElementById('terminal')
       //创建一个xterm实例
       this.term = new Terminal({
           cursorBlink: true, //显示光标
           cursorStyle: 'underline' //光标样式
       })
       this.term.open(terminalContainer)
       this.term.write('$ ')
       this.term.on('key', (key, ev) => {
           console.log('key=========', ev.keyCode);
           this.term.write(key) 
           if (ev.keyCode == 13) {
               this.terminalSocket.send(this.order)
               console.log('里面的order:', this.order)
           }else if(ev.keyCode == 8){
               this.order = this.order.substr(0, this.order.lengthh+1)
               this.term.write('\x1b[2k\r')

               this.term.write('$ '+this.order)
               console.log('截取的字符串' + this.order)
               typeof this.order
           }else{
               this.order += key;
               console.log('外部order', this.order)
           }
       })
   },
   watch: {

   },
   methods: {


   },
   filters:{

   }
}

</script>
<style>
</style>