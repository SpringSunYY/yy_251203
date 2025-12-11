from typing import List, Optional

from pydantic import BaseModel, Field


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


class RelationStatisticsVo(BaseModel):
    """
    关系统计对象
      {
    "name": "企业岗位要求",
    "value": 0,
    "list": [
      {
        "name": "10000人以上", "value": 10,
        "list": [
    """
    name: str
    value: int
    tooltipText: Optional[str] = None
    children: List['RelationStatisticsVo'] = Field(default_factory=list)

    class Config:
        # 允许前向引用
        arbitrary_types_allowed = True
