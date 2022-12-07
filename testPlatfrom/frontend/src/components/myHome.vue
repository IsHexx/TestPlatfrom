<template >
  <div   class="body">
    <div v-for="item in dataapi" :key="item.id" class="test">
      <div class="htest">
        <div class="item">
          <!-- 测试用例总 -->
          <div id="caseall_title">
            <span>测试用例总</span>
          </div>
          <div id='all_number'>
            <div id="all">
              <span>总:</span>
              <span>{{ item.all}}</span>
            </div>
            <div id="all_pass">
              <span>已通过:</span>
              <span>{{ item.allpass}}</span>
            </div>
            <div id="all_fail">
              <span>未通过:</span>
              <span>{{ item.allfile}}</span>
            </div>
            <div id="all_bug">
              <span>缺陷:</span>
              <span>{{ item.allbug}}</span>
            </div>
          </div>
        </div>

        <!-- UI自动化汇总 -->
        <div class="item">
          <div id="caseui_title">
            <span>UI自动化用例</span>
          </div>
          <div id='ui_number'>
            <div id="ui">
              <span>总:</span>
              <span>{{ item.uiall}}</span>
            </div>
            <div id="ui_pass">
              <span>已通过:</span>
              <span>{{ item.uipass}}</span>
            </div>
            <div id="ui_fail">
              <span>未通过:</span>
              <span>{{ item.uifile}}</span>
            </div>
            <div id="ui_bug">
              <span>缺陷:</span>
              <span>{{ item.uiall}}</span>
            </div>
          </div>
        </div>

        <!-- API自动化汇总 -->
        <div class="item">
          <div id="caseapi_title">
            <span>API自动化用例</span>
          </div>
          <div id='api_number'>
            <div id="api">
              <span>总:</span>
              <span>{{ item.apiall}}</span>
            </div>
            <div id="api_pass">
              <span>已通过:</span>
              <span>{{ item.apipass}}</span>
            </div>
            <div id="api_fail">
              <span>未通过:</span>
              <span>{{ item.apifile}}</span>
            </div>
            <div id="api_bug">
              <span>缺陷:</span>
              <span>{{ item.apibug}}</span>
            </div>
          </div>
        </div>
      </div>

      <!--echarts的容器-->
      <div id="chart1" ref = "a"></div>
      <div id="chart2" ref = "b"></div>

    </div>
  </div>

</template>

<script>
import * as echarts from "echarts";
import axios from "axios";

export default {
  name: "myHome",
  data: function () {
    return {
      dataapi:[]
    }
  },
  mounted() {
    setTimeout(()=>{
      this.initEcharts();
      this.initEcharts2();
      },200)
  },
//   mounted() {
// 	// this.$nextTick(()=>{
// 	// 	 this.initEcharts()
// 	//  })
// 	 // 新建一个promise对象
// 	let newPromise = new Promise((resolve) => {
// 	  resolve()
// 	 })
// 	 //然后异步执行echarts的初始化函数
//     newPromise.then(() => {
// 	   //	此dom为echarts图标展示dom
// 	   this.initEcharts();
//      this.initEcharts2();
// 	 })
// },
  created() {
    this.getapi();
  },
  methods: {

    initEcharts() {
      // let uimychart = this.$charts.initEcharts(document.getElementById("chart1"))
      const uimychart = echarts.init(document.getElementById("chart1"));
      const uichart = {
        title: {text: "UI自动化用例执行情况统计"},
        legend: {},
        tooltip: {},
        dataset: {
          source: [
            ["", "Pass", "Fail", "Bug"],
            ["9月1日", 72.4, 53.9, 39.1],
            [this.xqo.data_date, this.xqo.allpass, this.xqo.allfile, this.xqo.allbug],
            ["9月3日", 83.1, 73.4, 55.1],
            ["9月4日", 86.4, 65.2, 82.5],
            ["9月5日", 72.4, 53.9, 39.1],
            ["9月6日", 72.4, 53.9, 39.1],
            ["9月7日", 72.4, 53.9, 39.1],
            ["9月8日", 72.4, 53.9, 39.1]
          ]
        },
        xAxis: {
          type: "category",
          axisLabel: {
            interval: 0,
            rotate: 40
          }
        },
        yAxis: {},
        // Declare several bar series, each will be mapped
        // to a column of dataset.source by default.
        series: [
          {type: "bar", color: ["#93d5dc"]},
          {type: "bar", color: ["#20a162"]},
          {type: "bar", color: ["#61ac85"]}
        ]
      };

      uimychart.setOption(uichart);
      window.addEventListener("resize", () => {
        uimychart.resize();
      });
    },

    initEcharts2() {
      const apichart = {
        title: {text: "API自动化用例执行情况统计"},
        legend: {},
        tooltip: {},
        dataset: {
          source: [
            ["", "Pass", "Fail", "Bug"],
            [this.xqo.data_date, this.xqo.allpass, this.xqo.allfile, this.xqo.allbug],
            ["9月2日", 43.3, 85.8, 93.7],
            ["9月3日", 83.1, 73.4, 55.1],
            ["9月4日", 86.4, 65.2, 82.5],
            ["9月5日", 72.4, 53.9, 39.1],
            ["9月6日", 72.4, 53.9, 39.1],
            ["9月7日", 72.4, 53.9, 39.1]
          ]
        },
        xAxis: {
          type: "category",
          axisLabel: {
            interval: 0,
            rotate: 40
          }
        },
        yAxis: {},
        // Declare several bar series, each will be mapped
        // to a column of dataset.source by default.
        series: [
          {type: "bar", color: ["#93d5dc"]},
          {type: "bar", color: ["#20a162"]},
          {type: "bar", color: ["#61ac85"]}
        ]
      };
      const apimychart = echarts.init(document.getElementById("chart2"));
      apimychart.setOption(apichart);
      window.addEventListener("resize", () => {
        apimychart.resize();
      });
    },
    getapi() {
      var that = this;
      axios.get('/testhome/').then(response => {
        if (response.data) {
          that.dataapi = response.data;
          this.xqo = JSON.stringify(that.dataapi, null, " ")
          this.xqo = JSON.parse(this.xqo.slice(1,-2));
          console.log(this.xqo)
          return response.data
        }
      })
        .catch(error => {
          alert('请求失败')
        })
    },
  },
};
</script>
<style>
.body {
  margin-left: 3px;
  background: #ebebeb;
}

.menu {
  width: 100%;
  height: 100%;
  background-color: #f7f4ed;
  /* top: 120px;
    bottom: 120px;
    background-color: azure; */
  float: left;
}

.menu_list .current {
  background: rgb(147, 213, 220);
}

.menu_nva {
  line-height: 38px;
  border-left: 1px solid #93d5dc33;
  background: #fff;
  border-right: 1px solid #93d5dc33;
}

.menu_nva a {
  display: block;
  height: 38px;
  line-height: 38px;
  padding-left: 38px;
  color: #777777;
  background: #fff;
  text-decoration: none;
  border-bottom: 1px solid #51a9f18c;
}

.menu_nva a:hover {
  text-decoration: none;
}

.menu_head {
  height: 47px;
  line-height: 47px;
  padding-left: 25px;
  font-size: 18px;
  color: #525252;
  cursor: pointer;
  border: 1px solid #f1f1f1;
  position: relative;
  margin: 0px;
  font-weight: bold;
  background: #93d5dc33;
}

.test {
  height: 1200px;
  margin: 0px;
  margin-top: 0px;
  overflow: hidden;
}

.htest {
  height: calc(15%- 20px);
  width: 97%;
  margin-top: 5px;
  margin-left: 20px;
  border-left: 2px solid #e6e4e2;
  border-right: 2px solid #e6e4e2;
  border-bottom: 2px solid #e6e4e2;
  border-top: 1px solid #e6e4e2;
  background-color: #f7f4ed;
  overflow: hidden;
}

.item {
  background-color: rgb(147, 213, 220, 0.7);
  width: calc(33.3333% - 20px);
  height: 130px;
  margin: 10px;
  border-radius: 15px;
  float: left;
}

#caseall_title {
  width: 150px;
  height: 20px;
  margin-left: 10px;
  margin-top: 10px;
  border-radius: 15px;
  font-weight: bold;
  font-size: large;
}

#all_number {
  width: 270px;
  height: 100px;
  left: 10px;
  /*margin-top: 0px;*/
  position: relative;
}

#all {
  width: 50px;
  height: 100px;
  margin-left: 10px;
  margin-top: 20px;
  border-radius: 15px;
  position: absolute;
}

#all_bug {
  width: 50px;
  height: 10px;
  margin-left: 10px;
  margin-top: 60px;
  border-radius: 15px;
  position: absolute;
}

#all_pass {
  width: 70px;
  height: 100px;
  margin-left: 160px;
  margin-top: 20px;
  border-radius: 15px;
  position: absolute;
}

#all_fail {
  width: 70px;
  height: 100px;
  margin-left: 160px;
  margin-top: 60px;
  border-radius: 15px;
  position: absolute;
}

/* UI自动化样式 */
#caseui_title {
  width: 150px;
  height: 20px;
  margin-left: 10px;
  margin-top: 10px;
  border-radius: 15px;
  font-weight: bold;
  font-size: large;
}

#ui_number {
  width: 270px;
  height: 100px;
  left: 10px;
  /*margin-top: 0px;*/
  position: relative;
}

#ui {
  width: 50px;
  height: 100px;
  margin-left: 10px;
  margin-top: 20px;
  border-radius: 15px;
  position: absolute;
}

#ui_bug {
  width: 50px;
  height: 10px;
  margin-left: 10px;
  margin-top: 60px;
  border-radius: 15px;
  position: absolute;
}

#ui_pass {
  width: 70px;
  height: 100px;
  margin-left: 160px;
  margin-top: 20px;
  border-radius: 15px;
  position: absolute;
}

#ui_fail {
  width: 70px;
  height: 100px;
  margin-left: 160px;
  margin-top: 60px;
  border-radius: 15px;
  position: absolute;
}

/* API自动化样式 */
#caseapi_title {
  width: 150px;
  height: 20px;
  margin-left: 10px;
  margin-top: 10px;
  border-radius: 15px;
  font-weight: bold;
  font-size: large;
}

#api_number {
  width: 270px;
  height: 100px;
  left: 10px;
  /*margin-top: 0px;*/
  position: relative;
}

#api {
  width: 50px;
  height: 100px;

  margin-left: 10px;
  margin-top: 20px;
  border-radius: 15px;
  position: absolute;
}

#api_bug {
  width: 50px;
  height: 10px;
  margin-left: 10px;
  margin-top: 60px;
  border-radius: 15px;
  position: absolute;
}

#api_pass {
  width: 70px;
  height: 100px;
  margin-left: 160px;
  margin-top: 20px;
  border-radius: 15px;
  position: absolute;
}

#api_fail {
  width: 70px;
  height: 100px;
  margin-left: 160px;
  margin-top: 60px;
  border-radius: 15px;
  position: absolute;
}

#chart1 {
  margin-top: 10px;
  margin-left: 20px;
  width: 97%;
  height: 500px;
  border-left: 2px solid #e6e4e2;
  border-right: 2px solid #e6e4e2;
  border-bottom: 2px solid #e6e4e2;
  border-top: 1px solid #e6e4e2;
  background-color: #f7f4ed;
}

#chart2 {
  width: 97%;
  height: 500px;
  margin-left: 20px;
  margin-top: 12px;
  border-left: 2px solid #e6e4e2;
  border-right: 2px solid #e6e4e2;
  border-bottom: 2px solid #e6e4e2;
  border-top: 1px solid #e6e4e2;
  background-color: #f7f4ed;
}
</style>
