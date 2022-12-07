<template>
  <div class="ui_main">
    <!-- 搜索筛选 -->
    <div style="text-align: left">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="">
          <el-input size="small" v-model="searchForm.condition" prefix-icon="el-icon-search"
                    placeholder="请输入元素NO、名称"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button size="small" type="primary" @click="search">搜索</el-button>
          <el-button size="small" @click="reset">重置</el-button>
        </el-form-item>
        <el-form-item style="float: right">
          <el-button size="small" type="primary" icon="el-icon-plus" @click="addElement">新增元素</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 页面模块 -->
    <el-col :span="4" class="left-tree">
      <module-tree title="页面模块" :treeData="treeData" :currentModule="searchForm.module_id"
                   @clickModule="clickModule($event)" @appendModule="appendModule($event)"
                   @removeModule="removeModule(arguments)" @dragNode="dragNode(arguments)"/>
    </el-col>
    <!-- 元素列表 -->
    <el-col :span="20" class="right-table">
      <!--列表-->
      <el-table type="primary"
                :header-cell-style="tableHeaderCellStyle"
                size="small" :data="elementListData"
                v-loading="loading" element-loading-text="拼命加载中">
        <el-table-column prop="id" label="NO" width="60px"/>
        <el-table-column prop="name" label="元素名称" min-width="180"/>
        <el-table-column prop="by" label="定位方式"/>
        <el-table-column prop="expression" label="表达式" min-width="150"/>
        <el-table-column prop="module_name" label="所属页面"/>
        <el-table-column prop="create_user" label="创建人"/>
        <el-table-column prop="update_time" label="更新时间" width="150px"/>
        <el-table-column fixed="right" align="operation" label="操作" width="100">
          <template slot-scope="scope">
            <el-button type="text" size="mini" @click="editElement(scope.row)">编辑</el-button>
            <el-button type="text" size="mini" @click="deleteElement(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页组件 -->
      <Pagination v-bind:childMsg="pageparam" @callFather="callFather"/>
    </el-col>
    <!-- 添加模块弹框 -->
    <module-append title="添加页面模块" :show.sync="moduleVisible" :moduleForm="moduleForm" @closeDialog="closeDialog"
                   @submitModule="submitModule($event)"/>

    <!-- 添加元素弹框 -->
    <el-dialog title="选择元素类型" :visible.sync="elementVisible" width="40%" destroy-on-close>
      <el-form label-width="120px" style="padding-right: 30px;" :model="addElementForm" :rules="rules"
               ref="addElementForm">
        <el-form-item label="元素名称" prop="name">
          <el-input size="small" style="width:95%" v-model="addElementForm.name" auto-complete="off"
                    placeholder="元素名称"/>
        </el-form-item>
        <el-form-item label="定位方式" prop="by">
          <el-select size="small" style="width:95%;" v-model="addElementForm.by" placeholder="定位方式">
            <el-option v-for="item in byList" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="表达式" prop="expression">
          <el-input size="small" style="width:95%" v-model="addElementForm.expression" auto-complete="off"
                    placeholder="表达式"/>
        </el-form-item>
        <el-form-item label="所属页面" prop="module_id">
          <select-tree style="width:95%; margin-left: 9px;" placeholder="所属页面" :selectedValue="addElementForm.module_id"
                       :selectedLabel="addElementForm.module_name" :treeData="treeData"
                       @selectModule="selectModule($event)"/>
        </el-form-item>
        <el-form-item label="元素描述">
          <el-input size="small" style="width:95%" v-model="addElementForm.description" :autosize="{ minRows: 3}"
                    type="textarea" maxlength="200" show-word-limit auto-complete="off" placeholder="元素描述"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="elementVisible=false">取消</el-button>
        <el-button size="small" type="primary" @click="submitElement">确定</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import ModuleTree from '../views/moduleTree'
import Pagination from '../views/Pagination'
import moduleAppend from '../views/moduleAppend'
import SelectTree from '../common/selectTree'
import {timestampToTime} from '../utils/util'
import axios from "axios";

export default {
  // 注册组件
  components: {
    ModuleTree, Pagination, moduleAppend, SelectTree
  },
  name: "elementManage",
  data() {
    return {
      loading: false,
      moduleVisible: false,
      elementVisible: false,
      moduleForm: {
        moduleName: "",
        parentId: "",
        parentName: "",
        data: "",
      },
      newelementType: "API",
      elementTypes: [
        {label: "API", value: "API"},
        {label: "WEB", value: "WEB"},
      ],
      byList: [
        {label: "ID", value: "ID"},
        {label: "NAME", value: "NAME"},
        {label: "TAG", value: "TAG"},
        {label: "CLASS", value: "CLASS"},
        {label: "CSS", value: "CSS"},
        {label: "LINK", value: "LINK"},
        {label: "PARTIAL_LINK", value: "PARTIAL"},
        {label: "XPATH", value: "XPATH"},
      ],
      addElementForm: {
        id: "",
        name: "",
        by: "",
        expression: "",
        module_id: "",
        module_name: "",
        description: ""
      },
      searchForm: {
        page: 1,
        limit: 10,
        module_id: "",
        condition: "",

      },
      elementListData: [],
      pageparam: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      treeData: [],
      rules: {
        name: [{required: true, message: '元素名称不能为空', trigger: 'blur'}],
        by: [{required: true, message: '定位方式不能为空', trigger: 'blur'}],
        expression: [{required: true, message: '表达式不能为空', trigger: 'blur'}],
        module_id: [{required: true, message: '所属页面不能为空', trigger: 'blur'}]
      }
    }
  },
  // watch:{
  //       '$route':"getTree"
  //  	},
  created() {
    // this.$root.Bus.$emit('initBread', ["用例中心", "元素管理"])
    this.getTree()
    this.getdata(this.searchForm)

  },
  methods: {
    // 样式加载
    tableHeaderCellStyle({row, column, rowIndex, columnIndex}) {
      let cellStyle;
      cellStyle = "background-color: #efefef; color: #333333"
      return cellStyle;
    },
    // 点击模块
    clickModule(data) {
      this.searchForm.module_id = data.id;
      this.getdata(this.searchForm);
    },
    // 添加模块
    appendModule(data) {
      console.log(data)
      if (data) {
        this.moduleForm.parentId = data.id;
        this.moduleForm.parentName = data.name;
        this.moduleForm.data = data;
      } else {
        this.moduleForm.parentId = 0;
        this.moduleForm.parentName = "根节点";
        this.moduleForm.data = "";
      }
      this.moduleVisible = true;
    },
    // 删除模块
    removeModule(args) {
      let node = args[0];
      let data = args[1];
      let url = '/testhome/pagedelete';
      axios.post(url, data).then((response) => {
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        children.splice(index, 1);
        this.$message.success("模块删除成功")
      });
    },
    // 拖拽模块
    dragNode(args) {
      let dragNode = args[0];
      let newParent = args[1];
      let url = '/autotest/module/save';
      let moduleForm = dragNode.data;
      moduleForm.parentId = newParent;
      this.$post(url, moduleForm, response => {
        this.$message.success("更改成功")
      });
    },
    // 关闭弹框
    closeDialog() {
      this.moduleVisible = false;
    },

    // 提交模块方法1--success
    submitModule(moduleForm) {
      /*获取项目Id*/
      moduleForm.project_id = this.$store.state.projectId;
      moduleForm.create_user = "轻羽",
        /*模块标签*/
        moduleForm.module_type = 'page_module';
      moduleForm.name = this.moduleForm.name;
      moduleForm.parent_id = this.moduleForm.parentId
      /***从这里开始请求后端***/
      let url = '/testhome/pagelist';
      axios.post(url, moduleForm).then((response) => {

        const newChild = response.data;
        if (moduleForm.parentId === 0) {
          this.treeData.push(newChild);
        } else {
          console.log("this.moduleForm.data.children值>>", this.moduleForm.data.children)
          if (!this.moduleForm.data.children) {
            this.$set(this.moduleForm.data, 'children', []);
          }
          console.log("newChild值>>", newChild)
          console.log("this.moduleForm.data.值>>", this.moduleForm.data)
          this.moduleForm.data.children.push(newChild);
          console.log("this.moduleForm.data.children值>>", this.moduleForm.data.children)
        }

        this.moduleVisible = false;
        this.moduleForm.name = "";
        this.$message.success("保存成功");
      });
    },
    // 获取树数据
    getTree(moduleForm) {
      // let url = '/testhome/pagelist' + this.$store.state.projectId;
      let url = '/testhome/getpagelist';
      // const {data: res} = await this.$get(url, {params: this.treeData})
      axios.get(url).then((response) => {
        this.treeData = response.data;
        // const ids = []
        // var keys = Object.keys(this.treeData)
        // var values = Object.values(this.treeData)
        //
        // // console.log(this.treeData)
        // for (let index in this.treeData) {
        //   ids.push(this.treeData[index].id);
        // }
        // console.log("ids=", ids)
        // for (let index in this.treeData) {
        //   if (this.treeData[index].parent_id in ids) {
        //     console.log("")
        //   } else {
        //     const fvalue = this.treeData[index].parent_id
        //     const childvalue = this.treeData[index]
        //     console.log("fvalue值为", fvalue)
        //     // 根据id的值获取id所属行的index
        //     for (index in this.treeData) {
        //       if (fvalue == this.treeData[index].id) {
        //         // 获取索引值
        //         // const newindex = index
        //         console.log("索引值为", this.treeData[index].id)
        //         this.treeData.push(childvalue);
        //          console.log(this.treeData)
        //       } else {
        //         console.log(index)
        //       }
        //     }
        //     // const newchild = this.treeData[index]
        //
        //   }
        //
        // }
      }).catch(error => {
        alert(error)
      });
    },
    // 获取列表数据方法
    getdata(searchParam) {
      this.loading = true;
      let url = '/testhome/elementlistpush/' + searchParam.page + '/' + searchParam.limit;
      // let url = '/testhome/elementlistpush';
      let param = {
        condition: searchParam.condition,
        module_id: searchParam.module_id,
        projectId: this.$store.state.projectId
      };
      axios.post(url, param).then((response) => {
        let data = response.data;
        for (let i = 0; i < data.length; i++) {
          data.update_time = timestampToTime(data[i].update_time);
        }
        this.elementListData = data;
        this.loading = false
        console.log(data.total)
        // 分页赋值
        this.pageparam.currentPage = this.searchForm.page;
        this.pageparam.pageSize = this.searchForm.limit;
        if (data.length !== 0){
          this.pageparam.total = data[0].total;
          }
        else {
          this.pageparam.total = data.total;
          }
      });
    },
    // 分页插件事件
    callFather(parm) {
      this.searchForm.page = parm.currentPage
      this.searchForm.limit = parm.pageSize
      this.getdata(this.searchForm)
    },
    // 搜索按钮
    search() {
      console.log(this.searchForm)
      this.getdata(this.searchForm)
    },
    // 重置按钮
    reset() {
      this.searchForm.module_id = "";
      this.searchForm.condition = "";
      this.getdata(this.searchForm)
    },
    // 新增元素
    addElement() {
      this.addElementForm = {
        id: "",
        name: "",
        by: "",
        expression: "",
        module_id: "",
        module_name: "",
        description: ""
      };
      this.elementVisible = true;
    },
    selectModule(data) {
      console.log(data)
      this.addElementForm.module_id = data.id;
      this.addElementForm.module_name = data.name;
    },
    // 提交元素
    submitElement() {
      // 请求接口
      this.$refs["addElementForm"].validate(valid => {
        if (valid) {
          this.addElementForm.create_user = "轻羽",
            this.addElementForm.project_id = this.$store.state.projectId;
          let url = '/testhome/elementlist';
          console.log(this.addElementForm)
          axios.post(url, this.addElementForm).then((response) => {
            this.$message.success("保存成功");
            this.elementVisible = false;
            this.getdata(this.searchForm);
          });
        } else {
          return false;
        }
      })
    },
    // 编辑元素
    editElement(row) {
      console.log(row)
      this.addElementForm.id = row.id;
      this.addElementForm.name = row.name;
      this.addElementForm.by = row.by;
      this.addElementForm.expression = row.expression;
      this.addElementForm.module_id = row.module_id;
      this.addElementForm.module_name = row.module_name;
      this.addElementForm.description = row.description;
      this.elementVisible = true;
    },
    // 删除元素
    deleteElement(row) {
      this.$confirm('确定要删除元素吗?', '删除提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          let url = '/testhome/elementdelete';
          axios.post(url, {id: row.id}).then((response) => {
            this.$message.success("删除成功");
            this.getdata(this.searchForm);
          });
        })
        .catch(() => {
          this.$message.success("取消成功");
        })
    },
  }
}
</script>

<style scoped>

.tree-title {
  float: left;
  padding: 6px 12px;
  font-weight: bold;
  font-size: 12px;
}

.tree-add {
  float: right;
  width: 24px;
  padding: 5px 5px;
  height: 24px;
}

.tree-input {
  height: 30px;
  padding: 5px 5px;
}

.module-tree {
  border: 1px solid rgb(219, 219, 219);
}

.tree-header {
  height: 39px;
  padding-right: 5px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #efefef;
}

.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  padding-right: 8px;
}

.custom-tree-node:hover .tree-opt {
  display: block;
  /*align-items: top;*/
}

.custom-tree-node:hover .tree-label {
  word-wrap: break-word;
}

.tree-opt {
  display: none;
}

.filter-tree >>> .el-tree-node__children {
  overflow: visible !important;
}

.tree-body {
  min-height: 520px;
  overflow: hidden;
  overflow-x: auto;
  white-space: nowrap;
}

.ui_main {
  /*width: 100%;*/
  /*height: 100%;*/
  /*background-color: #ffffff;*/
  border: 1px #d9ecc5;

}

.left-tree {
  margin-bottom: 0px !important;
  padding-right: 5px;
  border-right: 1px solid rgb(219, 219, 219);
}

.right-table {
  padding-left: 5px;
}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  background: #ffffff;
}

.bg-purple {
  background: #ffffff;
}

.bg-purple-light {
  background: #fbfbfb;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

.el-button--primary {
  border: 0px;
  background-color: #22ac68;
}

.el-table-column {
  background-color: #B1DFE1FF;
}

</style>
