<template>
  <div :class="className" :style="{ height, width }" ref="chartRef"/>
</template>

<script>
import * as echarts from 'echarts'
import 'echarts/theme/macarons'


export default {
  name: 'BarPieCharts',
  props: {
    className: {type: String, default: 'chart'},
    width: {type: String, default: '100%'},
    height: {type: String, default: '100%'},
    // 统一数据源
    chartData: {
      type: Array,
      default: () => [
        {name: '太原市民政局', value: 70, tooltipText: '太原市民政局在太原，\n是的在太原。'},
        {name: '太原市运输局', value: 34, tooltipText: '负责太原市的交通运输管理。'},
        {name: '太原市残联', value: 60, tooltipText: '为残疾人提供服务和保障。'},
        {name: '太原市报社', value: 78, tooltipText: '太原市的主要新闻出版机构。'},
        {name: '太原市司法局', value: 69, tooltipText: '负责太原市的法律事务管理。'}
      ]
    },
    // 标题
    chartName: {type: String, default: '太原市机构数据总览 - Bar & Pie'},
    // 背景颜色
    backgroundColor: {type: String, default: 'transparent'},
    // 默认颜色
    defaultColor: {
      type: Array,
      default: () => ['#fd566a', '#9787ff', '#fdb36a', '#fdd56a', '#6da7ff', '#63e1f2']
    },
    // 间隔块的固定值
    gapValue: {
      type: Number,
      default: 5
    },

  },
  data() {
    return {
      chart: null,
      resizeObserver: null,
    };
  },
  computed: {
    // 提取所有名称
    chartNames() {
      return this.chartData.map(item => item.name);
    },
    // 计算总值
    chartTotalValue() {
      return this.chartData.reduce((sum, item) => sum + item.value, 0);
    },
    // 预处理环形图数据 (包含间隔块)
    pieData() {
      const pieData = [];
      for (let i = 0; i < this.chartData.length; i++) {
        const item = this.chartData[i];

        // 实际数据块
        pieData.push(
          {
            value: item.value,
            name: item.name,
            tooltipText: item.tooltipText, // 保留自定义 tooltipText
            itemStyle: {
              normal: {
                borderWidth: 5,
                shadowBlur: 20,
                borderColor: this.defaultColor[i % this.defaultColor.length],
                shadowColor: this.defaultColor[i % this.defaultColor.length],
              },
            },
          },
          // 间隔块
          {
            value: this.gapValue,
            name: '', // 间隔块名称为空
            itemStyle: {
              normal: {
                label: {show: false},
                labelLine: {show: false},
                color: 'rgba(0, 0, 0, 0)', // 透明颜色
                borderColor: 'rgba(0, 0, 0, 0)',
                borderWidth: 0,
              },
            },
            labelLine: {show: false}
          }
        );
      }
      return pieData;
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      this.observeResize();
    });
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
    if (this.resizeObserver && this.$refs.chartRef) {
      // 优先使用 ResizeObserver 销毁监听
      if (typeof ResizeObserver !== 'undefined' && this.resizeObserver.unobserve) {
        this.resizeObserver.unobserve(this.$refs.chartRef);
      }
      this.resizeObserver = null;
    }
    // 移除 window resize 监听 (作为兜底或兼容 IE/旧版浏览器)
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    /**
     * ECharts option 配置对象
     */
    getOption() {
      // 在这里使用 echarts.graphic 确保渐变色函数可用
      const graphic = echarts.graphic;

      return {
        backgroundColor: this.backgroundColor,
        color: this.defaultColor, // 环形图颜色主题

        title: [
          // 总标题
          {
            text: this.chartName,
            left: 'center',
            top: '1%',
            textStyle: {
              color: '#fff',
              fontSize: 20
            }
          },
          // 环形图中心的总计文本
          {
            text: '总计:' + this.chartTotalValue,
            top: '78%',
            textAlign: 'center',
            left: '40%',
            textStyle: {
              color: '#fff',
              fontSize: 16,
              fontWeight: '400'
            }
          },
        ],
        // Legend 移至右下角
        legend: {
          data: this.chartNames,
          orient: 'vertical',
          right: '5%',
          bottom: '10%',
          textStyle: {color: '#fff'}
        },

        // 统一 Tooltip (根据 seriesType 定制内容)
        tooltip: {
          trigger: 'item',
          axisPointer: {type: 'shadow'},
          backgroundColor: 'rgba(50,50,50,0.7)',
          borderColor: '#333',
          borderWidth: 0,
          shadowBlur: 10,
          padding: 10,
          textStyle: {color: '#fff', fontSize: 14},
          formatter: (params) => {
            // 忽略环形图的间隔块
            if (params.name === '' && params.seriesType === 'pie') {
              return '';
            }
            let tooltipHtml = '';

            if (params.seriesType === 'bar') {
              const originalItem = this.chartData[params.dataIndex];
              const name = originalItem.name;
              const value = originalItem.value;

              // 柱形图：name: value + tooltipText
              tooltipHtml = name + '：' + value + '<br/>';

              if (originalItem && originalItem.tooltipText) {
                // 使用 <br/> 替换换行符 \n
                tooltipHtml += originalItem.tooltipText.replace(/\n/g, '<br/>');
              }
            } else if (params.seriesType === 'pie') {
              const value = params.value;
              const percent = ((value / this.chartTotalValue) * 100).toFixed(2);
              const percentText = ' (' + percent + '%)';
              const name = params.name;
              const tooltipText = params.data.tooltipText; // 从预处理数据中获取

              // 环形图：name: value/total (百分比) + tooltipText
              tooltipHtml = name + '：' + value + '/' + this.chartTotalValue + percentText;

              if (tooltipText && tooltipText !== '') {
                tooltipHtml += '<br/>' + tooltipText.replace(/\n/g, '<br/>');
              }
            }

            return tooltipHtml;
          }
        },

        // 布局 grid (柱状图区域)
        grid: {
          left: '3%',
          right: '3%',
          bottom: '45%',
          top: '8%',
          containLabel: true
        },

        xAxis: {
          show: true,
          axisLabel: {show: true, color: '#a2a2a2'},
          axisLine: {show: false, lineStyle: {color: 'red', type: 'dotted'}},
          splitLine: {
            show: true,
            lineStyle: {color: ['rgba(160, 192, 252, 0.2)'], width: 1, type: [5, 8], dashOffset: 2}
          },
        },

        yAxis: [
          // 柱形图 Y 轴 (机构名称)
          {
            data: this.chartNames,
            show: true, inverse: false,
            axisLine: {
              show: true,
              lineStyle: {color: ['rgba(160, 192, 252, 0.2)'], width: 1, type: [5, 8], dashOffset: 2}
            },
            splitLine: {show: false}, axisTick: {show: false},
            axisLabel: {color: '#fff'},
          },
          // 柱形图背景框 Y 轴 (隐藏)
          {show: false, inverse: false, data: []},
        ],

        series: [
          // 1. 柱形图系列 (上部 - 实际值)
          {
            name: '太原市各局值',
            type: 'bar',
            yAxisIndex: 0,
            data: this.chartData,
            barWidth: '50%', barGap: '10%',
            itemStyle: {
              normal: {
                barBorderRadius: 30,
                // 使用 echarts.graphic 实现渐变色
                color: new graphic.LinearGradient(0, 0, 1, 0, [
                  {offset: 0, color: '#28b1ff'},
                  {offset: 1, color: '#00fcff'},
                ]),
              },
            },
            label: {normal: {show: false}},
          },
          // 2. 柱形图背景框系列
          {
            name: '框',
            type: 'bar',
            yAxisIndex: 1,
            // 使用 prop.max 作为背景数据，以填满 X 轴
            data: new Array(this.chartData.length).fill(this.max),
            barWidth: '50%',
            itemStyle: {normal: {color: 'rgba(160, 192, 252, 0.1)', barBorderRadius: 15}},
          },
          // 3. 分段环形图系列 (下部)
          {
            name: '机构数值比例',
            type: 'pie',
            clockWise: false,
            radius: [80, 90],
            center: ['40%', '80%'],
            hoverAnimation: true,
            data: this.pieData, // 使用 computed 属性预处理的数据
            itemStyle: {normal: {}},
            label: {
              show: true,
              position: 'outside',
              color: '#fff',
              // Label 仅对非间隔块显示
              formatter: (params) => {
                if (params.name !== '') {
                  // 计算百分比并显示
                  const percent = ((params.value / this.chartTotalValue) * 100).toFixed(0);
                  return params.name + '\t' + percent + '%';
                } else {
                  return '';
                }
              },
            },
            labelLine: {
              length: 15,
              length2: 15,
              show: true,
              lineStyle: {color: '#00ffff'},
            },
          },
        ],
      };
    },

    // 4. 初始化图表
    initChart() {
      if (!this.$refs.chartRef) return;

      if (this.chart) {
        this.chart.dispose();
        this.chart = null;
      }

      this.chart = echarts.init(this.$refs.chartRef);
      const option = this.getOption();
      this.chart.setOption(option, true);
    },

    // 5. 统一的自适应处理函数和观察者
    handleResize() {
      if (this.chart) {
        this.chart.resize();
      }
    },
    observeResize() {
      // 优先使用 ResizeObserver
      if (typeof ResizeObserver !== 'undefined' && this.$refs.chartRef) {
        this.resizeObserver = new ResizeObserver(() => {
          // 使用 requestAnimationFrame 优化性能
          requestAnimationFrame(this.handleResize);
        });
        this.resizeObserver.observe(this.$refs.chartRef);
      } else {
        // 兼容模式：使用 window resize 事件 (需在 beforeDestroy 移除监听)
        window.addEventListener('resize', this.handleResize);
      }
    }
  },
  // 监听数据变化，重新渲染图表
  watch: {
    chartData: {
      deep: true,
      handler() {
        this.initChart();
      }
    },
    // 如果其他 prop 变化也需要重新渲染，可在此添加监听
    max() {
      this.initChart();
    },
    chartName() {
      this.initChart();
    },
    backgroundColor() {
      this.initChart();
    }
  }
};
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
}
</style>
