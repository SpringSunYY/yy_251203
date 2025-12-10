<template>
  <div :class="className" :style="{ height, width }" ref="chartRef"></div>
</template>

<script>
import * as echarts from 'echarts';
import 'echarts/theme/macarons'; // 引入主题

// --- ECharts 颜色和样式配置 ---
// 定义通用的颜色数组，用于循环分配
const colorList = ['#ff8c00', '#46ea91', '#2ba0ff', '#ed593b', '#7357ff', '#f2d750'];

/**
 * 动态生成 Series 配置
 * @param {Array} data - chartData.values
 * @returns {Array} Series 配置数组
 */
const getSeries = (data) => {
  // 定义一个通用的线性渐变函数
  const getGradientColor = (color) => {
    const hexToRgb = (hex) => {
      const bigint = parseInt(hex.slice(1), 16);
      const r = (bigint >> 16) & 255;
      const g = (bigint >> 8) & 255;
      const b = bigint & 255;
      return `${r}, ${g}, ${b}`;
    };
    const rgbColor = hexToRgb(color);

    return new echarts.graphic.LinearGradient(1, 1, 0, 0, [
      {offset: 0, color: `rgba(${rgbColor}, 0.8)`},
      {offset: 1, color: color},
    ]);
  };

  // 映射数据生成 Series 配置
  return data.map((item, index) => {
    const color = colorList[index % colorList.length]; // 循环取色

    const seriesItem = {
      name: item.name,
      type: 'line',
      data: item.values,
      symbolSize: 1,
      symbol: 'circle',
      smooth: true,
      showSymbol: false,
      lineStyle: {
        width: 2,
        color: getGradientColor(color),
        shadowColor: `rgba(0, 0, 0, 0.3)`,
        shadowBlur: 5,
        shadowOffsetY: 5,
      },
      itemStyle: {
        normal: {
          color: color,
          borderColor: color,
        },
      },
    };

    // 仅对第一个系列（index=0）应用面积图样式
    if (index === 0) {
      seriesItem.areaStyle = {
        normal: {
          // 使用 #ff8c00 的 0.4 透明度作为面积图起始色
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
            offset: 0,
            color: `rgba(255, 140, 0, 0.4)`
          }, {
            offset: 0.8,
            color: `rgba(255, 140, 0, 0)` // 渐变至透明
          }], false),
          shadowColor: 'rgba(0, 0, 0, 0.1)',
          shadowBlur: 10
        }
      };
    }
    return seriesItem;
  });
};


export default {
  name: 'LineBatchZoomCharts',
  props: {
    className: {type: String, default: 'chart'},
    width: {type: String, default: '100%'},
    height: {type: String, default: '100%'},
    autoResize: {type: Boolean, default: true},
    chartData: {
      type: Object,
      default: () => ({
        names: [
          '2024-10-01', '2024-10-02', '2024-10-03', '2024-10-04', '2024-10-05', '2024-10-06', '2024-10-07', '2024-10-08', '2024-10-09', '2024-10-10', '2024-10-11', '2024-10-12', '2024-10-13', '2024-10-14', '2024-10-15', '2024-10-16', '2024-10-17', '2024-10-18', '2024-10-19', '2024-10-20', '2024-10-21', '2024-10-22', '2024-10-23', '2024-10-24', '2024-10-25', '2024-10-26', '2024-10-27', '2024-10-28', '2024-10-29', '2024-10-30', '2024-10-31'
        ],
        values: [
          // 1. 用户注册
          {
            name: '用户注册',
            values: [509, 917, 2455, 2610, 2719, 3033, 3044, 3085, 2708, 2809, 2117, 2000, 1455, 1210, 719, 733, 944, 2285, 2208, 3372, 3936, 3693, 2962, 2810, 3519, 2455, 2610, 2719, 2484, 2078, 5000]
          },
          // 2. 咨询
          {
            name: '咨询',
            values: [100, 20, 30, 102, 15, 30, 20, 18, 50, 40, 70, 80, 90, 110, 120, 10, 25, 45, 65, 85, 95, 105, 150, 130, 125, 115, 105, 95, 85, 75, 65]
          },
          // 3. 求助
          {
            name: '求助',
            values: [20, 12, 11, 14, 25, 16, 10, 20, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140]
          },
          // 4. 无效
          {
            name: '无效',
            values: [150, 120, 170, 140, 100, 160, 110, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450, 470, 490, 510, 530, 550, 570]
          },
          // 5. 投诉举报
          {
            name: '投诉举报',
            values: [200, 80, 100, 30, 60, 50, 110, 20, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125, 135, 145, 155, 165, 175, 185, 195, 205, 215, 225, 235]
          },
          // 6. 建议
          {
            name: '建议',
            values: [20, 80, 150, 30, 60, 50, 50, 20, 10, 5, 2, 1, 3, 7, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96, 102, 108]
          }
        ]
      })
    },
    chartName: {type: String, default: '数据趋势分析'},
    // 默认颜色
    defaultColor: {
      type: Array,
      default: () => colorList
    },
    // 背景颜色
    backgroundColor: {type: String, default: '#0D2753'},
  },
  data() {
    return {
      chart: null
    };
  },
  watch: {
    chartData: {
      handler() {
        this.setOptions();
      },
      deep: true
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
    });
    if (this.autoResize) {
      window.addEventListener('resize', this.resizeChart);
    }
  },
  beforeDestroy() {
    this.destroyChart();
  },
  methods: {
    destroyChart() {
      if (this.chart) {
        this.chart.dispose();
        this.chart = null;
      }
      if (this.autoResize) {
        window.removeEventListener('resize', this.resizeChart);
      }
    },
    initChart() {
      if (this.chart) {
        this.destroyChart();
      }
      // 使用 macarons 主题
      this.chart = echarts.init(this.$refs.chartRef, 'macarons');
      this.setOptions();
    },
    resizeChart() {
      this.chart?.resize();
    },
    setOptions() {
      if (!this.chart) return;
      const {names: xData, values: yData} = this.chartData;

      if (!xData || !xData.length || !yData || !yData.length) return;

      const series = getSeries(yData);

      this.chart.setOption({
        backgroundColor: this.backgroundColor,
        // --- 标题配置 (右上角) ---
        title: {
          text: this.chartName,
          left: '5%',
          top: '2%',
          textStyle: {
            color: '#fff',
            fontSize: 18
          }
        },
        legend: {
          icon: 'circle',
          top: '5%',
          right: '5%',
          itemWidth: 6,
          itemGap: 5,
          textStyle: {
            color: '#fff',
            padding: [3, 0, 0, 0],
          },
          data: yData.map(item => item.name)
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        // --- Grid 调整，为 DataZoom 留出空间 ---
        grid: {
          top: '10%',
          left: '5%',
          bottom: '10%', // 留给 DataZoom
          right: '5%',
          containLabel: true
        },
        // --- DataZoom 配置 ---
        dataZoom: [
          {
            type: 'slider', // 滑块型
            show: true,
            xAxisIndex: [0],
            bottom: '5%',
            start: 0,
            end: 100, // 默认显示全部
            textStyle: {
              color: '#fff'
            },
            borderColor: '#33BBFF',
            fillerColor: 'rgba(51, 187, 255, 0.2)',
            handleStyle: {
              color: '#33BBFF',
            }
          },
          {
            type: 'inside', // 内置型
            xAxisIndex: [0],
            start: 0,
            end: 100
          }
        ],
        xAxis: [
          {
            type: 'category',
            data: xData,
            axisLine: {
              lineStyle: {
                color: '#33BBFF',
              },
            },
            axisTick: {
              show: false,
            },
            axisLabel: {
              interval: 'auto',
              rotate: 0, // X 轴标签水平
              textStyle: {
                color: '#5FBBEB',
              },
              fontSize: 10,
              margin: 10,
            },
            boundaryGap: false,
          },
        ],
        yAxis: [
          {
            name: '', // Y 轴无单位
            type: 'value',
            axisTick: {
              show: false,
            },
            axisLine: {
              show: true,
              lineStyle: {
                color: '#05D5FF',
              },
            },
            axisLabel: {
              textStyle: {
                color: '#5FBBEB',
              },
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: 'rgba(5, 213, 255, 0.2)',
                type: 'dashed'
              }
            },
          },
        ],
        series: series
      });
    }
  }
};
</script>

<style scoped>
.chart {
  overflow: hidden;
}
</style>
