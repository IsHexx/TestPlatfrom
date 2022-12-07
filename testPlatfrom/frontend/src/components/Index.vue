<template>
  <el-container class="index-con">
    <el-header class='m-header'>
      <my-header/>
    </el-header>
    <el-container>
      <el-aside style="width: 200px">
        <Navigation/>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import myHeader from "../views/myHeader";
import Navigation from "../views/Navigation.vue";
import MyHome from "./myHome.vue";

export default {
  name: 'Index',
  components: {myHeader, Navigation, MyHome},
  props: {
    msg: String
  }
}
</script>
<style>
/*.OuterFrame{*/
/*  height: 100%;*/
/*}*/
/*.el-container {*/
/*  height: 100%;*/
/*}*/

.index-con {
  /*height: 100%;*/
  /*width: 100%;*/
  box-sizing: border-box;
}

.el-main {
  margin-bottom: 0px !important;
}

.el-header {
  height: 40px !important;
  text-align: left;
  font-size: 28px;
  font-family: "华文仿宋", cursive, serif, sans-serif !important;
  background: linear-gradient(to left, #80c0c1, #b9e3c3);
  /*background: #b9e3c3;*/
  border-style: solid !important;
  border-top-width: 0px !important;
  border-right-width: 0px !important;
  border-left-width: 0px !important;
  border-bottom-width: 5px !important;
  border-color: #ffffff;
}

.el-aside {
  /*height: 100%;*/
  background-color: #b9e3c3;

}

.el-main {
  padding-top: 0px !important;
  vertical-align: top;
  /*background-color: #ebebeb;*/
  color: #333;

}

body > .el-container {
  margin-bottom: 0;
  /*height: 100%;*/
}
</style>
