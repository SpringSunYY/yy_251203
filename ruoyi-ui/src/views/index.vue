<template>
  <div class="dashboard-editor-container">
    <h1 style="text-align: center;font-size: 36px;color: white;font-weight: bold">新能源汽车可视化分析</h1>
    <!-- 搜索栏 -->
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" label-width="80px" class="search-form">
      <el-form-item label="品牌名" prop="brandName">
        <el-input
          v-model="queryParams.brandName"
          placeholder="请输入品牌名"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="系列名称" prop="seriesName">
        <el-input
          v-model="queryParams.seriesName"
          placeholder="请输入系列名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="车型" prop="modelType">
        <el-select v-model="queryParams.modelType" placeholder="请选择车型" clearable>
          <el-option
            v-for="dict in dict.type.manage_model_type"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="能源类型" prop="energyType">
        <el-select v-model="queryParams.energyType" placeholder="请选择能源类型" clearable>
          <el-option
            v-for="dict in dict.type.manage_energy_type"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>
    <el-row :gutter="32">
      <el-col :span="12">
        <div class="chart-wrapper">
          <ScatterRandomCharts :chart-data="carModelType" :chartTitle="carModelTypeName"/>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart-wrapper">
          <BarPieCharts :chart-data="carPrice" :chart-name="carPriceName"/>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="chart-wrapper">
          <LabelValueList :data-list="carCount"/>
          <dv-scroll-ranking-board :config="salesRankConfig" style="width:500px;height:250px"/>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="chart-wrapper">
          <LineBatchZoomCharts :chart-data="carScore" :chart-name="carScoreName"/>
        </div>
      </el-col>
    </el-row>
    <div style="height: 80vh;width: 100%">
      <PieBarCharts :chart-data="carBrand" :chart-name="carBrandName"/>
    </div>
    <div style="height: 100vh;width: 100vw">
      <RelationRoundCharts :chart-name="carRelationName" :chart-data="carRelation"/>
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
import LineBatchZoomCharts from "@/components/Echarts/LineBatchZoomCharts.vue";
import {
  carBrandStatistics, carCountStatistics,
  carModelTypeStatistics,
  carPriceStatistics, carRelationStatistics,
  carSalesRankStatistics,
  carScoreStatistics
} from "@/api/manage/statistics";
import ScatterRandomCharts from "@/components/Echarts/ScatterRandomCharts.vue";
import RelationRoundCharts from "@/components/Echarts/RelationRoundCharts.vue";
import LabelValueList from "@/components/Echarts/LabelValueList.vue";
import {parseTime} from "@/utils/ruoyi";


export default {
  name: 'Index',
  dicts: ["manage_model_type", "manage_energy_type"],
  components: {
    LabelValueList,
    RelationRoundCharts,
    ScatterRandomCharts,
    LineBatchZoomCharts,
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
        rowNum: 8
      },
      carBrand: [],
      carBrandName: "汽车品牌销量分析",
      carPrice: [],
      carPriceName: "汽车价格分析",
      carScore: {},
      carScoreName: "汽车评分分析",
      carModelType: [],
      carModelTypeName: "汽车车型分析",
      carRelation: {},
      carRelationName: "新能源汽车关系图分析",
      carCount: [],
      queryParams: {
        brandName: null,
        seriesName: null,
        modelType: null,
        energyType: null,
      }
    }
  },
  created() {
    this.getStatistics()
  },
  methods: {
    handleQuery() {
      this.getStatistics();
    },
    resetQuery() {
      this.resetForm("queryForm");
      this.getStatistics();
    },
    getStatistics() {
      this.getSalesRankData()
      this.getCarBrand()
      this.getCarPrice()
      this.getCarScore()
      this.getCarModerType()
      this.getCarRelation()
      this.getCarCount()
    },
    getCarCount() {
      carCountStatistics(this.queryParams).then(res => {
        if (res.code !== 200 || !res.data) {
          return
        }
        const now = new Date();
        var data = []
        data.push({
          label: "查询时间",
          //获取当前时间年月日时分
          value: parseTime(now, "{y}-{m}-{d}"),
        })
        res.data.forEach(item => {
          data.push({
            label: item.name,
            value: item.value,
          })
        })
        this.carCount = data
      })
    },
    getSalesRankData() {
      carSalesRankStatistics(this.queryParams).then(res => {
        this.salesRankConfig = {
          ...this.salesRankConfig,
          data: res.data,
        }
        console.log(this.salesRankConfig)
      })
    },
    getCarBrand() {
      carBrandStatistics(this.queryParams).then(res => {
        this.carBrand = res.data
      })
    },
    getCarPrice() {
      carPriceStatistics(this.queryParams).then(res => {
        this.carPrice = res.data
      })
    },
    getCarScore() {
      carScoreStatistics(this.queryParams).then(res => {
        this.carScore = res.data
      })
    },
    getCarModerType() {
      carModelTypeStatistics(this.queryParams).then(res => {
        this.carModelType = res.data
      })
    },
    getCarRelation() {
      carRelationStatistics(this.queryForm).then(res => {
        this.carRelation = res.data
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  background-image: url("../assets/images/index-bg.png");
  background-repeat: no-repeat;
  background-position: center;
  background-attachment: fixed;
  margin-top: -10px; // 抵消默认间距
  padding-top: 10px; // 添加适当内边距
  position: relative;

  .chart-wrapper {
    padding: 16px 16px 0;
    margin-bottom: 32px;
    height: 500px;
  }

  .search-form {
    padding: 10px 20px;
    margin-top: 20px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.6);
  }
}

</style>
