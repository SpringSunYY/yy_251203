
from typing import List

from flask import g
from flask_login import login_required
from pydantic import BeforeValidator
from typing_extensions import Annotated
from werkzeug.datastructures import FileStorage

from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.constant import HttpStatus
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, BodyValidator, PathValidator, FileDownloadValidator, FileUploadValidator
from ruoyi_common.domain.enum import BusinessType
from ruoyi_common.utils.base import ExcelUtil
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_manage.controller import car_info as car_info_bp
from ruoyi_manage.domain.entity import CarInfo
from ruoyi_manage.service.car_info_service import CarInfoService

# 使用 controller/__init__.py 中定义的蓝图
gen = car_info_bp

car_info_service = CarInfoService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None

@gen.route('/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('manage:car:list'))
@JsonSerializer()
def car_list(dto: CarInfo):
    """查询汽车信息列表"""
    car_info_entity = CarInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(car_info_entity, attr):
            setattr(car_info_entity, attr, getattr(dto, attr))
    cars = car_info_service.select_car_info_list(car_info_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=cars)


@gen.route('/<int:carId>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('manage:car:query'))
@JsonSerializer()
def get_car(car_id: int):
    """获取汽车信息详细信息"""
    car_info_entity = car_info_service.select_car_info_by_id(car_id)
    return AjaxResponse.from_success(data=car_info_entity)


@gen.route('', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('manage:car:add'))
@Log(title='汽车信息管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_car(dto: CarInfo):
    """新增汽车信息"""
    car_info_entity = CarInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(car_info_entity, attr):
            setattr(car_info_entity, attr, getattr(dto, attr))
    result = car_info_service.insert_car_info(car_info_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='新增失败')


@gen.route('', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('manage:car:edit'))
@Log(title='汽车信息管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_car(dto: CarInfo):
    """修改汽车信息"""
    car_info_entity = CarInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(car_info_entity, attr):
            setattr(car_info_entity, attr, getattr(dto, attr))
    result = car_info_service.update_car_info(car_info_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='修改失败')



@gen.route('/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('manage:car:remove'))
@Log(title='汽车信息管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_car(ids: str):
    """删除汽车信息"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = car_info_service.delete_car_info_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@gen.route('/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('manage:car:export'))
@Log(title='汽车信息管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_car(dto: CarInfo):
    """导出汽车信息列表"""
    car_info_entity = CarInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(car_info_entity, attr):
            setattr(car_info_entity, attr, getattr(dto, attr))
    _clear_page_context()
    car_info_entity.page_num = None
    car_info_entity.page_size = None
    cars = car_info_service.select_car_info_list(car_info_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(CarInfo)
    return excel_util.export_response(cars, "汽车信息数据")

@gen.route('/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def import_template():
    """下载汽车信息导入模板"""
    excel_util = ExcelUtil(CarInfo)
    return excel_util.import_template_response(sheetname="汽车信息数据")

@gen.route('/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('manage:car:import'))
@Log(title='汽车信息管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入汽车信息数据"""
    file = file[0]
    excel_util = ExcelUtil(CarInfo)
    car_list = excel_util.import_file(file, sheetname="汽车信息数据")
    msg = car_info_service.import_car_info(car_list, update_support)
    return AjaxResponse.from_success(msg=msg)