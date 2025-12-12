<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="编号" prop="carId">
        <el-input
          v-model="queryParams.carId"
          placeholder="请输入编号"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
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
      <el-form-item label="车系ID" prop="seriesId">
        <el-input
          v-model="queryParams.seriesId"
          placeholder="请输入车系ID"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="价格" prop="dealerPrice">
        <el-input
          v-model="queryParams.dealerPrice"
          placeholder="请输入价格"
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
      <el-form-item label="上市时间" prop="marketTime">
        <el-date-picker
          v-model="dateRangeMarketTime"
          value-format="yyyy-MM-dd"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        ></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['manage:car:add']"
        >新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['manage:car:edit']"
        >修改
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['manage:car:remove']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['manage:car:export']"
        >导出
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-upload2"
          size="mini"
          @click="handleImport"
          v-hasPermi="['manage:car:import']"
        >导入
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>
    </el-row>

    <el-table :loading="loading" :data="carList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="编号" :show-overflow-tooltip="true" v-if="columns[0].visible" prop="carId"/>
      <el-table-column label="品牌名" align="center" :show-overflow-tooltip="true" v-if="columns[1].visible"
                       prop="brandName"/>
      <el-table-column label="封面" align="center" v-if="columns[2].visible" prop="image" width="100">
        <template slot-scope="scope">
          <image-preview :src="scope.row.image" :width="50" :height="50"/>
        </template>
      </el-table-column>
      <el-table-column label="系列名称" align="center" :show-overflow-tooltip="true" v-if="columns[3].visible"
                       prop="seriesName"/>
      <el-table-column label="车系ID" align="center" :show-overflow-tooltip="true" v-if="columns[4].visible"
                       prop="seriesId"/>
      <el-table-column label="价格" align="center" :show-overflow-tooltip="true" v-if="columns[5].visible"
                       prop="dealerPrice"/>
      <el-table-column label="最大价格" align="center" :show-overflow-tooltip="true" v-if="columns[6].visible"
                       prop="maxPrice"/>
      <el-table-column label="最低价格" align="center" :show-overflow-tooltip="true" v-if="columns[7].visible"
                       prop="minPrice"/>
      <el-table-column label="销量" align="center" :show-overflow-tooltip="true" v-if="columns[8].visible"
                       prop="salesCount"/>
      <el-table-column label="车型" align="center" v-if="columns[9].visible" prop="modelType">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.manage_model_type" :value="scope.row.modelType"/>
        </template>
      </el-table-column>
      <el-table-column label="能源类型" align="center" v-if="columns[10].visible" prop="energyType">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.manage_energy_type" :value="scope.row.energyType"/>
        </template>
      </el-table-column>
      <el-table-column label="上市时间" align="center" v-if="columns[11].visible" prop="marketTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.marketTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="综合评分" align="center" :show-overflow-tooltip="true" v-if="columns[12].visible"
                       prop="overall"/>
      <el-table-column label="外观评分" align="center" :show-overflow-tooltip="true" v-if="columns[13].visible"
                       prop="exterior"/>
      <el-table-column label="内饰评分" align="center" :show-overflow-tooltip="true" v-if="columns[14].visible"
                       prop="interior"/>
      <el-table-column label="空间评分" align="center" :show-overflow-tooltip="true" v-if="columns[15].visible"
                       prop="space"/>
      <el-table-column label="操控评分" align="center" :show-overflow-tooltip="true" v-if="columns[16].visible"
                       prop="handling"/>
      <el-table-column label="舒适性评分" align="center" :show-overflow-tooltip="true" v-if="columns[17].visible"
                       prop="comfort"/>
      <el-table-column label="动力评分" align="center" :show-overflow-tooltip="true" v-if="columns[18].visible"
                       prop="power"/>
      <el-table-column label="配置评分" align="center" :show-overflow-tooltip="true" v-if="columns[19].visible"
                       prop="configuration"/>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['manage:car:edit']"
          >修改
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['manage:car:remove']"
          >删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改汽车信息对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="品牌名" prop="brandName">
          <el-input v-model="form.brandName" placeholder="请输入品牌名"/>
        </el-form-item>
        <el-form-item label="系列名称" prop="seriesName">
          <el-input v-model="form.seriesName" placeholder="请输入系列名称"/>
        </el-form-item>
        <el-form-item label="车系ID" prop="seriesId">
          <el-input v-model="form.seriesId" placeholder="请输入车系ID"/>
        </el-form-item>
        <el-form-item label="价格" prop="dealerPrice">
          <el-input v-model="form.dealerPrice" placeholder="请输入价格"/>
        </el-form-item>
        <el-form-item label="最大价格" prop="maxPrice">
          <el-input v-model="form.maxPrice" placeholder="请输入最大价格"/>
        </el-form-item>
        <el-form-item label="最低价格" prop="minPrice">
          <el-input v-model="form.minPrice" placeholder="请输入最低价格"/>
        </el-form-item>
        <el-form-item label="销量" prop="salesCount">
          <el-input v-model="form.salesCount" placeholder="请输入销量"/>
        </el-form-item>
        <el-form-item label="车型" prop="modelType">
          <el-select v-model="form.modelType" placeholder="请选择车型">
            <el-option
              v-for="dict in dict.type.manage_model_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="能源类型" prop="energyType">
          <el-select v-model="form.energyType" placeholder="请选择能源类型">
            <el-option
              v-for="dict in dict.type.manage_energy_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上市时间" prop="marketTime">
          <el-date-picker clearable
                          v-model="form.marketTime"
                          type="date"
                          value-format="yyyy-MM-dd"
                          placeholder="选择上市时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="综合评分" prop="overall">
          <el-input-number :precision="2" v-model="form.overall" placeholder="请输入综合评分"/>
        </el-form-item>
        <el-form-item label="外观评分" prop="exterior">
          <el-input-number :precision="2" v-model="form.exterior" placeholder="请输入外观评分"/>
        </el-form-item>
        <el-form-item label="内饰评分" prop="interior">
          <el-input-number :precision="2" v-model="form.interior" placeholder="请输入内饰评分"/>
        </el-form-item>
        <el-form-item label="空间评分" prop="space">
          <el-input-number :precision="2" v-model="form.space" placeholder="请输入空间评分"/>
        </el-form-item>
        <el-form-item label="操控评分" prop="handling">
          <el-input-number :precision="2" v-model="form.handling" placeholder="请输入操控评分"/>
        </el-form-item>
        <el-form-item label="舒适性评分" prop="comfort">
          <el-input-number :precision="2" v-model="form.comfort" placeholder="请输入舒适性评分"/>
        </el-form-item>
        <el-form-item label="动力评分" prop="power">
          <el-input-number :precision="2" v-model="form.power" placeholder="请输入动力评分"/>
        </el-form-item>
        <el-form-item label="配置评分" prop="configuration">
          <el-input-number :precision="2" v-model="form.configuration" placeholder="请输入配置评分"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 导入对话框 -->
    <el-dialog :title="upload.title" :visible.sync="upload.open" width="400px" append-to-body>
      <el-upload
        ref="upload"
        :limit="1"
        accept=".xlsx, .xls"
        :headers="upload.headers"
        :action="upload.url + '?updateSupport=' + upload.updateSupport"
        :disabled="upload.isUploading"
        :on-progress="handleFileUploadProgress"
        :on-success="handleFileSuccess"
        :auto-upload="false"
        drag
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip text-center" slot="tip">
          <div class="el-upload__tip" slot="tip">
            <el-checkbox v-model="upload.updateSupport"/>
            是否更新已经存在的汽车信息数据
          </div>
          <span>仅允许导入xls、xlsx格式文件。</span>
          <el-link type="primary" :underline="false" style="font-size:12px;vertical-align: baseline;"
                   @click="importTemplate">下载模板
          </el-link>
        </div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitFileForm">确 定</el-button>
        <el-button @click="upload.open = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>


import {listCar, getCar, delCar, addCar, updateCar} from "@/api/manage/car";
import {getToken} from "@/utils/auth";

export default {
  name: "Car",
  dicts: ['manage_model_type', 'manage_energy_type'],
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 汽车信息表格数据
      carList: [],
      // 表格列信息
      columns: [
        {key: 0, label: '编号', visible: false},
        {key: 1, label: '品牌名', visible: true},
        {key: 2, label: '封面', visible: true},
        {key: 3, label: '系列名称', visible: true},
        {key: 4, label: '车系ID', visible: true},
        {key: 5, label: '价格', visible: true},
        {key: 6, label: '最大价格', visible: true},
        {key: 7, label: '最低价格', visible: true},
        {key: 8, label: '销量', visible: true},
        {key: 9, label: '车型', visible: true},
        {key: 10, label: '能源类型', visible: true},
        {key: 11, label: '上市时间', visible: true},
        {key: 12, label: '综合评分', visible: true},
        {key: 13, label: '外观评分', visible: false},
        {key: 14, label: '内饰评分', visible: false},
        {key: 15, label: '空间评分', visible: false},
        {key: 16, label: '操控评分', visible: false},
        {key: 17, label: '舒适性评分', visible: false},
        {key: 18, label: '动力评分', visible: false},
        {key: 19, label: '配置评分', visible: false}
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 上市时间时间范围
      dateRangeMarketTime: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        carId: null,
        brandName: null,
        seriesName: null,
        seriesId: null,
        dealerPrice: null,
        modelType: null,
        energyType: null,
        marketTime: null,
      },
      // 表单参数
      form: {},
      // 导入参数
      upload: {
        // 是否显示弹出层（导入）
        open: false,
        // 弹出层标题（导入）
        title: "",
        // 是否禁用上传
        isUploading: false,
        // 是否更新已经存在的汽车信息数据
        updateSupport: 0,
        // 设置上传的请求头部
        headers: {Authorization: "Bearer " + getToken()},
        // 上传的地址
        url: process.env.VUE_APP_BASE_API + "/manage/car/importData"
      },
      // 表单校验
      rules: {
        carId: [
          {required: true, message: "编号不能为空", trigger: "blur"}
        ]
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询汽车信息列表 */
    getList() {
      this.loading = true;
      this.queryParams.params = {};
      if (null != this.dateRangeMarketTime && '' != this.dateRangeMarketTime.toString()) {
        this.queryParams.params["beginMarketTime"] = this.dateRangeMarketTime[0];
        this.queryParams.params["endMarketTime"] = this.dateRangeMarketTime[1];
      }
      listCar(this.queryParams).then(response => {
        this.carList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        carId: null,
        brandName: null,
        image: null,
        seriesName: null,
        seriesId: null,
        dealerPrice: null,
        maxPrice: null,
        minPrice: null,
        salesCount: null,
        modelType: null,
        energyType: null,
        marketTime: null,
        overall: null,
        exterior: null,
        interior: null,
        space: null,
        handling: null,
        comfort: null,
        power: null,
        configuration: null
      };
      this.resetForm("form");
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.dateRangeMarketTime = [];
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.carId)
      this.single = selection.length !== 1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加汽车信息";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const carId = row.carId || this.ids
      getCar(carId).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改汽车信息";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          const submitData = this.buildSubmitData();
          if (submitData.carId != null) {
            updateCar(submitData).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addCar(submitData).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const carIds = row.carId || this.ids;
      this.$modal.confirm('是否确认删除汽车信息编号为"' + carIds + '"的数据项？').then(function () {
        return delCar(carIds);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {
      });
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('manage/car/export', {
        ...this.queryParams
      }, `car_${new Date().getTime()}.xlsx`)
    },
    /** 导入按钮操作 */
    handleImport() {
      this.upload.title = "汽车信息导入";
      this.upload.open = true;
    },
    /** 下载模板操作 */
    importTemplate() {
      this.download(
        "manage/car/importTemplate",
        {},
        "car_template_" + new Date().getTime() + ".xlsx"
      );
    },
    // 文件上传中处理
    handleFileUploadProgress(event, file, fileList) {
      this.upload.isUploading = true;
    },
    // 文件上传成功处理
    handleFileSuccess(response, file, fileList) {
      this.upload.open = false;
      this.upload.isUploading = false;
      this.$refs.upload.clearFiles();
      this.$alert("<div style='overflow: auto;overflow-x: hidden;max-height: 70vh;padding: 10px 20px 0;'>" + response.msg + "</div>", "导入结果", {dangerouslyUseHTMLString: true});
      this.$modal.closeLoading()
      this.getList();
    },
    buildSubmitData() {
      const data = {...this.form};
      if (data.carId !== null && data.carId !== undefined && data.carId !== "") {
        data.carId = parseInt(data.carId, 10);
      } else {
        data.carId = null;
      }
      if (data.maxPrice !== null && data.maxPrice !== undefined && data.maxPrice !== "") {
        data.maxPrice = parseFloat(data.maxPrice);
      } else {
        data.maxPrice = null;
      }
      if (data.minPrice !== null && data.minPrice !== undefined && data.minPrice !== "") {
        data.minPrice = parseFloat(data.minPrice);
      } else {
        data.minPrice = null;
      }
      if (data.salesCount !== null && data.salesCount !== undefined && data.salesCount !== "") {
        data.salesCount = parseInt(data.salesCount, 10);
      } else {
        data.salesCount = null;
      }
      if (data.overall !== null && data.overall !== undefined && data.overall !== "") {
        data.overall = parseFloat(data.overall);
      } else {
        data.overall = null;
      }
      if (data.exterior !== null && data.exterior !== undefined && data.exterior !== "") {
        data.exterior = parseFloat(data.exterior);
      } else {
        data.exterior = null;
      }
      if (data.interior !== null && data.interior !== undefined && data.interior !== "") {
        data.interior = parseFloat(data.interior);
      } else {
        data.interior = null;
      }
      if (data.space !== null && data.space !== undefined && data.space !== "") {
        data.space = parseFloat(data.space);
      } else {
        data.space = null;
      }
      if (data.handling !== null && data.handling !== undefined && data.handling !== "") {
        data.handling = parseFloat(data.handling);
      } else {
        data.handling = null;
      }
      if (data.comfort !== null && data.comfort !== undefined && data.comfort !== "") {
        data.comfort = parseFloat(data.comfort);
      } else {
        data.comfort = null;
      }
      if (data.power !== null && data.power !== undefined && data.power !== "") {
        data.power = parseFloat(data.power);
      } else {
        data.power = null;
      }
      if (data.configuration !== null && data.configuration !== undefined && data.configuration !== "") {
        data.configuration = parseFloat(data.configuration);
      } else {
        data.configuration = null;
      }
      return data;
    },
    // 提交上传文件
    submitFileForm() {
      this.$modal.loading("导入中请稍后")
      this.$refs.upload.submit();
    }
  }
};
</script>
