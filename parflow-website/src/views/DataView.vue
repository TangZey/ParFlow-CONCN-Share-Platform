<template>
  <div class="explorer">
    <aside class="explorer-panel">
      <div class="panel-heading">
        <span>CONCN BASIN EXPLORER</span>
        <h1>探索中国<br>流域数据</h1>
        <p>选择流域层级和数据类型，在地图中定位你的研究区域。</p>
      </div>

      <div class="search-control">
        <label for="basin-search">搜索流域</label>
        <div><input id="basin-search" v-model="keyword" placeholder="输入名称或流域编号" @keyup.enter="search"><button aria-label="搜索" @click="search">⌕</button></div>
      </div>

      <fieldset class="level-control">
        <legend><span>流域层级</span><strong>Level {{ level }}</strong></legend>
        <div class="level-options"><button v-for="item in levels" :key="item" :class="{active:item===level}" @click="level=item">{{ item }}</button></div>
        <p>层级越高，流域单元越精细</p>
      </fieldset>

      <label class="select-control">所属水系
        <span><select v-model="river"><option value="">全部水系</option><option>长江流域</option><option>黄河流域</option><option>珠江流域</option><option>海河流域</option></select><i>⌄</i></span>
      </label>

      <div class="product-control">
        <span>需要的数据</span>
        <div class="product-chips"><button v-for="product in products" :key="product.name" :class="{active:product.active}" @click="product.active=!product.active"><i>✓</i>{{ product.name }}</button></div>
      </div>

      <button class="search-action" @click="search"><span>在地图中查找</span><i>→</i></button>

      <div class="preview-note"><span>预览模式</span><p>当前页面不连接本地流域数据。你仍然可以体验完整的界面和交互。</p></div>
    </aside>

    <section class="map-area">
      <header class="map-header">
        <div><span class="online-dot"></span><strong>全国流域视图</strong><small>界面预览</small></div>
        <div class="map-view-options"><button class="active">地形</button><button>边界</button><button>河网</button></div>
      </header>

      <div class="map-viewport">
        <div class="map-grid"></div>
        <div class="map-caption"><span>CONCN / CHINA</span><strong>国家尺度水文数据底图</strong></div>
        <div class="map-image-wrap">
          <img src="/logo.png" alt="中国水文地形示意图">
          <button v-for="basin in basins" :key="basin.id" class="basin-marker" :class="[{selected:selection?.id===basin.id},basin.className]" @click="selectBasin(basin)"><i></i><span>{{ basin.name }}</span></button>
        </div>
        <div class="zoom-tools"><button aria-label="放大">＋</button><button aria-label="缩小">−</button><button aria-label="定位">⌖</button></div>
        <div class="map-coordinate"><span>80°E</span><i></i><span>120°E</span></div>

        <transition name="result">
          <article v-if="selection" class="basin-result">
            <button class="result-close" aria-label="关闭" @click="selection=null">×</button>
            <span>已选择流域</span><h2>{{ selection.name }}</h2>
            <dl><div><dt>编号</dt><dd>{{ selection.id }}</dd></div><div><dt>层级</dt><dd>Level {{ level }}</dd></div><div><dt>数据类型</dt><dd>{{ activeProductCount }} 项</dd></div></dl>
            <button class="detail-action">查看数据详情 <i>→</i></button>
          </article>
        </transition>
        <div v-if="feedback" class="search-feedback"><i>✓</i><span><strong>已定位演示流域</strong><small>当前未连接真实数据</small></span></div>
      </div>

      <footer class="map-footer">
        <div class="legend"><span><i class="terrain-key"></i>水文地形</span><span><i class="marker-key"></i>可选流域</span></div>
        <div class="scale"><span></span><small>500 km</small></div>
        <div>数据参考 · EPSG:4326</div>
      </footer>
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
const levels=[2,4,6,8,10,12,14]
const level=ref(4),keyword=ref(''),river=ref(''),selection=ref(null),feedback=ref(false)
const products=ref([{name:'地形高程',active:true},{name:'土壤地质',active:true},{name:'土地覆盖',active:false},{name:'气象驱动',active:false}])
const basins=[{id:'CJ-0201',name:'长江上游',className:'marker-yangtze'},{id:'HH-0108',name:'黄河中游',className:'marker-yellow'},{id:'ZJ-0402',name:'珠江流域',className:'marker-pearl'}]
const activeProductCount=computed(()=>products.value.filter(item=>item.active).length)
function selectBasin(basin){selection.value=basin}
function search(){const name=keyword.value||river.value||'长江上游';selection.value={id:'DEMO-0201',name};feedback.value=true;window.setTimeout(()=>feedback.value=false,2200)}
</script>

<style scoped>
.explorer{height:calc(100vh - 78px);min-height:650px;display:grid;grid-template-columns:370px minmax(0,1fr);overflow:hidden;background:white}.explorer-panel{padding:34px 38px 25px;overflow:auto;border-right:1px solid var(--line);background:white}.panel-heading>span{color:var(--blue);font-family:var(--mono);font-size:9px;font-weight:700;letter-spacing:.12em}.panel-heading h1{margin:12px 0 11px;color:var(--navy);font-family:var(--display);font-size:38px;font-weight:600;line-height:1.12;letter-spacing:-.04em}.panel-heading p{margin:0;color:var(--muted);font-size:12px;line-height:1.75}.search-control{margin-top:28px}.search-control label,.select-control,.product-control>span{display:block;color:#4e697c;font-size:11px;font-weight:600}.search-control>div{height:44px;margin-top:9px;display:flex;border:1px solid var(--line);border-radius:10px;background:var(--snow);transition:.2s}.search-control>div:focus-within{border-color:var(--blue);box-shadow:0 0 0 3px rgba(22,139,224,.09)}.search-control input{min-width:0;flex:1;padding:0 13px;border:0;outline:0;color:var(--navy);background:transparent;font-size:12px}.search-control button{width:44px;border:0;color:var(--blue);background:transparent;cursor:pointer;font-size:18px}.level-control{margin:24px 0 0;padding:20px 0 0;border:0;border-top:1px solid var(--line)}.level-control legend{width:100%;display:flex;justify-content:space-between;color:#4e697c;font-size:11px;font-weight:600}.level-control legend strong{color:var(--blue);font-family:var(--mono);font-size:9px}.level-options{margin-top:12px;display:grid;grid-template-columns:repeat(7,1fr);gap:5px}.level-options button{height:32px;padding:0;border:1px solid var(--line);border-radius:7px;color:#7590a2;background:white;font-family:var(--mono);font-size:9px;cursor:pointer}.level-options button:hover{border-color:#9bcaea;color:var(--blue)}.level-options button.active{border-color:var(--blue);color:white;background:var(--blue);box-shadow:0 5px 12px rgba(22,139,224,.2)}.level-control p{margin:8px 0 0;color:#9aabb7;font-size:9px}.select-control{margin-top:20px;padding-top:20px;border-top:1px solid var(--line)}.select-control>span{position:relative;display:block;margin-top:9px}.select-control select{width:100%;height:42px;padding:0 36px 0 12px;appearance:none;border:1px solid var(--line);border-radius:9px;outline:0;color:#547084;background:var(--snow);font-size:11px}.select-control i{position:absolute;right:13px;top:10px;color:#8399a9;font-style:normal}.product-control{margin-top:20px;padding-top:19px;border-top:1px solid var(--line)}.product-chips{margin-top:10px;display:flex;flex-wrap:wrap;gap:7px}.product-chips button{height:30px;padding:0 10px;border:1px solid var(--line);border-radius:16px;color:#708899;background:white;font-size:10px;cursor:pointer}.product-chips button i{display:none;margin-right:4px;font-style:normal}.product-chips button.active{border-color:#9fdbe6;color:#117d94;background:#ecfbfd}.product-chips button.active i{display:inline}.search-action{width:100%;height:46px;margin-top:23px;padding:0 16px;display:flex;align-items:center;justify-content:space-between;border:0;border-radius:10px;color:white;background:linear-gradient(90deg,var(--blue),#20a9d2);box-shadow:0 10px 22px rgba(20,139,204,.2);font-size:12px;font-weight:600;cursor:pointer;transition:.2s}.search-action:hover{transform:translateY(-1px);box-shadow:0 13px 25px rgba(20,139,204,.28)}.search-action i{font-style:normal;font-size:16px}.preview-note{margin-top:17px;padding:12px 13px;border-radius:9px;background:var(--soft)}.preview-note span{color:var(--blue);font-size:9px;font-weight:700}.preview-note p{margin:4px 0 0;color:#8196a5;font-size:9px;line-height:1.55}
.map-area{min-width:0;display:grid;grid-template-rows:55px minmax(0,1fr) 42px;background:var(--sky)}.map-header{padding:0 20px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(88,151,180,.16);background:rgba(255,255,255,.58)}.map-header>div:first-child{display:flex;align-items:center;gap:8px}.map-header strong{font-size:11px}.map-header small{padding-left:8px;border-left:1px solid #c5dce6;color:#7e98a7;font-size:9px}.online-dot{width:7px;height:7px;border-radius:50%;background:var(--success);box-shadow:0 0 0 4px rgba(37,167,121,.1)}.map-view-options{padding:3px;display:flex;border:1px solid rgba(112,170,196,.2);border-radius:18px;background:rgba(255,255,255,.65)}.map-view-options button{height:27px;padding:0 13px;border:0;border-radius:14px;color:#7290a1;background:transparent;font-size:9px;cursor:pointer}.map-view-options button.active{color:var(--navy);background:white;box-shadow:0 3px 9px rgba(20,73,104,.09)}.map-viewport{position:relative;min-height:0;overflow:hidden;background:radial-gradient(circle at 52% 48%,#fff 0,#f4fbfd 45%,#e5f4f9 100%)}.map-grid{position:absolute;inset:0;opacity:.42;background-image:linear-gradient(rgba(45,126,157,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(45,126,157,.08) 1px,transparent 1px);background-size:82px 82px;mask-image:radial-gradient(circle,#000,transparent 82%)}.map-caption{position:absolute;z-index:3;left:24px;top:22px}.map-caption span,.map-caption strong{display:block}.map-caption span{color:#68a2b8;font-family:var(--mono);font-size:7px;letter-spacing:.12em}.map-caption strong{margin-top:4px;color:#547d8f;font-size:11px}.map-image-wrap{position:absolute;left:8%;right:7%;top:8%;bottom:6%;display:flex;align-items:center;justify-content:center}.map-image-wrap>img{max-width:100%;max-height:100%;object-fit:contain;filter:saturate(.87) drop-shadow(0 18px 28px rgba(21,95,130,.13));user-select:none}.basin-marker{position:absolute;z-index:5;padding:0;border:0;background:transparent;cursor:pointer}.basin-marker i{width:14px;height:14px;display:block;border:3px solid white;border-radius:50%;background:var(--blue);box-shadow:0 3px 12px rgba(7,67,107,.32);transition:.2s}.basin-marker span{position:absolute;left:17px;top:-3px;padding:4px 7px;border-radius:5px;color:#345e76;background:rgba(255,255,255,.88);box-shadow:0 4px 12px rgba(28,91,124,.08);font-size:8px;white-space:nowrap;opacity:0;transform:translateX(-4px);transition:.2s}.basin-marker:hover i,.basin-marker.selected i{transform:scale(1.2);background:var(--cyan)}.basin-marker:hover span,.basin-marker.selected span{opacity:1;transform:none}.marker-yangtze{left:55%;top:63%}.marker-yellow{left:61%;top:46%}.marker-pearl{left:67%;top:79%}.zoom-tools{position:absolute;z-index:6;right:20px;top:23px;display:grid;overflow:hidden;border:1px solid rgba(68,133,160,.24);border-radius:9px;background:rgba(255,255,255,.88);box-shadow:0 7px 20px rgba(20,75,106,.08)}.zoom-tools button{width:34px;height:34px;border:0;border-bottom:1px solid var(--line);color:#527a8f;background:transparent;cursor:pointer}.zoom-tools button:last-child{border-bottom:0}.map-coordinate{position:absolute;left:26px;right:25px;bottom:15px;display:flex;align-items:center;gap:8px;color:#80a2b1;font-family:var(--mono);font-size:7px}.map-coordinate i{height:1px;flex:1;background:linear-gradient(90deg,transparent,#99c4d3,transparent)}.basin-result{position:absolute;z-index:8;right:22px;bottom:22px;width:260px;padding:19px;border:1px solid rgba(145,194,214,.45);border-radius:14px;background:rgba(255,255,255,.94);box-shadow:0 18px 45px rgba(20,75,105,.16);backdrop-filter:blur(12px)}.result-close{position:absolute;right:12px;top:10px;border:0;color:#89a0ae;background:transparent;cursor:pointer;font-size:16px}.basin-result>span{color:var(--blue);font-size:8px;font-weight:700}.basin-result h2{margin:6px 0 14px;color:var(--navy);font-family:var(--display);font-size:21px}.basin-result dl{margin:0}.basin-result dl>div{padding:7px 0;display:flex;justify-content:space-between;border-top:1px solid var(--line);font-size:9px}.basin-result dt{color:#8499a7}.basin-result dd{margin:0;color:#3c6074;font-family:var(--mono)}.detail-action{width:100%;height:36px;margin-top:12px;padding:0 11px;display:flex;align-items:center;justify-content:space-between;border:0;border-radius:8px;color:white;background:var(--navy);font-size:9px;cursor:pointer}.detail-action i{font-style:normal}.search-feedback{position:absolute;z-index:9;left:50%;top:22px;transform:translateX(-50%);padding:10px 14px;display:flex;align-items:center;gap:9px;border-radius:10px;color:white;background:var(--navy);box-shadow:0 12px 25px rgba(4,43,72,.18)}.search-feedback>i{width:20px;height:20px;display:grid;place-items:center;border-radius:50%;color:var(--navy);background:var(--cyan);font-size:10px;font-style:normal}.search-feedback strong,.search-feedback small{display:block;font-size:9px}.search-feedback small{margin-top:2px;color:#9cc4d3;font-size:7px}.result-enter-active,.result-leave-active{transition:.22s}.result-enter-from,.result-leave-to{opacity:0;transform:translateY(8px)}.map-footer{padding:0 20px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;border-top:1px solid rgba(88,151,180,.18);color:#7692a1;background:rgba(255,255,255,.66);font-size:8px}.legend{display:flex;gap:14px}.legend span{display:flex;align-items:center;gap:5px}.legend i{display:inline-block}.terrain-key{width:13px;height:5px;background:linear-gradient(90deg,#245ebd,#77dfdb)}.marker-key{width:7px;height:7px;border-radius:50%;background:var(--blue)}.scale{display:flex;align-items:center;gap:7px}.scale span{width:70px;height:5px;border-left:1px solid #6d8d9c;border-right:1px solid #6d8d9c;border-bottom:1px solid #6d8d9c}.map-footer>div:last-child{text-align:right;font-family:var(--mono)}
@media(max-width:980px){.explorer{grid-template-columns:330px 1fr}.explorer-panel{padding:28px 25px}.panel-heading h1{font-size:33px}.map-image-wrap{left:4%;right:4%}}
@media(max-width:760px){.explorer{height:auto;min-height:calc(100vh - 68px);display:block;overflow:visible}.explorer-panel{padding:28px 20px;border-right:0}.panel-heading h1 br{display:none}.map-area{height:620px}.map-header{position:sticky;top:68px;z-index:9}.map-caption{left:16px}.map-image-wrap{left:0;right:0}.basin-result{left:14px;right:14px;width:auto}.map-footer{grid-template-columns:1fr auto}.map-footer>div:last-child{display:none}}
</style>
