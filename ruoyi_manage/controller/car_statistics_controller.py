from ruoyi_common.base.model import AjaxResponse
from ruoyi_common.descriptor.serializer import JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_manage.domain.statistics.dto import CarStatisticsRequest
from ruoyi_manage.controller import car_statistics as car_statistics_bp
from ruoyi_manage.service.car_statistics_service import CarStatisticsService

gen = car_statistics_bp
"""汽车信息统计"""
car_statistics_service = CarStatisticsService()

"""汽车销量排行"""
@gen.route('/car/sales/rank', methods=['GET'])
@QueryValidator()
@PreAuthorize(HasPerm('manage:car:statistics'))
@JsonSerializer()
def get_car_sales_rank_statistics(request: CarStatisticsRequest):
    # 直接传递 request 参数，无需转换
    return AjaxResponse.from_success(data=car_statistics_service.get_car_sales_rank_statistics(request))


###汽车品牌统计
"""汽车品牌统计"""
@gen.route('/car/brand', methods=['GET'])
@QueryValidator()
@PreAuthorize(HasPerm('manage:car:statistics'))
@JsonSerializer()
def get_car_brand_statistics(request: CarStatisticsRequest):
    # 直接传递 request 参数，无需转换
    return AjaxResponse.from_success(data=car_statistics_service.get_car_brand_statistics(request))


"""汽车价格分析"""
@gen.route('/car/price', methods=['GET'])
@QueryValidator()
@PreAuthorize(HasPerm('manage:car:statistics'))
@JsonSerializer()
def get_car_price_statistics(request: CarStatisticsRequest):
    # 直接传递 request 参数，无需转换
    return AjaxResponse.from_success(data=car_statistics_service.get_car_price_statistics(request))
