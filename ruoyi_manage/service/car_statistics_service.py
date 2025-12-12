from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR
from typing import List

from ruoyi_common.utils import DateUtil
from ruoyi_manage.domain.entity import CarInfo
from ruoyi_manage.domain.statistics.vo.statistics_vo import PieBarStatisticsVo, BatchLineStatisticsVo, BatchLineItem, \
    StatisticsVo, RelationStatisticsVo
from ruoyi_manage.mapper import CarStatisticsMapper, CarInfoMapper


class CarStatisticsService:
    """汽车信息统计服务类"""

    def get_car_sales_rank_statistics(self, request) -> List[StatisticsVo]:
        """
        获取汽车销量排行

        Args:
            request: 请求参数

        Returns:
            List[CarInfo]: 汽车信息列表
        """
        pos = CarStatisticsMapper.get_car_sales_rank_statistics(request)
        if pos:
            return [StatisticsVo(name=po.name, value=po.value) for po in pos]
        return []

    def get_car_brand_statistics(self, request) -> List[PieBarStatisticsVo]:
        """
        获取汽车品牌统计
        """
        # 首先查询到前十的品牌
        brand_pos = CarStatisticsMapper.get_car_brand_statistics(request)
        # 然后查询到对应品牌的车系
        results = []
        rank = 1
        for brand_po in brand_pos:
            # 创建带有品牌名称的查询参数副本，避免修改原请求对象（pydantic BaseModel 默认冻结）
            brand_request = request.model_copy(update={"brand_name": brand_po.name})
            series_pos = CarStatisticsMapper.get_car_sales_rank_statistics(brand_request)
            results.append(
                PieBarStatisticsVo(
                    name=brand_po.name,
                    tooltipText=f"排名：{rank}",
                    values=[StatisticsVo(name=series_po.name, value=series_po.value) for series_po in series_pos],
                )
            )
            rank += 1
        return results

    def get_car_price_statistics(self, request) -> List[StatisticsVo]:
        ###汽车价格分析
        # 先获取到所有的汽车
        car_info = CarInfo()
        car_info.brand_name = request.brand_name
        car_info.series_name = request.series_name
        car_info.model_type = request.model_type
        car_info.energy_type = request.energy_type
        pos = CarInfoMapper.select_car_info_list(car_info)
        if not pos:
            return []
        ###根据价格分类，十万以下，10万到20万，20万到30万，30万到40万，40万以上
        ###计算其总销量,每个范围的,数据保存单位是万
        results = {"10万以下": 0, "10万到20万": 0, "20万到30万": 0, "30万到40万": 0, "40万以上": 0}
        for po in pos:
            if po.max_price < 10:
                results["10万以下"] += po.sales_count
            elif 10 <= po.max_price < 20:
                results["10万到20万"] += po.sales_count
            elif 20 <= po.max_price < 30:
                results["20万到30万"] += po.sales_count
            elif 30 <= po.max_price < 40:
                results["30万到40万"] += po.sales_count
            elif po.max_price >= 40:
                results["40万以上"] += po.sales_count
        return [StatisticsVo(name=key, value=value) for key, value in results.items()]

    def get_car_score_statistics(self, request) -> BatchLineStatisticsVo:
        """
        汽车评分维度分析
        - 汇总所有维度的评分，取全局最小/最大评分（向下/向上取一位小数）
        - names：从最小到最大，步进 0.1 的评分档位字符串（如 2.5, 2.6, ...）
        - 每个维度生成一个 BatchLineItem，values 为各档位销量求和（按向下取一位小数归档）
        """
        # 综合评分
        overall_pos = CarStatisticsMapper.get_car_score_statistics(request, "overall")
        # 外观评分
        exterior_pos = CarStatisticsMapper.get_car_score_statistics(request, "exterior")
        # 内饰评分
        interior_pos = CarStatisticsMapper.get_car_score_statistics(request, "interior")
        # 空间评分
        space_pos = CarStatisticsMapper.get_car_score_statistics(request, "space")
        # 操控评分
        handling_pos = CarStatisticsMapper.get_car_score_statistics(request, "handling")
        # 舒适性评分
        comfort_pos = CarStatisticsMapper.get_car_score_statistics(request, "comfort")
        # 动力评分
        power_pos = CarStatisticsMapper.get_car_score_statistics(request, "power")
        # 配置评分
        configuration_pos = CarStatisticsMapper.get_car_score_statistics(request, "configuration")
        score_series_map = {
            "综合评分": overall_pos,
            "外观评分": exterior_pos,
            "内饰评分": interior_pos,
            "空间评分": space_pos,
            "操控评分": handling_pos,
            "舒适性评分": comfort_pos,
            "动力评分": power_pos,
            "配置评分": configuration_pos,
        }

        def safe_decimal(value) -> Decimal | None:
            if value is None:
                return None
            try:
                return Decimal(str(value))
            except (InvalidOperation, ValueError, TypeError):
                return None

        # 收集全局评分最小、最大值
        score_values: List[Decimal] = []
        for series in score_series_map.values():
            for item in series:
                decimal_score = safe_decimal(item.name)
                if decimal_score is not None:
                    score_values.append(decimal_score)

        if not score_values:
            # 无数据时给出 0.0-5.0 的默认刻度，values 全 0，避免前端空数组
            default_names = [f"{Decimal(i) / Decimal(10):.1f}" for i in range(0, 51)]  # 0.0 -> 5.0
            empty_values = [0 for _ in default_names]
            batch_values: List[BatchLineItem] = []
            for label in score_series_map.keys():
                batch_values.append(BatchLineItem(name=label, values=list(empty_values)))
            return BatchLineStatisticsVo(names=default_names, values=batch_values)

        step = Decimal("0.1")
        min_score = min(score_values)
        max_score = max(score_values)

        # 向下/向上一位小数确定边界
        start = (min_score * 10).to_integral_value(rounding=ROUND_FLOOR) / Decimal(10)
        end = (max_score * 10).to_integral_value(rounding=ROUND_CEILING) / Decimal(10)

        # names 升序 0.1 步进
        names: List[str] = []
        current = start
        while current <= end:
            names.append(f"{current:.1f}")
            current += step

        # 将评分按向下取一位小数归档并求和销量
        def bucketize(series):
            bucket_dict = {name: 0 for name in names}
            for item in series:
                decimal_score = safe_decimal(item.name)
                if decimal_score is None:
                    continue
                bucket = (decimal_score * 10).to_integral_value(rounding=ROUND_FLOOR) / Decimal(10)
                bucket_name = f"{bucket:.1f}"
                if bucket_name in bucket_dict:
                    bucket_dict[bucket_name] += int(item.value)
            return [bucket_dict.get(name, 0) for name in names]

        batch_values: List[BatchLineItem] = []
        for label, series in score_series_map.items():
            batch_values.append(BatchLineItem(name=label, values=bucketize(series)))

        return BatchLineStatisticsVo(names=names, values=batch_values)

    def get_car_model_type_statistics(self, request) -> List[StatisticsVo]:
        """汽车车型分析"""
        pos = CarStatisticsMapper.get_car_model_type_statistics(request)
        return [StatisticsVo(name=po.name, value=po.value) for po in pos]

    def get_car_relation_statistics(self, request) -> RelationStatisticsVo:
        """汽车关系分析"""
        ###首先拿到车车型
        model_pos = CarStatisticsMapper.get_car_model_type_statistics(request)
        if not model_pos:
            return RelationStatisticsVo(name="汽车关系分析", value=0, tooltipText=None, children=[])
        # 构建结果
        # 销售总数，车型总销量
        sales_count = 0
        results_children = []
        for model_po in model_pos:
            sales_count += model_po.value
            model_children = []
            # 获取到品牌，每种类型
            brand_request = request.model_copy(update={"model_type": model_po.name})
            brand_pos = CarStatisticsMapper.get_car_brand_statistics(brand_request)
            for brand_po in brand_pos:
                # 获取到车系
                series_request = brand_request.model_copy(update={"brand_name": brand_po.name})
                series_pos = CarStatisticsMapper.get_car_sales_rank_statistics(series_request)
                series_children = [
                    RelationStatisticsVo(name=series_po.name, value=series_po.value, tooltipText=None, children=[])
                    for series_po in series_pos
                ]
                model_children.append(
                    RelationStatisticsVo(
                        name=brand_po.name,
                        value=brand_po.value,
                        tooltipText=None,
                        children=series_children,
                    )
                )
            results_children.append(
                RelationStatisticsVo(
                    name=model_po.name,
                    value=model_po.value,
                    tooltipText=None,
                    children=model_children,
                )
            )
        return RelationStatisticsVo(name="汽车关系分析", value=sales_count, tooltipText=None, children=results_children)

    def get_car_count_statistics(self, request) -> List[StatisticsVo]:
        vos = []
        # 汽车NO1
        series_car_pos = CarStatisticsMapper.get_car_sales_rank_statistics(request, limit=1000)
        # 汽车系列数
        vos.append(StatisticsVo(name="汽车系列数", value=len(series_car_pos)))
        # 汽车品牌
        brand_pos = CarStatisticsMapper.get_car_brand_statistics(request, 1000)
        # 汽车品牌数
        vos.append(StatisticsVo(name="汽车品牌数", value=len(brand_pos)))
        # 总销量
        sales_count = CarStatisticsMapper.get_car_sales_count_statistics(request)
        vos.append(StatisticsVo(name="总销量", value=sales_count))
        vos.append(StatisticsVo(name="系列：" + series_car_pos[0].name, value=series_car_pos[0].value))
        vos.append(StatisticsVo(name="品牌：" + brand_pos[0].name, value=brand_pos[0].value))
        return vos
