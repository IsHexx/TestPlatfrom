<template>
  <div class="menu_list">
    <el-menu background-color="#b9e3c3"
             text-color="#000000"
             active-text-color="#ffffff"
             default-active="/index/myHome"
             class="el-menu-vertical-demo"
             router>
      <el-menu-item index="/index/myHome"><i class="el-icon-house"></i>首页</el-menu-item>
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-location"></i><span>UI自动化</span></template>
        <el-menu-item index="/index/elementManage">元素库</el-menu-item>
        <el-menu-item index="/index/caseManage">用例库</el-menu-item>
        <el-menu-item index="/index/menu3">测试报告</el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
import method from 'bluebird/js/release/method';

export default {
  name: "Navigation",
  methods: {
    handleOpen(key, keyPath) {
      console.log("打开", key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log("关闭", key, keyPath);
    },
    handSelect(key, keyPath) {
      console.log("选择", key, keyPath);
    }
  }
}
</script>

<style scoped>

.menu_list {
  margin-bottom: 0px;
  text-align: left;
  height: 100%;

}

.el-menu-vertical-demo {
  height: 100%;
}
</style>
