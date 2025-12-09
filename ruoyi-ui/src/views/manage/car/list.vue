<template>
  <div class="app-container">
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

    <!-- 统计信息 -->
    <div class="total-info">
      <span class="total-text">共找到 <strong>{{ total }}</strong> 条车辆</span>
    </div>

    <!-- 卡片列表容器 -->
    <div class="card-container masonry-container" v-loading="loading">
      <div class="masonry-wrapper">
        <div v-for="item in carList" :key="item.carId" class="masonry-item">
          <el-card class="car-card" shadow="hover">
            <div class="card-image" :class="{'no-image': !item.image}">
              <template v-if="item.image">
                <image-preview class="card-photo" :src="item.image" :width="320" :height="180"/>
              </template>
              <template v-else>
                <div class="image-placeholder">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </template>
            </div>

            <div class="name-line">
              <div class="brand">{{ item.brandName || '未命名品牌' }}/{{ item.seriesName || '-' }}</div>
            </div>

            <div class="card-content">
              <div class="info-item price">
                <i class="el-icon-coin"></i>
                <span class="label">价格：</span>
                <span class="value highlight">{{ item.dealerPrice || '暂无报价' }}</span>
              </div>

              <div class="info-item">
                <i class="el-icon-s-data"></i>
                <span class="label">销量：</span>
                <span class="value">{{ item.salesCount != null ? item.salesCount : '—' }}</span>
              </div>

              <div class="info-item">
                <i class="el-icon-timer"></i>
                <span class="label">上市：</span>
                <span class="value">{{ item.marketTime ? parseTime(item.marketTime, '{y}-{m}') : '—' }}</span>
              </div>


              <div class="info-item tags">
                <i class="el-icon-collection-tag"></i>
                <span class="label">标签：</span>
                <div class="tag-line">
                  <dict-tag :options="dict.type.manage_model_type" :value="item.modelType"/>
                  <dict-tag :options="dict.type.manage_energy_type" :value="item.energyType"/>
                </div>
              </div>

              <div class=" scores" v-if="builderChartData(item).length>1">
                <RadarTooltipCharts :chart-name="item.overall" :max="5" :chart-data="builderChartData(item)"
                                    background-color="rgba(50,50,50,0.3)"/>
              </div>

              <div class="detail-link">
                <el-button type="text" icon="el-icon-link" @click="openDetail(item.seriesId)">查看详情</el-button>
              </div>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 加载提示 -->
      <div class="load-more-tip" v-if="hasMore">
        <i class="el-icon-loading" v-if="loadingMore"></i>
        <span>{{ loadingMore ? '加载中...' : '滚动加载更多' }}</span>
      </div>
      <div class="load-more-tip no-more" v-if="!hasMore && carList.length > 0">
        <span>没有更多数据了</span>
      </div>
      <div class="empty-tip" v-if="!loading && carList.length === 0">
        <el-empty description="暂无数据"></el-empty>
      </div>
    </div>
  </div>
</template>

<script>
import {listCar} from "@/api/manage/car";
import RadarTooltipCharts from "@/components/Echarts/RadarTooltipCharts.vue";

export default {
  name: "CarList",
  components: {RadarTooltipCharts},
  dicts: ["manage_model_type", "manage_energy_type"],
  data() {
    return {
      loading: false,
      loadingMore: false,
      carList: [],
      total: 0,
      dateRangeMarketTime: [],
      queryParams: {
        pageNum: 1,
        pageSize: 20,
        carId: null,
        brandName: null,
        seriesName: null,
        seriesId: null,
        dealerPrice: null,
        modelType: null,
        energyType: null,
        marketTime: null
      },
      hasMore: true,
      scrollTimer: null
    };
  },
  created() {
    this.getList(true);
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.handleScroll);
    if (this.scrollTimer) {
      clearTimeout(this.scrollTimer);
    }
  },
  methods: {
    builderChartData(item) {
      if (!item) {
        return [];
      }
      if (!item.overall || !item.exterior || !item.power || !item.handling || !item.space || !item.configuration) {
        return [];
      }
      return [
        {name: '外观', value: item.exterior, tooltip: '外观评分'},
        {name: '内饰', value: item.interior, tooltip: '内饰评分'},
        {name: '动力', value: item.power, tooltip: '动力评分'},
        {name: '操控', value: item.handling, tooltip: '操控评分'},
        {name: '空间', value: item.space, tooltip: '空间评分'},
        {name: '配置', value: item.configuration, tooltip: '油耗评分'},
      ]
    },
    buildQuery() {
      const params = {...this.queryParams, params: {}};
      if (this.dateRangeMarketTime && this.dateRangeMarketTime.length === 2) {
        params.params.beginMarketTime = this.dateRangeMarketTime[0];
        params.params.endMarketTime = this.dateRangeMarketTime[1];
      }
      return params;
    },
    getList(reset = false) {
      if (reset) {
        this.queryParams.pageNum = 1;
        this.carList = [];
        this.hasMore = true;
        this.loading = true;
      } else {
        this.loadingMore = true;
      }
      listCar(this.buildQuery())
        .then(response => {
          const rows = response.rows || [];
          if (reset) {
            this.carList = rows;
          } else {
            this.carList = [...this.carList, ...rows];
          }
          this.total = response.total || 0;
          this.hasMore = this.carList.length < this.total;
        })
        .finally(() => {
          this.loading = false;
          this.loadingMore = false;
        });
    },
    loadMore() {
      if (this.loading || this.loadingMore || !this.hasMore) return;
      this.queryParams.pageNum += 1;
      this.getList(false);
    },
    handleQuery() {
      this.getList(true);
    },
    resetQuery() {
      this.dateRangeMarketTime = [];
      this.resetForm("queryForm");
      this.getList(true);
    },
    openDetail(seriesId) {
      const sid = seriesId || "";
      const url = `https://www.dongchedi.com/auto/series/${sid || 398}`;
      window.open(url, "_blank");
    },
    handleScroll() {
      if (this.loading || this.loadingMore || !this.hasMore) return;
      if (this.scrollTimer) clearTimeout(this.scrollTimer);
      this.scrollTimer = setTimeout(() => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        const documentHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
        if (scrollTop + windowHeight >= documentHeight - 200) {
          this.loadMore();
        }
      }, 100);
    }
  }
};
</script>

<style scoped>
.app-container {
  padding: 20px;
  background: #f6f7fb;
}

.search-form {
  background: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}

.total-info {
  background: #fff;
  padding: 14px 18px;
  margin-bottom: 18px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}

.total-text {
  font-size: 14px;
  color: #606266;
}

.total-text strong {
  color: #409eff;
  font-size: 18px;
  font-weight: 600;
  margin: 0 4px;
}

.card-container {
  min-height: 400px;
  padding: 10px 0;
}

.masonry-container {
  width: 100%;
}

.masonry-wrapper {
  column-count: 4;
  column-gap: 20px;
  column-fill: balance;
}

.masonry-item {
  break-inside: avoid;
  margin-bottom: 20px;
  display: inline-block;
  width: 100%;
}

.car-card {
  width: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
  border-radius: 10px;
  overflow: hidden;
}

.car-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
}

.card-image {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  min-height: 180px;
  background: linear-gradient(135deg, #f8fafc, #eef2f8);
}

.card-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-placeholder {
  width: 100%;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #b8c2d1;
  font-size: 28px;
}

.name-line {
  padding: 12px 14px 6px;
}

.brand {
  font-size: 17px;
  font-weight: 700;
  color: #303133;
  line-height: 22px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.series {
  margin-top: 2px;
  color: #909399;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-content {
  padding: 14px 18px 16px;
  display: flex;
  flex-direction: column;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
  color: #606266;
}

.info-item i {
  margin-right: 8px;
  color: #909399;
  font-size: 16px;
  width: 18px;
  text-align: center;
}

.info-item .label {
  margin-right: 6px;
  color: #909399;
  min-width: 54px;
}

.info-item .value {
  flex: 1;
  color: #303133;
  word-break: break-all;
}

.info-item.price {
  padding-bottom: 12px;
  margin-bottom: 14px;
  border-bottom: 1px dashed #e4e7ed;
}

.info-item .highlight {
  color: #f56c6c;
  font-weight: 700;
  font-size: 16px;
}

.scores {
  height: 300px;
}

.tag-line {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.score-line {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  color: #475164;
}

.detail-link {
  text-align: right;
  margin-top: 8px;
}

.detail-link .el-button {
  padding: 0;
}

.load-more-tip {
  text-align: center;
  padding: 20px;
  color: #909399;
  font-size: 14px;
}

.load-more-tip i {
  margin-right: 8px;
  animation: rotating 2s linear infinite;
}

.load-more-tip.no-more {
  color: #c0c4cc;
}

.empty-tip {
  padding: 60px 0;
}

@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 1600px) {
  .masonry-wrapper {
    column-count: 3;
  }
}

@media (max-width: 1200px) {
  .masonry-wrapper {
    column-count: 2;
  }
}

@media (max-width: 800px) {
  .masonry-wrapper {
    column-count: 1;
  }

  .card-content {
    padding: 15px;
  }

  .info-item {
    font-size: 13px;
    margin-bottom: 10px;
  }
}
</style>

