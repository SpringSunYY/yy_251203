<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <PieBarCharts :chart-data="carBrand" :chart-name="carBrandName"/>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <BarPieCharts :chart-data="carPrice" :chart-name="carPriceName"/>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <dv-scroll-ranking-board :config="salesRankConfig" style="width:500px;height:300px"/>
        </div>
      </el-col>
    </el-row>

    <div style="height: 100vh;width: 100vw">
      <RelationRoundCharts/>
    </div>
    <div style="height: 80vh;width: 100%">
      <LineBatchZoomCharts :chart-data="carScore" :chart-name="carScoreName"/>
    </div>
    <div style="height: 80vh;width: 100%">
      <ScatterRandomCharts :chart-data="carModelType" :chart-name="carModelTypeName"/>
    </div>
  </div>
</template>

<script>
import PanelGroup from './dashboard/PanelGroup'
import LineChart from './dashboard/LineChart'
import RaddarChart from './dashboard/RaddarChart'
import PieChart from './dashboard/PieChart'
import BarChart from './dashboard/BarChart'
import PieBarCharts from "@/components/Echarts/PieBarCharts.vue";
import BarPieCharts from "@/components/Echarts/BarPieCharts.vue";
import RelationRoundCharts from "@/components/Echarts/RelationRoundCharts.vue";
import LineBatchZoomCharts from "@/components/Echarts/LineBatchZoomCharts.vue";
import {
  carBrandStatistics, carModelTypeStatistics,
  carPriceStatistics,
  carSalesRankStatistics,
  carScoreStatistics
} from "@/api/manage/statistics";
import ScatterRandomCharts from "@/components/Echarts/ScatterRandomCharts.vue";


export default {
  name: 'Index',
  components: {
    ScatterRandomCharts,
    LineBatchZoomCharts,
    RelationRoundCharts,
    BarPieCharts,
    PieBarCharts,
    PanelGroup,
    LineChart,
    RaddarChart,
    PieChart,
    BarChart
  },
  data() {
    return {
      salesRankConfig: {
        data: [],
      },
      carBrand: [],
      carBrandName: "汽车品牌销量分析",
      carPrice: [],
      carPriceName: "汽车价格分析",
      carScore: {},
      carScoreName: "汽车评分分析",
      carModelType: [],
      carModelTypeName: "汽车车型分析",
      query: {
        brandName: null,
        seriesName: null,
        modelType: null,
        energyType: null,
      }
    }
  },
  created() {
    this.getSalesRankData()
    this.getCarBrand()
    this.getCarPrice()
    this.getCarScore()
    this.getCarModerType()
  },
  methods: {
    getSalesRankData() {
      carSalesRankStatistics(this.query).then(res => {
        this.salesRankConfig = {
          ...this.salesRankConfig,
          data: res.data,
        }
        console.log(this.salesRankConfig)
      })
    },
    getCarBrand() {
      carBrandStatistics(this.query).then(res => {
        this.carBrand = res.data
      })
    },
    getCarPrice() {
      carPriceStatistics(this.query).then(res => {
        this.carPrice = res.data
      })
    },
    getCarScore() {
      carScoreStatistics(this.query).then(res => {
        this.carScore = res.data
      })
    },
    getCarModerType() {
      carModelTypeStatistics(this.query).then(res => {
        this.carModelType = res.data
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
    height: 500px;
  }
}

@media (max-width: 1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
