<template>
  <div class="home-page">
    <section class="home-hero">
      <div class="hero-copy">
        <span>PARFLOW · CONCN</span>
        <h1>为中国流域研究<br>准备的数据入口</h1>
        <p>从流域边界到模型输入，用统一的空间索引组织水文数据，让研究者更快进入计算与分析。</p>
        <div class="hero-actions"><RouterLink to="/data/view">探索流域数据 <i>→</i></RouterLink><RouterLink class="secondary" to="/help">了解如何使用</RouterLink></div>
        <div class="hero-status"><i></i><span>当前为内部测试环境，仅校园网可连接数据服务</span></div>
      </div>
      <div class="hero-map"><div class="map-halo"></div><img :src="basinMapUrl" alt="CONCN PFBAS2 一级流域分区图"><span>CONCN / PFBAS2 BASIN ZONES</span></div>
    </section>
    <section class="workflow">
      <header><span>从研究区域到模型数据</span><p>平台将数据准备整理为三个连续步骤。</p></header>
      <div class="workflow-steps"><article v-for="step in steps" :key="step.no"><b>{{ step.no }}</b><div><h2>{{ step.title }}</h2><p>{{ step.text }}</p></div><i>→</i></article></div>
    </section>
  </div>
</template>
<script setup>
import basinMapUrl from '../../../Fig/pfbas2_basins.png'

const steps=[{no:'01',title:'定位流域',text:'按名称、水系或空间层级找到研究单元。'},{no:'02',title:'核对数据',text:'确认空间范围、版本和可用数据产品。'},{no:'03',title:'准备下载',text:'生成面向 ParFlow 工作流的数据包。'}]
</script>
<style scoped>
.home-page{background:white}.home-hero{min-height:calc(100vh - 78px);padding:clamp(45px,6vw,90px) clamp(24px,6vw,90px);display:grid;grid-template-columns:minmax(380px,.85fr) minmax(500px,1.15fr);align-items:center;gap:4vw;overflow:hidden;background:linear-gradient(135deg,#fff 0,#fff 45%,#edf9fd 100%)}.hero-copy>span{color:var(--blue);font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.14em}.hero-copy h1{margin:17px 0;color:var(--navy);font-family:var(--display);font-size:clamp(45px,5.5vw,74px);font-weight:600;line-height:1.12;letter-spacing:-.055em}.hero-copy>p{max-width:560px;margin:0;color:var(--muted);font-size:15px;line-height:1.9}.hero-actions{margin-top:31px;display:flex;align-items:center;gap:15px}.hero-actions a{height:46px;padding:0 19px;display:flex;align-items:center;gap:24px;border-radius:24px;color:white;background:var(--navy);text-decoration:none;font-size:12px;font-weight:600}.hero-actions a:hover{background:var(--blue)}.hero-actions .secondary{color:#587388;background:transparent}.hero-actions .secondary:hover{color:var(--blue);background:var(--sky)}.hero-actions i{font-style:normal}.hero-status{margin-top:29px;display:flex;align-items:center;gap:8px;color:#8298a7;font-size:9px}.hero-status i{width:7px;height:7px;border-radius:50%;background:#ffb04a}.hero-map{position:relative;min-height:520px;display:flex;align-items:center;justify-content:center}.hero-map img{position:relative;z-index:2;width:110%;max-height:610px;object-fit:contain;filter:saturate(.9) drop-shadow(0 28px 38px rgba(17,93,132,.16))}.map-halo{position:absolute;width:80%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,#fff 0,rgba(255,255,255,.45) 50%,transparent 72%)}.hero-map>span{position:absolute;right:4%;bottom:6%;z-index:3;color:#6f9aaa;font-family:var(--mono);font-size:7px;letter-spacing:.13em}.workflow{padding:75px clamp(24px,6vw,90px);background:var(--navy)}.workflow>header{display:flex;align-items:flex-end;justify-content:space-between;color:white}.workflow>header span{font-family:var(--display);font-size:28px;font-weight:600}.workflow>header p{margin:0;color:#8eb2c9;font-size:11px}.workflow-steps{margin-top:35px;display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid rgba(255,255,255,.15)}.workflow-steps article{padding:27px 24px 10px 0;display:grid;grid-template-columns:38px 1fr auto;gap:15px;border-right:1px solid rgba(255,255,255,.12)}.workflow-steps article+article{padding-left:24px}.workflow-steps b{color:var(--cyan);font-family:var(--mono);font-size:10px}.workflow-steps h2{margin:0 0 7px;color:white;font-size:16px}.workflow-steps p{margin:0;color:#83a6bc;font-size:10px;line-height:1.7}.workflow-steps i{color:#5f8fa8;font-style:normal}@media(max-width:900px){.home-hero{min-height:auto;grid-template-columns:1fr}.hero-map{min-height:380px}.hero-map img{width:100%}.workflow-steps{grid-template-columns:1fr}.workflow-steps article,.workflow-steps article+article{padding:22px 0;border-right:0;border-bottom:1px solid rgba(255,255,255,.12)}}@media(max-width:600px){.home-hero{padding:48px 20px}.hero-copy h1{font-size:43px}.hero-actions{align-items:stretch;flex-direction:column}.hero-actions a{justify-content:space-between}.hero-map{min-height:270px}.workflow{padding:48px 20px}.workflow>header{align-items:flex-start;flex-direction:column;gap:10px}}
</style>
