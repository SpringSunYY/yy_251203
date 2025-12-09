# -*- coding: utf-8 -*-
# @Module: manage
# @Author: YY

def init_app(app):
    """
    初始化模块，注册蓝图
    
    Args:
        app: Flask应用实例
    """
    # 导入 controller 模块，自动注册所有蓝图
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_manage.controller import car_info
    app.register_blueprint(car_info)