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


//汽车评分统计/car/score
export function carScoreStatistics(query) {
  return request({
    url: '/manage/statistics/car/score',
    method: 'get',
    params: query
  })
}

//汽车车型分析
export function carModelTypeStatistics(query) {
  return request({
    url: '/manage/statistics/car/model/type',
    method: 'get',
    params: query
  })
}

//汽车关系
export function carRelationStatistics(query) {
  return request({
    url: '/manage/statistics/car/relation',
    method: 'get',
    params: query
  })
}

//汽车各种总数
export function carCountStatistics(query) {
  return request({
    url: '/manage/statistics/car/count',
    method: 'get',
    params: query
  })
}
