<template>
  <div :class="className" :style="{ height, width }" ref="chartRef"/>
</template>

<script>
// 引入 ECharts 库
import echarts from 'echarts';

export default {
  name: 'ScatterRandomCharts',

  // 属性定义
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
      default: '100%'
    },
    chartTitle: {
      type: String,
      default: '行业数据气泡分布图'
    },
    chartSubtitle: {
      type: String,
      default: '基于价值比例和灵活定位'
    },
    chartData: {
      type: Array,
      default: () => [
        { name: "供热管理", value: 888, tooltip: "供热管理是这样的\n需要关注能源消耗和管网效率。" },
        { name: "水利环境", value: 650, tooltip: "水利环境需要对水资源进行监测和保护。" },
        { name: "批发零售", value: 420, tooltip: "批发零售关注库存周转和供应链效率。" },
        { name: "制造业", value: 300, tooltip: "制造业关注产线效率和产品质量。" },
        { name: "房地产", value: 250, tooltip: "房地产关注市场供需和土地利用。" },
        { name: "交通运输", value: 150, tooltip: "交通运输关注物流速度和路网承载力。" },
        { name: "居民服务", value: 120, tooltip: "居民服务关注社区满意度和响应速度。" },
        { name: "教育", value: 90, tooltip: "教育关注教学质量和资源分配。" },
        { name: "金融服务", value: 60, tooltip: "金融服务关注风险控制和资金流动。", position: [10, 10] }
      ]
    },
    backgroundColor: {
      type: String,
      default: 'transparent'
    },
    minSymbolSize: {
      type: Number,
      default: 50
    },
    maxSymbolSize: {
      type: Number,
      default: 200
    },
    defaultColor: {
      type: Array,
      default: () => [
        '#5B8FF9', '#5AD8A6', '#5D7092', '#F6BD16', '#E86A92',
        '#7262FD', '#269A29', '#8E36BE', '#41A7E2', '#7747A3',
        '#FF7F50', '#FFDAB9', '#ADFF2F', '#00CED1', '#9370DB',
        '#3CB371', '#FF69B4', '#FFB6C1', '#DA70D6', '#98FB98',
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
      ]},
    minRandomCoord: {
      type: Number,
      default: 5
    },
    maxRandomCoord: {
      type: Number,
      default: 95
    }
  },

  // 数据状态
  data() {
    return {
      chart: null, // ECharts 实例
    };
  },

  // 生命周期钩子:组件挂载后
  mounted() {
    this.$nextTick(() => {
      this.initChart(this.chartData);
      // 监听窗口尺寸变化
      window.addEventListener('resize', this.handleResize);
    });
  },

  // 生命周期钩子:组件销毁前
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
    window.removeEventListener('resize', this.handleResize);
  },

  // 监听器
  watch: {
    // 监听数据变化,重新渲染图表
    chartData: {
      handler(newData) {
        this.initChart(newData);
      },
      deep: true
    }
  },

  methods: {
    /**
     * @description 计算数据总值
     */
    calculateTotal(data) {
      return data.reduce((sum, item) => sum + (item.value || 0), 0);
    },

    /**
     * @description 生成安全范围内的随机坐标
     */
    getRandomCoordinate() {
      const range = this.maxRandomCoord - this.minRandomCoord + 1;
      return Math.floor(Math.random() * range) + this.minRandomCoord;
    },

    /**
     * @description 根据数据值计算气泡大小
     */
    calculateSymbolSize(value, totalValue) {
      const ratio = value / totalValue;
      return Math.max(
        this.minSymbolSize,
        Math.round(ratio * (this.maxSymbolSize - this.minSymbolSize)) + this.minSymbolSize
      );
    },

    /**
     * @description 检查并返回有效的定位,否则随机生成安全范围内的坐标
     */
    getValidPosition(item) {
      const pos = item.position || item.postion;

      // 如果存在指定坐标且在 [0, 100] 范围内,则使用它
      if (
        pos &&
        Array.isArray(pos) &&
        pos.length === 2 &&
        pos[0] >= 0 && pos[0] <= 100 &&
        pos[1] >= 0 && pos[1] <= 100
      ) {
        return pos;
      } else {
        // 否则,使用安全范围内的随机定位
        return [this.getRandomCoordinate(), this.getRandomCoordinate()];
      }
    },

    /**
     * @description 初始化 ECharts 图表
     */
    initChart(rawData) {
      if (!rawData || rawData.length === 0) {
        if (this.chart) {
          this.chart.dispose();
          this.chart = null;
        }
        return;
      }

      // 销毁旧实例并创建新实例
      if (this.chart) {
        this.chart.dispose();
      }
      this.chart = echarts.init(this.$refs.chartRef);

      const totalValue = this.calculateTotal(rawData);
      const data = [];

      rawData.forEach((item, index) => {
        const finalPosition = this.getValidPosition(item);
        const calculatedSize = this.calculateSymbolSize(item.value, totalValue);

        data.push({
          name: item.name,
          value: finalPosition,
          symbolSize: calculatedSize,
          dataValue: item.value,
          dataTooltip: item.tooltip || '',
          itemStyle: {
            normal: {
              color: new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
                { offset: 0.2, color: 'rgba(27, 54, 72, 0.3)' },
                { offset: 1, color: this.defaultColor[index % this.defaultColor.length] },
              ]),
              borderWidth: 3,
              borderColor: this.defaultColor[index % this.defaultColor.length],
            },
          },
        });
      });

      const option = {
        backgroundColor: this.backgroundColor,
        title: {
          text: this.chartTitle,
          subtext: this.chartSubtitle,
          left: 'center',
          top: 10,
          textStyle: {
            color: '#fff',
            fontSize: 24
          },
          subtextStyle: {
            color: '#aaa',
            fontSize: 14
          }
        },

        dataZoom: [
          {
            type: 'inside',
            xAxisIndex: 0,
            filterMode: 'none',
          },
          {
            type: 'inside',
            yAxisIndex: 0,
            filterMode: 'none',
          }
        ],

        tooltip: {
          trigger: 'item',
          formatter: function (params) {
            const name = params.name;
            const value = params.data.dataValue;
            const customTooltip = params.data.dataTooltip.replace(/\n/g, '<br/>');

            return `<strong>${name}: ${value}</strong><br/>${customTooltip}`;
          },
          backgroundColor: 'rgba(50,50,50,0.7)',
          borderColor: '#fff',
          borderWidth: 1,
          padding: 10,
        },

        grid: {
          show: false,
          top: 60,
          bottom: 10,
          left: 10,
          right: 10
        },

        xAxis: [
          {
            type: 'value',
            show: false,
            min: 0,
            max: 100,
          },
        ],

        yAxis: [
          {
            type: 'value',
            min: 0,
            show: false,
            max: 100,
          },
        ],

        series: [
          {
            type: 'scatter',
            symbol: 'circle',
            label: {
              normal: {
                show: true,
                formatter: '{b}',
                color: '#fff',
                textStyle: {
                  fontSize: '16',
                },
              },
            },
            animationDurationUpdate: 500,
            animationEasingUpdate: 500,
            animationDelay: function (idx) {
              return idx * 100;
            },
            data: data,
          },
        ],
      };

      this.chart.setOption(option);
    },

    /**
     * @description 处理窗口大小变化,调整图表尺寸
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
.chart {
  padding: 10px;
  box-sizing: border-box;
}
</style>
