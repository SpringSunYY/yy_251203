import requests
from bs4 import BeautifulSoup

# --- 全局配置与常量 ---
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
TIMEOUT = 10
DEFAULT_VALUE = ""
MAX_PAGES = 5
NEW_ENERGY_TYPE = [1, 2, 3, 4]
# 定义中文到英文的映射 (懂车分维度，保持不变)
SCORE_DIMENSION_MAP = {
    "综合": "overall",
    "外观": "exterior",
    "内饰": "interior",
    "空间": "space",
    "操控": "handling",
    "舒适性": "comfort",
    "动力": "power",
    "配置": "configuration"
}

# EXCEL_HEADERS
EXCEL_HEADERS = (
    "品牌名", "封面", "系列名称", "车系ID", "价格", "最大价格", "最低价格", "销量", "车型", "能源类型", "上市时间",
    "综合评分", "外观评分", "内饰评分", "空间评分", "操控评分", "舒适性评分", "动力评分", "配置评分",
)


class CarReptileUtil:
    """爬取懂车帝榜单数据的工具类，供外部调用。"""

    header = header
    timeout = TIMEOUT
    default_value = DEFAULT_VALUE
    score_dimension_map = SCORE_DIMENSION_MAP
    excel_headers = EXCEL_HEADERS

    @staticmethod
    def fetch_url(url, is_json=False):
        """封装 API 请求逻辑，处理异常并返回响应或数据，并打印请求 URL"""
        print(f"   [API Request] URL: {url}")
        try:
            response = requests.get(url=url, headers=CarReptileUtil.header, timeout=CarReptileUtil.timeout)
            response.raise_for_status()
            if is_json:
                return response.json()
            return response.text
        except requests.RequestException as e:
            print(f"请求失败，终止爬取：{url} | 错误: {e}")
            return None
        except Exception as e:
            print(f"发生未知错误：{url} | 错误: {e}")
            return None

    @staticmethod
    def safe_find_text(soup, anchor_name):
        """根据 data-row-anchor 查找元素并安全地提取文本 (用于车系参数页)"""
        try:
            element = soup.find("div", attrs={"data-row-anchor": anchor_name})
            if element:
                cell = element.select_one(".cell_normal__37nRi")
                if cell:
                    return cell.text.strip()
            return CarReptileUtil.default_value
        except Exception:
            return CarReptileUtil.default_value

    @classmethod
    def get_dcar_score_by_series_id(cls, series_id):
        """爬取懂车分，并使用对应的英文键名返回数据。"""
        score_result = {v: cls.default_value for v in cls.score_dimension_map.values()}
        score_api_url = f"https://www.dongchedi.com/auto/series/score/{series_id}-x-x-x-x-x-x"
        html_content = cls.fetch_url(score_api_url, is_json=False)
        if not html_content:
            return score_result
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            score_container = soup.find("div", class_="style_scoreContentRight__3F_2e")
            if not score_container:
                return score_result
            score_uls = score_container.find_all("ul", class_=lambda c: c and 'style_clearBorder' in c)
            for ul in score_uls:
                name_tag = ul.find("li", class_="tw-whitespace-nowrap")
                if not name_tag:
                    continue
                dim_name_cn = name_tag.text.strip()
                dim_name_en = cls.score_dimension_map.get(dim_name_cn)
                if dim_name_en:
                    score_tag = ul.find_all("li", class_=lambda c: c and 'tw-text-white' in c)
                    if score_tag and len(score_tag) >= 1:
                        score_value = score_tag[0].text.strip()
                        score_result[dim_name_en] = score_value
            return score_result
        except Exception:
            return score_result

    @classmethod
    def _send_http(cls, url, collector):
        """爬取一页数据，如果无数据返回 False 停止后续爬取。"""
        http_data = cls.fetch_url(url, is_json=True)
        if not http_data:
            return False
        cars = http_data.get("data", {}).get("list")
        if not cars:
            print("检测到当前页无数据，停止后续爬取。")
            return False
        for car in cars:
            series_name = car.get("series_name", cls.default_value)
            dealer_price = car.get("dealer_price", cls.default_value)
            max_price = car.get("max_price", cls.default_value)
            min_price = car.get("min_price", cls.default_value)
            sales_count = car.get("count", cls.default_value)
            brand_name = car.get("brand_name", cls.default_value)
            series_id = car.get("series_id", cls.default_value)
            image_url = car.get("image", cls.default_value)
            if series_id == cls.default_value:
                print(f"跳过 {series_name}：缺少 series_id。")
                continue
            second_http_url = f"https://www.dongchedi.com/auto/params-carIds-x-{series_id}"
            model_type, energy_type, market_time = cls.default_value, cls.default_value, cls.default_value
            html_content_2 = cls.fetch_url(second_http_url, is_json=False)
            if html_content_2:
                try:
                    soup = BeautifulSoup(html_content_2, 'lxml')
                    model_type = cls.safe_find_text(soup, "jb")
                    energy_type = cls.safe_find_text(soup, "fuel_form")
                    market_time = cls.safe_find_text(soup, "market_time")
                except Exception:
                    pass
            score_data = cls.get_dcar_score_by_series_id(series_id)
            print(
                f"   - 采集成功：【{series_name}】ID:{series_id} | "
                f"品牌:{brand_name} | 价格:{dealer_price} | 销量:{sales_count} | "
                f"车型:{model_type} | 能源:{energy_type} | 上市:{market_time} | "
                f"综合分:{score_data.get('overall', cls.default_value)}"
            )
            data_row = (
                brand_name,
                image_url,
                series_name,
                series_id,
                dealer_price,
                max_price,
                min_price,
                sales_count,
                model_type,
                energy_type,
                market_time,
                score_data.get('overall', cls.default_value),
                score_data.get('exterior', cls.default_value),
                score_data.get('interior', cls.default_value),
                score_data.get('space', cls.default_value),
                score_data.get('handling', cls.default_value),
                score_data.get('comfort', cls.default_value),
                score_data.get('power', cls.default_value),
                score_data.get('configuration', cls.default_value),
            )
            collector.append(data_row)
        return True

    @classmethod
    def _query_by_new_energy_type(cls, new_energy_type, max_pages, collector):
        for i in range(max_pages):
            url = (
                f"https://www.dongchedi.com/motor/pc/car/rank_data?aid=1839&app_name=auto_web_pc&count=10&offset={i * 10}&new_energy_type={new_energy_type}&"
                f"rank_data_type=11&brand_id=&price=&manufacturer=&outter_detail_type=&nation=0"
            )
            print(f"\n---type:{new_energy_type}, 正在爬取第 {i + 1} 页 (Offset: {i * 10}) ---")
            if not cls._send_http(url, collector):
                break

    @classmethod
    def crawl(cls, max_pages=MAX_PAGES, types=None):
        """
        对外暴露的入口：
        - max_pages: int，每个能源类型要爬取的页数
        - new_energy_type: int 或 list，懂车帝的能源类型编码
        返回：all_car_data 列表，顺序与 excel_headers 对应
        """
        if types is None:
            types = NEW_ENERGY_TYPE
        collector = []
        if isinstance(types, int):
            types = [types]
        for t in types:
            cls._query_by_new_energy_type(t, max_pages, collector)
        return collector
