from typing import List

from pydantic import BaseModel


class StatisticsVo(BaseModel):
    """
    统计总数对象
    """
    value: int
    name: str


class PieBarStatisticsVo(BaseModel):
    """
    饼状图统计对象
    """
    name: str
    tooltipText: str
    values: List[StatisticsVo]


class BatchLineItem(BaseModel):
    """
    批量折线图统计对象
    """
    name: str
    values: List[int]

class BatchLineStatisticsVo(BaseModel):
    """
    批量折线图统计对象
    """
    names: List[str]
    values: List[BatchLineItem]
    class Config:
        # 允许前向引用
        arbitrary_types_allowed = True
