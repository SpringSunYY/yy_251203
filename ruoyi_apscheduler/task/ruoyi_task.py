# -*- coding: utf-8 -*-
# @Author  : YY
from flask import current_app, has_app_context
from ruoyi_manage.service import CarInfoService
from ruoyi_admin.app import create_app

# 延迟创建 Flask 应用，避免模块导入阶段出错
_app = None
car_info_service = CarInfoService()


def get_app():
    global _app
    # 如果当前已有 Flask 应用上下文，优先复用
    if has_app_context():
        try:
            return current_app._get_current_object()
        except Exception:
            pass
    if _app is None:
        _app = create_app()
    return _app
def multiply_args(x, y):
    print("多参方法： x: {} y: {}".format(x, y))


def one_args(x):
    print("单个参方法： x: {} ".format(x))


def no_args():
    print("无参方法")


def auto_reptile_car_info():
    print("爬虫开始执行...")
    # 确保在应用上下文中执行数据库操作
    app = get_app()
    with app.app_context():
        car_info_service.auto_reptile_car_info(5000, [1, 2, 3, 4], True)
