import request from './request'

// 获取价格趋势
export const getPriceTrend = (params) => {
  return request({
    url: '/price/trend',
    method: 'get',
    params
  })
}

// 获取当前价格
export const getCurrentPrice = (params) => {
  return request({
    url: '/price/current',
    method: 'get',
    params
  })
}

// 获取价格对比
export const getPriceCompare = (params) => {
  return request({
    url: '/price/compare',
    method: 'get',
    params
  })
}

// 获取预警列表
export const getAlertList = (params) => {
  return request({
    url: '/alert/list',
    method: 'get',
    params
  })
}

// 处理预警
export const handleAlert = (alertId, data) => {
  return request({
    url: `/alert/${alertId}/handle`,
    method: 'put',
    data
  })
}

// 获取价格预测
export const getPrediction = (productId, params) => {
  return request({
    url: `/predict/${productId}`,
    method: 'get',
    params
  })
}

// 获取市场热力图数据
export const getMarketHeatmap = (params) => {
  return request({
    url: '/visualization/market/heatmap',
    method: 'get',
    params
  })
}

// 导出报表
export const exportReport = (params) => {
  return request({
    url: '/report/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}
