# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: car_info.py
# @Time    : 2025-12-09 19:32:56

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int, str_to_float
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class CarInfo(BaseEntity):
    """
    汽车信息表对象
    """
    # 编号
    car_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="编号"),
        VoField(query=True),
        ExcelField(name="编号")
    ]
    # 品牌名
    brand_name: Annotated[
        Optional[str],
        Field(default=None, description="品牌名"),
        VoField(query=True),
        ExcelField(name="品牌名")
    ]
    # 封面
    image: Annotated[
        Optional[str],
        Field(default=None, description="封面"),
        ExcelField(name="封面")
    ]
    # 系列名称
    series_name: Annotated[
        Optional[str],
        Field(default=None, description="系列名称"),
        VoField(query=True),
        ExcelField(name="系列名称")
    ]
    # 车系ID
    series_id: Annotated[
        Optional[str],
        Field(default=None, description="车系ID"),
        VoField(query=True),
        ExcelField(name="车系ID")
    ]
    # 价格
    dealer_price: Annotated[
        Optional[str],
        Field(default=None, description="价格"),
        VoField(query=True),
        ExcelField(name="价格")
    ]
    # 最大价格
    max_price: Annotated[
        Optional[float],
        Field(default=None, description="最大价格"),
        ExcelField(name="最大价格")
    ]
    # 最低价格
    min_price: Annotated[
        Optional[float],
        Field(default=None, description="最低价格"),
        ExcelField(name="最低价格")
    ]
    # 销量
    sales_count: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="销量"),
        ExcelField(name="销量")
    ]
    # 车型
    model_type: Annotated[
        Optional[str],
        Field(default=None, description="车型"),
        VoField(query=True),
        ExcelField(name="车型", dict_type="manage_model_type")
    ]
    # 能源类型
    energy_type: Annotated[
        Optional[str],
        Field(default=None, description="能源类型"),
        VoField(query=True),
        ExcelField(name="能源类型", dict_type="manage_energy_type")
    ]
    # 上市时间
    market_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="上市时间"),
        VoField(query=True),
        ExcelField(name="上市时间")
    ]
    # 综合评分
    overall: Annotated[
        Optional[float],
        BeforeValidator(str_to_float),
        Field(default=None, description="综合评分"),
        ExcelField(name="综合评分")
    ]
    # 外观评分
    exterior: Annotated[
        Optional[float],
        BeforeValidator(str_to_float),
        Field(default=None, description="外观评分"),
        ExcelField(name="外观评分")
    ]
    # 内饰评分
    interior: Annotated[
        Optional[float],
        BeforeValidator(str_to_float),
        Field(default=None, description="内饰评分"),
        ExcelField(name="内饰评分")
    ]
    # 空间评分
    space: Annotated[
        Optional[float],
        BeforeValidator(str_to_float),
        Field(default=None, description="空间评分"),
        ExcelField(name="空间评分")
    ]
    # 操控评分
    handling: Annotated[
        Optional[float],
        BeforeValidator(str_to_float),
        Field(default=None, description="操控评分"),
        ExcelField(name="操控评分")
    ]
    # 舒适性评分
    comfort: Annotated[
        Optional[float],
        BeforeValidator(str_to_float),
        Field(default=None, description="舒适性评分"),
        ExcelField(name="舒适性评分")
    ]
    # 动力评分
    power: Annotated[
        Optional[float],
        BeforeValidator(str_to_float),
        Field(default=None, description="动力评分"),
        ExcelField(name="动力评分")
    ]
    # 配置评分
    configuration: Annotated[
        Optional[float],
        BeforeValidator(str_to_float),
        Field(default=None, description="配置评分"),
        ExcelField(name="配置评分")
    ]

    params: Optional[dict] = Field(default=None, description="参数")
    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")
