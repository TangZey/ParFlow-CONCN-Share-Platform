<template>
  <div class="standard-page"><div class="page-label">平台动态 · UPDATES</div><h1>开发进展与<br>数据更新记录</h1><p class="page-description">正式公开前，我们会在这里说明平台状态、边界数据更新和服务调整。</p><div class="content-grid"><article v-for="item in notes" :key="item.title" class="content-card" :class="{'accent-card':item.featured}"><small>{{ item.date }} · {{ item.tag }}</small><h2>{{ item.title }}</h2><p>{{ item.copy }}</p></article></div></div>
</template>
<script setup>
const notes=[{date:'2026.08',tag:'PREVIEW',title:'新版数据界面进入内部评审',copy:'地图浏览、层级筛选和流域详情使用新的信息结构进行展示。',featured:true},{date:'2026.08',tag:'PERFORMANCE',title:'高等级边界支持视窗加载',copy:'精细流域不再一次性加载全国数据，以减少等待和浏览器渲染压力。'},{date:'INTERNAL',tag:'ACCESS',title:'数据服务仍限校园网络',copy:'公开前仅组内成员可以访问集群数据，本地前端可在无数据条件下预览。'}]
</script>
