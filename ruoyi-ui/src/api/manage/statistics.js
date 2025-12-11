import request from '@/utils/request'

//汽车销量排行
export function carSalesRankStatistics(query) {
  return request({
    url: '/manage/statistics/car/sales/rank',
    method: 'get',
    params: query
  })
}


//获取汽车品牌统计 /car/brand
export function carBrandStatistics(query) {
  return request({
    url: '/manage/statistics/car/brand',
    method: 'get',
    params: query
  })
}

//汽车价格统计/car/price
export function carPriceStatistics(query) {
  return request({
    url: '/manage/statistics/car/price',
    method: 'get',
    params: query
  })
}
