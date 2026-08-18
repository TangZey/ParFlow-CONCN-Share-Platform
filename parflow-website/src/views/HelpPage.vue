<template>
  <div class="standard-page"><div class="page-label">使用指南 · GUIDE</div><h1>三步找到并准备<br>你的流域数据</h1><p class="page-description">平台围绕“定位、确认、下载”组织操作。当前为界面预览，连接校内数据服务后即可使用真实流域边界和文件。</p><div class="content-grid"><article v-for="item in steps" :key="item.no" class="content-card"><small>{{ item.no }} / {{ item.en }}</small><h2>{{ item.title }}</h2><p>{{ item.copy }}</p><span class="card-number">{{ item.no }}</span></article></div></div>
</template>
<script setup>
const steps=[{no:'01',en:'FIND',title:'找到流域',copy:'选择 Level 2 至 Level 14 的空间层级，再按名称、编号或所属水系缩小范围。'},{no:'02',en:'CHECK',title:'核对范围',copy:'在地图中确认边界、面积和坐标范围，确保流域单元符合研究需求。'},{no:'03',en:'DOWNLOAD',title:'准备数据',copy:'选择地形、土壤、覆盖或气象产品，生成标准化的数据下载任务。'}]
</script>
