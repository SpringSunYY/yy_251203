from typing import Optional, Annotated

from pydantic import Field

from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class CarStatisticsRequest(BaseEntity):
    # 品牌名
    brand_name: Annotated[
        Optional[str],
        Field(default=None, description="品牌名"),
        VoField(query=True),
        ExcelField(name="品牌名")
    ]
    # 系列名称
    series_name: Annotated[
        Optional[str],
        Field(default=None, description="系列名称"),
        VoField(query=True),
        ExcelField(name="系列名称")
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
