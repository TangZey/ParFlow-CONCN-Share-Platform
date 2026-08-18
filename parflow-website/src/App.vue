<template>
  <div class="site-shell">
    <header class="site-header">
      <button class="menu-toggle" aria-label="打开导航" @click="menuOpen=true"><span></span><span></span></button>
      <RouterLink class="brand" to="/data/view" aria-label="CONCN DataHub">
        <img src="/new_logo.jpeg" alt="CONCN DataHub">
      </RouterLink>
      <nav :class="{open:menuOpen}" aria-label="主要导航">
        <button class="nav-close" aria-label="关闭导航" @click="menuOpen=false">×</button>
        <RouterLink to="/home" @click="menuOpen=false">首页</RouterLink>
        <RouterLink to="/data/view" @click="menuOpen=false">流域数据</RouterLink>
        <RouterLink to="/help" @click="menuOpen=false">使用指南</RouterLink>
        <RouterLink to="/notice" @click="menuOpen=false">平台动态</RouterLink>
      </nav>
      <div class="header-actions">
        <button class="language">中 / EN</button>
        <button class="login-button" @click="$router.push('/login')"><span>登录</span><i>→</i></button>
      </div>
    </header>
    <button v-if="menuOpen" class="nav-backdrop" aria-label="关闭导航" @click="menuOpen=false"></button>
    <main><RouterView /></main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const menuOpen=ref(false)
</script>

<style>
:root{
  --navy:#092a4a;--navy-2:#12446d;--blue:#168be0;--cyan:#42c9dd;
  --sky:#eaf7fc;--snow:#f8fbfe;--white:#fff;--text:#15344d;--muted:#6e879a;
  --line:#dbe8ef;--soft:#f0f6f9;--success:#25a779;
  --display:'Avenir Next','Helvetica Neue',Arial,sans-serif;
  --body:'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;
  --mono:'SFMono-Regular',Consolas,'Liberation Mono',monospace;
}
*{box-sizing:border-box}html,body,#app{min-height:100%;margin:0}body{color:var(--text);background:var(--snow);font-family:var(--body);-webkit-font-smoothing:antialiased}button,input,select{font:inherit}button,a{color:inherit}.site-shell{min-height:100vh}.site-header{position:relative;z-index:30;height:78px;padding:0 clamp(22px,4vw,64px);display:grid;grid-template-columns:220px 1fr auto;align-items:center;border-bottom:1px solid var(--line);background:rgba(255,255,255,.96);backdrop-filter:blur(18px)}.brand{width:190px;height:58px;display:flex;align-items:center;overflow:hidden}.brand img{width:185px;height:64px;object-fit:contain}.site-header nav{height:100%;display:flex;align-items:center;justify-content:center;gap:clamp(23px,3vw,48px)}.site-header nav a{position:relative;height:100%;display:flex;align-items:center;color:#587185;text-decoration:none;font-size:14px;font-weight:500;white-space:nowrap}.site-header nav a:after{content:'';position:absolute;left:0;right:0;bottom:-1px;height:3px;transform:scaleX(0);background:linear-gradient(90deg,var(--blue),var(--cyan));transition:transform .2s}.site-header nav a:hover,.site-header nav a.router-link-active{color:var(--navy)}.site-header nav a.router-link-active:after{transform:scaleX(1)}.header-actions{display:flex;align-items:center;gap:12px}.language{border:0;color:#7790a2;background:transparent;font-size:11px;cursor:pointer}.login-button{height:38px;padding:0 15px;display:flex;align-items:center;gap:15px;border:1px solid var(--navy);border-radius:20px;color:var(--navy);background:white;font-size:12px;font-weight:600;cursor:pointer;transition:.2s}.login-button:hover{color:white;background:var(--navy)}.login-button i{font-style:normal}.menu-toggle,.nav-close,.nav-backdrop{display:none}main{min-height:calc(100vh - 78px)}
.standard-page{max-width:1240px;margin:auto;padding:72px clamp(24px,6vw,88px)}.page-label{color:var(--blue);font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.13em}.standard-page h1{max-width:760px;margin:15px 0 17px;color:var(--navy);font-family:var(--display);font-size:clamp(38px,5vw,66px);font-weight:600;line-height:1.12;letter-spacing:-.045em}.page-description{max-width:660px;margin:0;color:var(--muted);font-size:15px;line-height:1.9}.content-grid{margin-top:50px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.content-card{min-height:220px;padding:27px;border:1px solid var(--line);border-radius:16px;background:white;box-shadow:0 12px 35px rgba(21,72,105,.055)}.content-card small{color:var(--blue);font-family:var(--mono);font-size:9px}.content-card h2{margin:23px 0 12px;color:var(--navy);font-family:var(--display);font-size:20px}.content-card p{margin:0;color:var(--muted);font-size:12px;line-height:1.8}.content-card .card-number{display:block;margin-top:28px;color:#d8e8ef;font-family:var(--display);font-size:42px;font-weight:600}.wide-card{grid-column:span 2}.accent-card{color:white;border:0;background:linear-gradient(135deg,#0a3d68,#126f9d)}.accent-card small,.accent-card h2,.accent-card p{color:white}.accent-card p{opacity:.75}
:focus-visible{outline:3px solid rgba(22,139,224,.25);outline-offset:3px}
@media(max-width:800px){.site-header{height:68px;padding:0 16px;grid-template-columns:1fr auto}.brand{width:155px;height:50px}.brand img{width:150px}.menu-toggle{width:36px;height:36px;margin-right:7px;display:grid;place-content:center;gap:5px;border:0;background:transparent}.menu-toggle span{width:19px;height:1px;background:var(--navy)}.site-header{grid-template-columns:auto 1fr auto}.site-header nav{position:fixed;z-index:32;left:0;top:0;bottom:0;width:min(310px,84vw);padding:92px 30px 30px;display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-start;gap:0;transform:translateX(-100%);background:white;transition:transform .25s}.site-header nav.open{transform:translateX(0)}.site-header nav a{width:100%;height:58px;border-bottom:1px solid var(--line);font-size:16px}.site-header nav a:after{display:none}.nav-close{position:absolute;right:20px;top:20px;display:block;border:0;background:transparent;font-size:25px}.nav-backdrop{position:fixed;inset:0;z-index:29;display:block;border:0;background:rgba(5,31,53,.4)}.language{display:none}.login-button{width:38px;padding:0;justify-content:center}.login-button span{display:none}.content-grid{grid-template-columns:1fr}.wide-card{grid-column:auto}.standard-page{padding:48px 20px}}
.brand{height:68px;overflow:visible}.brand img{display:block;height:auto}
@media(max-width:800px){.brand{height:58px}.brand img{height:auto}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;transition-duration:.01ms!important;animation-duration:.01ms!important;animation-iteration-count:1!important}}
</style>
