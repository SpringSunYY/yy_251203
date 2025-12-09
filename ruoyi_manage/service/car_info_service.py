# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: car_info_service.py
# @Time    : 2025-12-09 19:32:56

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils import DateUtil
from ruoyi_common.utils.base import LogUtil
from ruoyi_manage.domain.entity import CarInfo
from ruoyi_manage.mapper.car_info_mapper import CarInfoMapper

class CarInfoService:
    """汽车信息服务类"""

    def select_car_info_list(self, car: CarInfo) -> List[CarInfo]:
        """
        查询汽车信息列表

        Args:
            car (car_info): 汽车信息对象

        Returns:
            List[car_info]: 汽车信息列表
        """
        return CarInfoMapper.select_car_info_list(car)


    def select_car_info_by_id(self, car_id: int) -> CarInfo:
        """
        根据ID查询汽车信息

        Args:
            car_id (int): 编号

        Returns:
            car_info: 汽车信息对象
        """
        return CarInfoMapper.select_car_info_by_id(car_id)


    def insert_car_info(self, car: CarInfo) -> int:
        """
        新增汽车信息

        Args:
            car (car_info): 汽车信息对象

        Returns:
            int: 插入的记录数
        """
        return CarInfoMapper.insert_car_info(car)


    def update_car_info(self, car: CarInfo) -> int:
        """
        修改汽车信息

        Args:
            car (car_info): 汽车信息对象

        Returns:
            int: 更新的记录数
        """
        return CarInfoMapper.update_car_info(car)



    def delete_car_info_by_ids(self, ids: List[int]) -> int:
        """
        批量删除汽车信息

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return CarInfoMapper.delete_car_info_by_ids(ids)


    def import_car_info(self, car_list: List[CarInfo], is_update: bool = False) -> str:
        """
        导入汽车信息数据

        Args:
            car_list (List[car_info]): 汽车信息列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not car_list:
            raise ServiceException("导入汽车信息数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for car in car_list:
            try:
                display_value = car

                display_value = getattr(car, "car_id", display_value)
                # 格式化时间格式
                if car.market_time:
                    car.market_time = DateUtil.format_datetime(car.market_time)
                    print(car.market_time)
                existing = None
                if car.car_id is not None:
                    existing = CarInfoMapper.select_car_info_by_id(car.car_id)
                if existing:
                    if is_update:
                        result = CarInfoMapper.update_car_info(car)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = CarInfoMapper.insert_car_info(car)

                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入汽车信息失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg
