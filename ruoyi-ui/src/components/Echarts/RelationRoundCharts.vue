<template>
  <div :class="className" :style="{ height, width }" ref="chartRef"/>
</template>

<script>
// 引入 ECharts
import * as echarts from 'echarts';

// 经验层自动生成方法
function expWrap(jobValue, skills) {
  const childrenList = [
    {name: "1年以下", value: 0},
    {name: "经验不限", value: 1},
    {name: "1-3年", value: 2},
    {name: "无经验", value: 3},
    {name: "3-5年", value: 4},
    {name: "5-10年", value: 5}
  ];

  return childrenList.map(exp => ({
    name: exp.name,
    value: exp.value,
    children: skills
  }));
}

// 核心数据结构
const defaultData =
  {
    "name": "企业岗位要求",
    "value": 0,
    "tooltipText": "岗位要求\naaa",
    "children": [
      {
        "name": "10000人以上", "value": 10,
        "children": [
          {
            "name": "Java工程师",
            "value": 101,
            "children": expWrap(101, [{"name": "Java", "value": 10101}, {
              "name": "Spring Boot",
              "value": 10102
            }, {"name": "MySQL", "value": 10103}, {"name": "Redis", "value": 10104}, {
              "name": "消息队列",
              "value": 10105
            }])
          },
          {
            "name": "前端工程师",
            "value": 102,
            "children": expWrap(102, [{"name": "Vue", "value": 10201}, {
              "name": "React",
              "value": 10202
            }, {"name": "TypeScript", "value": 10203}, {"name": "Vite", "value": 10204}])
          },
          {
            "name": "后端架构师",
            "value": 103,
            "children": expWrap(103, [{"name": "微服务架构", "value": 10301}, {
              "name": "分布式系统",
              "value": 10302
            }, {"name": "高并发设计", "value": 10303}, {"name": "容器化部署", "value": 10304}])
          },
          {
            "name": "测试工程师",
            "value": 104,
            "children": expWrap(104, [{"name": "自动化测试", "value": 10401}, {
              "name": "接口测试",
              "value": 10402
            }, {"name": "性能测试", "value": 10403}])
          },
          {
            "name": "产品经理",
            "value": 105,
            "children": expWrap(105, [{"name": "需求分析", "value": 10501}, {
              "name": "原型设计",
              "value": 10502
            }, {"name": "项目推进", "value": 10503}])
          },
          {
            "name": "数据分析师",
            "value": 106,
            "children": expWrap(106, [{"name": "Python", "value": 10601}, {
              "name": "数据清洗",
              "value": 10602
            }, {"name": "可视化报表", "value": 10603}])
          },
          {
            "name": "算法工程师",
            "value": 107,
            "children": expWrap(107, [{"name": "深度学习", "value": 10701}, {
              "name": "机器学习",
              "value": 10702
            }, {"name": "模型优化", "value": 10703}])
          }
        ]
      },
      {
        "name": "100-299人", "value": 20,
        "children": [
          {
            "name": "综合行政专员",
            "value": 201,
            "children": expWrap(201, [{"name": "文档管理", "value": 20101}, {
              "name": "沟通协调",
              "value": 20102
            }, {"name": "采购流程", "value": 20103}])
          },
          {
            "name": "运营专员",
            "value": 202,
            "children": expWrap(202, [{"name": "数据分析", "value": 20201}, {
              "name": "活动策划",
              "value": 20202
            }, {"name": "内容运营", "value": 20203}])
          },
          {
            "name": "仓库管理员",
            "value": 203,
            "children": expWrap(203, [{"name": "出入库管理", "value": 20301}, {
              "name": "物料盘点",
              "value": 20302
            }])
          },
          {
            "name": "客服专员",
            "value": 204,
            "children": expWrap(204, [{"name": "沟通能力", "value": 20401}, {
              "name": "问题处理",
              "value": 20402
            }])
          }
        ]
      },
      {
        "name": "20-99人", "value": 30,
        "children": [
          {
            "name": "电工",
            "value": 301,
            "children": expWrap(301, [{"name": "线路检修", "value": 30101}, {
              "name": "设备维护",
              "value": 30102
            }, {"name": "应急处理", "value": 30103}])
          },
          {
            "name": "维修工",
            "value": 302,
            "children": expWrap(302, [{"name": "设备维修", "value": 30201}, {
              "name": "工具使用",
              "value": 30202
            }, {"name": "机械基础", "value": 30203}])
          },
          {
            "name": "安全员",
            "value": 303,
            "children": expWrap(303, [{"name": "隐患排查", "value": 30301}, {
              "name": "安全巡检",
              "value": 30302
            }, {"name": "应急预案", "value": 30303}])
          },
          {
            "name": "保洁员",
            "value": 304,
            "children": expWrap(304, [{"name": "垃圾分类", "value": 30401}, {
              "name": "区域维护",
              "value": 30402
            }])
          },
          {
            "name": "质检员",
            "value": 305,
            "children": expWrap(305, [{"name": "质量抽检", "value": 30501}, {
              "name": "异常记录",
              "value": 30502
            }])
          },
          {"name": "仓储助理", "value": 306, "children": expWrap(306, [{"name": "仓库整理", "value": 30601}])}
        ]
      },
      {
        "name": "500-999人", "value": 40,
        "children": [
          {
            "name": "绿化养护工",
            "value": 401,
            "children": expWrap(401, [{"name": "植物修剪", "value": 40101}, {
              "name": "施肥",
              "value": 40102
            }, {"name": "病害识别", "value": 40103}])
          },
          {
            "name": "设备管理员",
            "value": 402,
            "children": expWrap(402, [{"name": "设备台账", "value": 40201}, {
              "name": "例行保养",
              "value": 40202
            }])
          }
        ]
      },
      {
        "name": "1000-9999人", "value": 50,
        "children": [
          {
            "name": "园林巡检员",
            "value": 501,
            "children": expWrap(501, [{"name": "植物病害识别", "value": 50101}, {
              "name": "巡查记录",
              "value": 50102
            }, {"name": "简单处理", "value": 50103}])
          },
          {
            "name": "消防巡检员",
            "value": 502,
            "children": expWrap(502, [{"name": "消防设备检查", "value": 50201}, {
              "name": "隐患发现",
              "value": 50202
            }])
          }
        ]
      },
      {
        "name": "300-499人", "value": 60,
        "children": [
          {
            "name": "环卫工人",
            "value": 601,
            "children": expWrap(601, [{"name": "垃圾清运", "value": 60101}, {
              "name": "区域巡查",
              "value": 60102
            }])
          },
          {
            "name": "司机",
            "value": 602,
            "children": expWrap(602, [{"name": "驾驶技能", "value": 60201}, {
              "name": "车辆保养",
              "value": 60202
            }])
          }
        ]
      },
      {
        "name": "20人以下", "value": 70,
        "children": [
          {
            "name": "店员",
            "value": 701,
            "children": expWrap(701, [{"name": "收银", "value": 70101}, {"name": "商品整理", "value": 70102}])
          },
          {
            "name": "外卖员",
            "value": 702,
            "children": expWrap(702, [{"name": "路线规划", "value": 70201}, {
              "name": "快速配送",
              "value": 70202,
              "children": []
            }])
          },
        ]
      }
    ]
  }
;
export default {
  name: 'RelationRoundCharts', // 组件名称

  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '100%' // 默认给一个较大的高度以便展示完整的径向图
    },
    chartData: {
      type: Object,
      default: () => defaultData, // 组件外部传入的数据（即 getdata() 函数返回的数据结构）
    },
    chartName: {
      type: String,
      default: '数据分析'
    },
    backgroundColor: {
      type: String,
      default: 'transparent'
    },
    // 您的颜色数组，作为组件属性传入，便于复用和定制
    colors: {
      type: Array,
      default: () => [
        "#00ADD0",
        "#FFA12F",
        "#B62AFF",
        "#604BFF",
        "#6E35FF",
        "#002AFF",
        "#20C0F4",
        "#95F300",
        "#04FDB8",
        "#AF5AFF"
      ]
    },
  },

  data() {
    return {
      chart: null, // ECharts 实例
    };
  },

  mounted() {
    this.$nextTick(() => {
      this.initChart();
      window.addEventListener('resize', this.handleResize);
    });
  },

  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
    window.removeEventListener('resize', this.handleResize);
  },

  watch: {
    chartData: {
      handler() {
        this.initChart();
      },
      deep: true
    }
  },

  methods: {
    /**
     * @description 递归处理树图数据，设置节点样式（颜色、大小、线条样式）
     * @param {Array} data - 当前层级的子节点数组
     * @param {number} index - 当前层级深度（0为根节点）
     * @param {string} color - 父节点继承的颜色
     * @returns {Array} - 处理后的子节点数组
     */
    handleData(data, index, color = '#00f6ff') {
      return data.map((item, index2) => {
        let currentColor = color;

        // 逻辑：如果当前是第 1 层（index=1），则根据节点在同级的索引分配颜色
        if (index === 1) {
          currentColor = this.colors.find((c, eq) => eq === index2 % this.colors.length) || color;
        }

        // 设置节点大小 (symbolSize)
        switch (index) {
          case 0:
            item.symbolSize = 70; // 根节点
            break;
          case 1:
            item.symbolSize = 50; // 一级子节点
            break;
          default:
            item.symbolSize = 10; // 二级及以下节点
            break;
        }

        // 设置节点标签样式（仅根节点和一级子节点居中显示）
        if (index === 0 || index === 1) {
          item.label = {
            position: "inside",
          };
        } else {
          // 确保其他层级节点也有 label 样式，以便显示名称
          item.label = {
            position: 'outside', // 默认放在外面
          };
        }

        // 设置线条颜色 (lineStyle)
        item.lineStyle = {
          color: currentColor,
          width: 1,
          curveness: 0.5, // 径向图通常用不到 curveness，但保留原逻辑
        };

        // 设置节点颜色 (itemStyle)
        if (item.children && item.children.length) { // 存在子节点（非叶子节点）
          item.itemStyle = {
            borderColor: currentColor,
            color: currentColor // 填充色
          };
          // 递归处理子节点，颜色继续向下传递（直到下一级子节点重新根据 index2 取色）
          item.children = this.handleData(item.children, index + 1, currentColor);
        } else { // 不存在子节点（叶子节点）
          item.itemStyle = {
            color: 'transparent', // 透明填充
            borderColor: currentColor // 边框色
          };
        }

        return item;
      });
    },

    /**
     * @description 模拟原始 JS 代码中的 getData 函数来生成树图数据
     * @returns {Array} - 包含根节点的数组
     */
    getData() {
      // 使用深拷贝防止修改原始数据
      let data = JSON.parse(JSON.stringify(this.chartData));

      // 检查 data 是否为空或不符合结构，如果为空则返回空数组
      if (!data || Object.keys(data).length === 0) {
        return [];
      }

      // 原始 JS 逻辑中是单根节点，所以包装成数组
      let arr = [data];

      // 调用处理函数
      arr = this.handleData(arr, 0); // 0 表示根节点层级

      return arr;
    },

    /**
     * @description 初始化 ECharts 图表
     */
    initChart() {
      // 检查数据是否合法
      const processedData = this.getData();
      if (processedData.length === 0) {
        if (this.chart) {
          this.chart.dispose();
          this.chart = null;
        }
        return;
      }

      if (!this.chart) {
        // 初始化 ECharts 实例
        this.chart = echarts.init(this.$refs.chartRef);
      } else {
        // 清除旧图表，避免多余事件残留
        this.chart.clear();
      }

      // 获取 ECharts Option
      const option = this.getOption(processedData);

      // 设置图表配置
      this.chart.setOption(option, true);
    },

    /**
     * @description 获取 ECharts 配置项
     * @param {Array} data - 处理后的图表数据
     * @returns {Object} - ECharts Option
     */
    getOption(data) {
      return {
        // 使用您的原始配置
        backgroundColor: this.backgroundColor,
        title: {
          show: true,
          text: this.chartName,
          textStyle: {
            fontSize: 16,
            color: '#ffffff',
          },
          top: '5%',
          left: '5%',
        },
        toolbox: {
          show: true,
          iconStyle: {
            borderColor: "#03ceda"
          },
          feature: {
            restore: {}
          }
        },
        tooltip: {
          trigger: "item",
          triggerOn: "mousemove",
          backgroundColor: "rgba(1,70,86,1)",
          borderColor: "rgba(0,246,255,1)",
          borderWidth: 0.5,
          textStyle: {
            fontSize: 10
          },
          // 使用原逻辑中的 formatter 来显示 tooltipText
          formatter: function (params) {
            let res = params.name + ':' + params.value;
            if (params.data && params.data.tooltipText) {
              // tooltipText 是在原始数据生成时添加的，而不是在 handleData 中添加的
              res += "<br/>" + params.data.tooltipText;
            }
            // 对于一级/二级节点，默认 name 可能是 '节点1'，tooltipText 提供了更详细的信息
            return res;
          }
        },
        series: [
          {
            type: "tree",
            name: "径向树图",
            hoverAnimation: true,
            data: data, // 使用处理后的数据
            top: 0,
            bottom: 0,
            left: 0,
            right: 0,
            layout: "radial", // 径向布局
            symbol: "circle",
            symbolSize: 10, // 默认的 symbolSize 会被 handleData 覆盖
            nodePadding: 20,
            animationDurationUpdate: 750,
            expandAndCollapse: true,
            initialTreeDepth: 2, // 默认展开深度
            roam: true,
            focusNodeAdjacency: true, // 启用 ECharts 默认的焦点邻近高亮
            itemStyle: {
              borderWidth: 1,
            },
            label: {
              color: "#fff",
              fontSize: 10,
              fontFamily: "SourceHanSansCN",
              position: "inside",
              rotate: 0,
              // 其他层级的 label 样式在 handleData 中被动态设置
            },
            lineStyle: {
              width: 1,
              curveness: 0.5,
              // 颜色在 handleData 中设置
            }
          }
        ]
      };
    },

    /**
     * @description 处理窗口大小变化，使图表自适应
     */
    handleResize() {
      if (this.chart) {
        this.chart.resize();
      }
    }
  }
};
</script>

<style scoped>
/* 可以在这里添加一些样式 */
.chart {
  /* 确保 chart 元素本身能够完全填充父容器 */
  width: 100%;
  height: 100%;
}
</style>
