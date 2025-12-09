# -*- coding: utf-8 -*-
# @Module: ruoyi_manage/controller

from flask import Blueprint

car_info = Blueprint('car_info', __name__, url_prefix='/manage/car')


from . import car_info_controller
