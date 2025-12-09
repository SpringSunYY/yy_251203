# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: car_info_mapper.py
# @Time    : 2025-12-09 19:32:56

from typing import List
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_manage.domain.entity import CarInfo
from ruoyi_manage.domain.po import CarInfoPo

class CarInfoMapper:
    """汽车信息Mapper"""

    @staticmethod
    def select_car_info_list(car: CarInfo) -> List[CarInfo]:
        """
        查询汽车信息列表

        Args:
            car (car_info): 汽车信息对象

        Returns:
            List[car_info]: 汽车信息列表
        """
        try:
            # 构建查询条件
            stmt = select(CarInfoPo)

            if car.car_id is not None:
                stmt = stmt.where(CarInfoPo.car_id == car.car_id)
            if car.brand_name:
                stmt = stmt.where(CarInfoPo.brand_name.like("%" + str(car.brand_name) + "%"))
            if car.series_name:
                stmt = stmt.where(CarInfoPo.series_name.like("%" + str(car.series_name) + "%"))
            if car.series_id is not None:
                stmt = stmt.where(CarInfoPo.series_id == car.series_id)
            if car.dealer_price is not None:
                stmt = stmt.where(CarInfoPo.dealer_price == car.dealer_price)
            if car.model_type is not None:
                stmt = stmt.where(CarInfoPo.model_type == car.model_type)
            if car.energy_type is not None:
                stmt = stmt.where(CarInfoPo.energy_type == car.energy_type)
            _params = getattr(car, "params", {}) or {}
            begin_val = _params.get("beginMarketTime")
            end_val = _params.get("endMarketTime")
            if begin_val is not None:
                stmt = stmt.where(CarInfoPo.market_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(CarInfoPo.market_time <= end_val)
            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt

            result = db.session.execute(stmt).scalars().all()
            # 调试日志：查看数据库层是否有数据
            print(f"[car_info_mapper] query result count: {len(result)}")
            if not result:
                return []
            validated = []
            for item in result:
                try:
                    validated.append(CarInfo.model_validate(item))
                except Exception as e:
                    # 记录触发校验失败的原始行，帮助定位字段格式问题
                    print(f"[car_info_mapper] model_validate failed: raw={item}, err={e}")
            return validated
        except Exception as e:
            print(f"查询汽车信息列表出错: {e}")
            return []


    @staticmethod
    def select_car_info_by_id(car_id: int) -> CarInfo:
        """
        根据ID查询汽车信息

        Args:
            car_id (int): 编号

        Returns:
            car_info: 汽车信息对象
        """
        try:
            result = db.session.get(CarInfoPo, car_id)
            return CarInfo.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询汽车信息出错: {e}")
            return None


    @staticmethod
    def insert_car_info(car: CarInfo) -> int:
        """
        新增汽车信息

        Args:
            car (car_info): 汽车信息对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = CarInfoPo()
            new_po.car_id = car.car_id
            new_po.brand_name = car.brand_name
            new_po.image = car.image
            new_po.series_name = car.series_name
            new_po.series_id = car.series_id
            new_po.dealer_price = car.dealer_price
            new_po.max_price = car.max_price
            new_po.min_price = car.min_price
            new_po.sales_count = car.sales_count
            new_po.model_type = car.model_type
            new_po.energy_type = car.energy_type
            new_po.market_time = car.market_time
            new_po.overall = car.overall
            new_po.exterior = car.exterior
            new_po.interior = car.interior
            new_po.space = car.space
            new_po.handling = car.handling
            new_po.comfort = car.comfort
            new_po.power = car.power
            new_po.configuration = car.configuration
            db.session.add(new_po)
            db.session.commit()
            car.car_id = new_po.car_id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增汽车信息出错: {e}")
            return 0


    @staticmethod
    def update_car_info(car: CarInfo) -> int:
        """
        修改汽车信息

        Args:
            car (car_info): 汽车信息对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(CarInfoPo, car.car_id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.brand_name = car.brand_name
            existing.image = car.image
            existing.series_name = car.series_name
            existing.series_id = car.series_id
            existing.dealer_price = car.dealer_price
            existing.max_price = car.max_price
            existing.min_price = car.min_price
            existing.sales_count = car.sales_count
            existing.model_type = car.model_type
            existing.energy_type = car.energy_type
            existing.market_time = car.market_time
            existing.overall = car.overall
            existing.exterior = car.exterior
            existing.interior = car.interior
            existing.space = car.space
            existing.handling = car.handling
            existing.comfort = car.comfort
            existing.power = car.power
            existing.configuration = car.configuration
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改汽车信息出错: {e}")
            return 0

    @staticmethod
    def delete_car_info_by_ids(ids: List[int]) -> int:
        """
        批量删除汽车信息

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(CarInfoPo).where(CarInfoPo.car_id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除汽车信息出错: {e}")
            return 0
