<template>
  <div class="dashboard-editor-container">

  </div>
</template>

<script>

import RelationRoundCharts from "@/components/Echarts/RelationRoundCharts.vue";
import {carRelationStatistics} from "@/api/manage/statistics";


export default {
  name: 'Index',
  components: {
    RelationRoundCharts,
  },
  data() {
    return {
      carRelation:{},
      carRelationName: "新能源汽车关系图分析",
      queryForm: {
        brandName: null,
        seriesName: null,
        modelType: null,
        energyType: null,
      }
    }
  },
  created() {
    this.getCarRelation()
  },
  methods: {
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
  background-image: url("../../../assets/images/index-bg.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  max-height: 95.2vh;
  margin-top: -10px; // 抵消默认间距
  padding-top: 10px; // 添加适当内边距
  position: relative;

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
    height: 500px;
  }
}

</style>
