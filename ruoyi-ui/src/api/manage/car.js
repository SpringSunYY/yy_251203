import request from '@/utils/request'

// 查询汽车信息列表
export function listCar(query) {
  return request({
    url: '/manage/car/list',
    method: 'get',
    params: query
  })
}

// 查询汽车信息详细
export function getCar(carId) {
  return request({
    url: '/manage/car/' +carId,
    method: 'get'
  })
}

// 新增汽车信息
export function addCar(data) {
  return request({
    url: '/manage/car',
    method: 'post',
    data: data
  })
}

// 修改汽车信息
export function updateCar(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/manage/car',
    method: 'put',
    data: data
  })
}

// 删除汽车信息
export function delCar(carId) {
  return request({
    url: '/manage/car/' +carId,
    method: 'delete'
  })
}
