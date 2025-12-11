# -*- coding: utf-8 -*-
# @Module: ruoyi_manage/controller

from flask import Blueprint

car_info = Blueprint('car_info', __name__, url_prefix='/manage/car')
car_statistics = Blueprint('car_statistics', __name__, url_prefix='/manage/statistics')


from . import car_info_controller, car_statistics_controller