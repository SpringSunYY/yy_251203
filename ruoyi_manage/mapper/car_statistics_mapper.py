from typing import List

from sqlalchemy import select, func

from ruoyi_admin.ext import db
from ruoyi_manage.domain.entity import CarInfo
from ruoyi_manage.domain.po import CarInfoPo
from ruoyi_manage.domain.statistics.dto import CarStatisticsRequest
from ruoyi_manage.domain.statistics.po import StatisticsPo
from ruoyi_manage.domain.statistics.vo import StatisticsVo


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
            stmt = CarStatisticsMapper.builder_query_params(request, stmt)
            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            return [StatisticsPo(value=item.value, name=item.name) for item in result]
        except Exception as e:
            print(f"获取汽车销售数据排行出错: {e}")
            return []

    @staticmethod
    def builder_query_params(request, stmt):
        # 创建查询条件
        if request.brand_name:
            stmt = stmt.where(CarInfoPo.brand_name == request.brand_name)
        if request.series_name:
            stmt = stmt.where(CarInfoPo.series_name == request.series_name)
        if request.model_type:
            stmt = stmt.where(CarInfoPo.model_type == request.model_type)
        if request.energy_type:
            stmt = stmt.where(CarInfoPo.energy_type == request.energy_type)
        return stmt

    @staticmethod
    def get_car_brand_statistics(request, limit=10) -> List[StatisticsPo]:
        """
        获取汽车品牌统计
        select sum(sales_count) as value, brand_name as name
        from tb_car_info
        group by name
        order by value desc
        limit 10;
        """
        try:
            stmt = select(
                func.sum(CarInfoPo.sales_count).label("value"),
                CarInfoPo.brand_name.label("name")
            ).select_from(CarInfoPo).group_by(CarInfoPo.brand_name).order_by(db.desc("value")).limit(limit)
            # 创建查询条件
            stmt = CarStatisticsMapper.builder_query_params(request, stmt)
            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            return [StatisticsVo(value=item.value, name=item.name) for item in result]
        except Exception as e:
            print(f"获取汽车品牌统计出错: {e}")
            return []

    @staticmethod
    def get_car_score_statistics(request, score="overall") -> List[StatisticsPo]:
        """查询评分
              select sum(sales_count) as value, tb_car_info.overall as name
                from tb_car_info where overall is not null
                group by name
                order by name asc;
        """
        try:
            # 支持的评分字段列表
            valid_score_fields = [
                "overall",  # 综合评分
                "exterior",  # 外观评分
                "interior",  # 内饰评分
                "space",  # 空间评分
                "handling",  # 操控评分
                "comfort",  # 舒适性评分
                "power",  # 动力评分
                "configuration"  # 配置评分
            ]

            # 如果传入的score不在有效字段列表中，默认使用overall
            if score not in valid_score_fields:
                score = "overall"

            # 根据传入的score参数选择对应的列
            score_column = getattr(CarInfoPo, score)

            stmt = select(
                func.sum(CarInfoPo.sales_count).label("value"),
                score_column.label("name")
            ).select_from(CarInfoPo).where(score_column.is_not(None)).group_by(score_column).order_by(db.asc("name"))

            # 创建查询条件
            stmt = CarStatisticsMapper.builder_query_params(request, stmt)

            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            # name 可能是 Decimal，转为字符串以匹配 StatisticsPo 的类型定义
            return [StatisticsPo(value=item.value, name=str(item.name)) for item in result]
        except Exception as e:
            print(f"获取汽车评分统计出错: {e}")
            return []

    @staticmethod
    def get_car_model_type_statistics(request):
        """
        获取汽车车型统计
        select sum(sales_count) as value, model_type as name
        from tb_car_info where model_type is not null
        group by name
        order by value desc
        """
        try:
            stmt = (select(
                func.sum(CarInfoPo.sales_count).label("value"),
                CarInfoPo.model_type.label("name")
            ).select_from(CarInfoPo)
                    .where(CarInfoPo.model_type.is_not(None))
                    .group_by(CarInfoPo.model_type)
                    .order_by(db.desc("value")))
            # 创建查询条件
            stmt = CarStatisticsMapper.builder_query_params(request, stmt)
            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            return [StatisticsPo(value=item.value, name=item.name) for item in result]
        except Exception as e:
            print(f"获取汽车车型统计出错: {e}")
            return []
