from typing import List

from ruoyi_manage.domain.statistics.vo import StatisticsVo
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
