<template>
  <div class="sidebar-container">
    <div class="sidebar">
      <router-link to="/">Update</router-link>
      <router-link to="/about">Grouping</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
};
</script>

<style scoped>
.sidebar-container {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 30px; /* 初始宽度，可根据需要调整 */
  z-index: 1000;
  transition: width 0.3s ease; /* 添加过渡效果 */
}

.sidebar-container:hover {
  width: 200px; /* 鼠标悬停时的宽度，可根据需要调整 */
}

.sidebar {
  position: absolute;
  top: 0;
  left: 0;
  width: 150px; /* 侧边栏实际宽度 */
  height: 100vh;
  background-color: #2766b9;
  padding: 15px;
  transform: translateX(-100%); /* 初始状态隐藏在左侧 */
  transition: transform 0.35s ease; /* 添加过渡效果 */
}

.sidebar-container:hover .sidebar {
  transform: translateX(0); /* 鼠标悬停时显示侧边栏 */
}

.sidebar a {
  display: block;
  margin-bottom: 10px;
  text-decoration: none;
  font-weight:bold;
  color: #fafafa;
}

.sidebar a.router-link-active {
  font-weight: bold;
  color: #f8f9f9;
}
</style>