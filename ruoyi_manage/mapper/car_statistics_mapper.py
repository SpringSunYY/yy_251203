from typing import List

from sqlalchemy import select, func

from ruoyi_admin.ext import db
from ruoyi_manage.domain.entity import CarInfo
from ruoyi_manage.domain.po import CarInfoPo
from ruoyi_manage.domain.statistics.dto import CarStatisticsRequest
from ruoyi_manage.domain.statistics.po import StatisticsPo


class CarStatisticsMapper:
    """汽车统计Mapper"""

    """获取汽车销售数据排行"""

    @staticmethod
    def get_car_sales_rank_statistics(request: CarStatisticsRequest) -> List[StatisticsPo]:
        """
        获取汽车销售数据排行

        Args:
            request: 请求参数

        Returns:
            List[CarInfo]: 汽车信息列表
            select sum(sales_count) as value, series_name as name
            from tb_car_info
            group by name
            order by value desc
        """
        try:
            stmt = select(
                func.sum(CarInfoPo.sales_count).label("value"),
                CarInfoPo.series_name.label("name")
            ).select_from(CarInfoPo).group_by(CarInfoPo.series_name).order_by(db.desc("value"))
            # 创建查询条件
            if request.brand_name:
                stmt = stmt.where(CarInfoPo.brand_name.like("%" + str(request.brand_name) + "%"))
            if request.series_name:
                stmt = stmt.where(CarInfoPo.series_name.like("%" + str(request.series_name) + "%"))
            if request.model_type:
                stmt = stmt.where(CarInfoPo.model_type == request.model_type)
            if request.energy_type:
                stmt = stmt.where(CarInfoPo.energy_type == request.energy_type)
            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            return [StatisticsPo(value=item.value, name=item.name) for item in result]
        except Exception as e:
            print(f"获取汽车销售数据排行出错: {e}")
            return []
