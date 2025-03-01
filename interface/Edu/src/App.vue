<!-- App.vue -->
<template>
  <div id="app">
    <!-- 登录后才显示侧边栏 -->
    <Sidebar v-if="isLoggedIn" />
    
    <!-- 登录注册模态框 -->
    <LoginRegisterModal 
      :isOpen="isModalOpen"
      @login-success="onLoginSuccess"
      @close="isModalOpen = false"
    />
    
    <!-- 登录按钮 -->
    <button 
      v-if="!isLoggedIn"
      @click="openModal"
      class="login-button"
    >
      Login/Register
    </button>
    
    <!-- 主内容区域 -->
    <router-view v-if="isLoggedIn"></router-view>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import LoginRegisterModal from './components/LoginRegisterModal.vue';

export default {
  components: {
    Sidebar,
    LoginRegisterModal
  },
  data() {
    return {
      isModalOpen: false,
      isLoggedIn: false // 实际项目中建议使用Vuex或本地存储
    };
  },
  methods: {
    openModal() {
      this.isModalOpen = true;
    },
    onLoginSuccess() {
      this.isLoggedIn = true;
      this.isModalOpen = false; // 登录成功后关闭模态框
    }
  }
};
</script>

<style>
/* 整体布局 */
#app {
  position: relative;
  min-height: 100vh;
}

/* 登录按钮样式 */
.login-button {
  position: fixed;
  top: 150px;
  right: 540px;
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
  transition: background 0.3s;
}

.login-button:hover {
  background: #0056b3;
}

/* 其他原有样式 */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

.sidebar {
  width: 200px;
  background-color: #f4f4f4;
  padding: 15px;
  height: 100vh;
  position: fixed;
  left: 0;
}

.content {
  padding: 15px;
  margin-left: 200px;
}

a {
  display: block;
  margin-bottom: 10px;
  text-decoration: none;
  color: #333;
}

a.router-link-active {
  font-weight: bold;
  color: #007bff;
}
</style>