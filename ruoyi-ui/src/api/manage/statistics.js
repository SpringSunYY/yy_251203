import request from '@/utils/request'

//汽车销量排行
export function carSalesRank(query) {
  return request({
    url: '/manage/statistics/car/sales/rank',
    method: 'get',
    params: query
  })
}
