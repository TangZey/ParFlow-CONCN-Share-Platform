<template>
  <div id="app">
    <!-- ===== 顶部导航栏 ===== -->
    <el-container>
      <el-header height="70px" class="header">
        <div class="header-left">
          <!-- Logo 占位 -->
          <div class="logo">
            <span style="font-size: 24px; font-weight: bold; color: #2c6b9e;">🌊</span>
            <span style="font-size: 20px; font-weight: bold; color: #2c6b9e; margin-left: 8px;">流域数据</span>
          </div>
        </div>

        <div class="header-center">
          <!-- 横向菜单 -->
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            background-color="#ffffff"
            text-color="#333333"
            active-text-color="#2c6b9e"
            @select="handleMenuSelect"
            style="border-bottom: none;"
          >
            <el-menu-item index="/home">网站主页</el-menu-item>
            <el-sub-menu index="/data">
              <template #title>流域数据</template>
              <el-menu-item index="/data/view">流域数据</el-menu-item>
            </el-sub-menu>
            <el-menu-item index="/help">使用说明</el-menu-item>
            <el-menu-item index="/notice">公告</el-menu-item>
          </el-menu>
        </div>

        <div class="header-right">
          <el-button type="primary" size="small" @click="switchLanguage">English</el-button>
          <el-button type="primary" size="small" @click="handleLogin">登录/注册</el-button>
        </div>
      </el-header>

      <!-- ===== 页面内容区域 ===== -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeMenu: '/data/view'
    };
  },
  mounted() {
    this.activeMenu = this.$route.path;
  },
  methods: {
    handleMenuSelect(index) {
      this.$router.push(index);
      this.activeMenu = index;
    },
    switchLanguage() {
      alert('切换语言功能待开发');
    },
    handleLogin() {
      alert('登录/注册功能待开发');
    }
  },
  watch: {
    '$route.path'(newPath) {
      this.activeMenu = newPath;
    }
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.el-container {
  min-height: 100vh;
  flex-direction: column;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #ffffff;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  min-width: 160px;
}

.logo {
  display: flex;
  align-items: center;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.header-center .el-menu {
  width: 100%;
  max-width: 600px;
  display: flex;
  justify-content: space-around;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 180px;
  justify-content: flex-end;
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px 40px;
  flex: 1;
}

/* ===== 菜单字体放大加粗 ===== */
:deep(.el-menu-item),
:deep(.el-sub-menu .el-sub-menu__title) {
  font-size: 20px !important;
  font-weight: bold !important;
}

/* ===== 右侧按钮变大，字体与菜单一致 ===== */
:deep(.header-right .el-button) {
  font-size: 20px !important;
  font-weight: bold !important;
  padding: 14px 28px !important;
  height: auto !important;
}
</style>