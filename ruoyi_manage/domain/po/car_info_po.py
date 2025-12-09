# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: car_info_po.py
# @Time    : 2025-12-09 19:32:56

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from ruoyi_admin.ext import db

class CarInfoPo(db.Model):
    """
    汽车信息表PO对象
    """
    __tablename__ = 'tb_car_info'
    __table_args__ = {'comment': '汽车信息表'}
    car_id: Mapped[int] = mapped_column(
        'car_id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='编号'
    )
    brand_name: Mapped[Optional[str]] = mapped_column(
        'brand_name',
        String(255),
        nullable=True,
        comment='品牌名'
    )
    image: Mapped[Optional[str]] = mapped_column(
        'image',
        String(255),
        nullable=True,
        comment='封面'
    )
    series_name: Mapped[Optional[str]] = mapped_column(
        'series_name',
        String(255),
        nullable=True,
        comment='系列名称'
    )
    series_id: Mapped[Optional[str]] = mapped_column(
        'series_id',
        String(255),
        nullable=True,
        comment='车系ID'
    )
    dealer_price: Mapped[Optional[str]] = mapped_column(
        'dealer_price',
        String(255),
        nullable=True,
        comment='价格'
    )
    max_price: Mapped[Optional[str]] = mapped_column(
        'max_price',
        Numeric(10, 0),
        nullable=True,
        comment='最大价格'
    )
    min_price: Mapped[Optional[str]] = mapped_column(
        'min_price',
        Numeric(10, 0),
        nullable=True,
        comment='最低价格'
    )
    sales_count: Mapped[Optional[int]] = mapped_column(
        'sales_count',
        Integer,
        nullable=True,
        comment='销量'
    )
    model_type: Mapped[Optional[str]] = mapped_column(
        'model_type',
        String(255),
        nullable=True,
        comment='车型'
    )
    energy_type: Mapped[Optional[str]] = mapped_column(
        'energy_type',
        String(255),
        nullable=True,
        comment='能源类型'
    )
    market_time: Mapped[Optional[datetime]] = mapped_column(
        'market_time',
        DateTime,
        nullable=True,
        comment='上市时间'
    )
    overall: Mapped[Optional[str]] = mapped_column(
        'overall',
        Numeric(10, 0),
        nullable=True,
        comment='综合评分'
    )
    exterior: Mapped[Optional[str]] = mapped_column(
        'exterior',
        Numeric(10, 0),
        nullable=True,
        comment='外观评分'
    )
    interior: Mapped[Optional[str]] = mapped_column(
        'interior',
        Numeric(10, 0),
        nullable=True,
        comment='内饰评分'
    )
    space: Mapped[Optional[str]] = mapped_column(
        'space',
        Numeric(10, 0),
        nullable=True,
        comment='空间评分'
    )
    handling: Mapped[Optional[str]] = mapped_column(
        'handling',
        Numeric(10, 0),
        nullable=True,
        comment='操控评分'
    )
    comfort: Mapped[Optional[str]] = mapped_column(
        'comfort',
        Numeric(10, 0),
        nullable=True,
        comment='舒适性评分'
    )
    power: Mapped[Optional[str]] = mapped_column(
        'power',
        Numeric(10, 0),
        nullable=True,
        comment='动力评分'
    )
    configuration: Mapped[Optional[str]] = mapped_column(
        'configuration',
        Numeric(10, 0),
        nullable=True,
        comment='配置评分'
    )