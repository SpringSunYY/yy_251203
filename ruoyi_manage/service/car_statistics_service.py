from typing import List

from ruoyi_manage.domain.statistics.vo import StatisticsVo
from ruoyi_manage.domain.statistics.vo.statistics_vo import PieBarStatisticsVo
from ruoyi_manage.mapper import CarStatisticsMapper


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
