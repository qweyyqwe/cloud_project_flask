<template>
    <div>
        <div role="tabpanel" class="tab-pane active">

            <ul class="row question-items" v-for="(question,index) in questionlist" :key="index">

                <li class="question-item">
                    <div class="col-md-10">
                        <div class="col-sm-2 question-item-author">

                            <div class="user-avatar ">
                                <a class="avatar" href="../user/13/study.html" target="_blank">
                                    <img :src="src">
                                </a>

                            </div>

                        </div>
                        <div class="col-sm-10">
                            <h4>
                                <a class="question-item-title" href="show.html" target="_blank">{{ question.title }}</a>

                            </h4>
                            <div class="question-item-summary">

                                <div class="user-username ">
                                    <a class="avatar" href="../user/13/study.html" target="_blank">

                                        shiyanlouadmin

                                    </a>
                                    <span class="user-level">L14</span>
                                </div>

                                <span class="question-item-date">3小时前</span>

                                最后回复 <span class="question-item-date">

                                    <div class="user-username ">
                                        <a class="username" href="/user/256544" target="_blank">

                                            芃逆明

                                        </a>
                                        <span class="user-level">L38</span>
                                    </div>
                                </span>

                            </div>
                        </div>
                    </div>
                    <div class="col-md-2 question-item-rank">
                        <div class="question-item-answered">
                            <div>{{ question.count }}</div>
                            <div>回复</div>
                        </div>
                        <div class="question-item-views">
                            <div>{{ question.examine }}</div>
                            <div>查看</div>
                        </div>
                    </div>
                </li>
            </ul>

        </div>
    </div>
</template>

<script>
export default {
    props: ['questionlist', 'src']
}
</script>

<style>
</style>