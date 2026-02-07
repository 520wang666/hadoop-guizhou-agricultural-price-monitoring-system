# API接口设计文档

## 1. 接口设计规范

### 1.1 RESTful API设计原则
- 使用HTTP动词表示操作类型（GET、POST、PUT、DELETE）
- 使用名词表示资源
- 使用HTTP状态码表示响应状态
- 统一的响应格式

### 1.2 基础URL
```
开发环境：http://localhost:8080/api/v1
生产环境：https://api.example.com/api/v1
```

### 1.3 统一响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2026-02-07T08:00:00Z"
}
```

### 1.4 状态码定义

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 2. 认证授权接口

### 2.1 用户登录

**接口地址：** `POST /auth/login`

**请求参数：**
```json
{
  "username": "admin",
  "password": "123456"
}
```

**响应数据：**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userInfo": {
      "userId": "1001",
      "username": "admin",
      "realName": "管理员",
      "role": "ADMIN"
    }
  }
}
```

### 2.2 用户登出

**接口地址：** `POST /auth/logout`

**请求头：**
```
Authorization: Bearer {token}
```

**响应数据：**
```json
{
  "code": 200,
  "message": "登出成功"
}
```

---

## 3. 价格查询接口

### 3.1 获取价格趋势

**接口地址：** `GET /price/trend`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| productId | String | 是 | 产品ID |
| regionId | String | 否 | 地区ID |
| startDate | String | 否 | 开始日期（YYYY-MM-DD） |
| endDate | String | 否 | 结束日期（YYYY-MM-DD） |
| period | String | 否 | 周期（day/week/month） |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "productId": "P001",
    "productName": "白菜",
    "regionId": "R001",
    "regionName": "贵阳市",
    "trendList": [
      {
        "date": "2026-01-01",
        "avgPrice": 2.50,
        "wholesalePrice": 2.30,
        "retailPrice": 2.80,
        "tradeVolume": 15000.00
      },
      {
        "date": "2026-01-02",
        "avgPrice": 2.55,
        "wholesalePrice": 2.35,
        "retailPrice": 2.85,
        "tradeVolume": 14500.00
      }
    ],
    "statistics": {
      "maxPrice": 3.20,
      "minPrice": 2.30,
      "avgPrice": 2.65,
      "priceChangeRate": 8.50
    }
  }
}
```

### 3.2 获取当前价格

**接口地址：** `GET /price/current`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| productId | String | 否 | 产品ID |
| regionId | String | 否 | 地区ID |
| marketId | String | 否 | 市场ID |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "productId": "P001",
      "productName": "白菜",
      "regionId": "R001",
      "regionName": "贵阳市",
      "marketId": "M001",
      "marketName": "贵阳农产品批发市场",
      "currentPrice": 2.55,
      "wholesalePrice": 2.35,
      "retailPrice": 2.85,
      "updateTime": "2026-02-07T08:00:00Z"
    }
  ]
}
```

### 3.3 获取价格对比

**接口地址：** `GET /price/compare`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| productId | String | 是 | 产品ID |
| regionIds | String | 是 | 地区ID列表（逗号分隔） |
| date | String | 否 | 对比日期（YYYY-MM-DD） |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "productId": "P001",
    "productName": "白菜",
    "compareDate": "2026-02-07",
    "regionList": [
      {
        "regionId": "R001",
        "regionName": "贵阳市",
        "price": 2.55,
        "nationalAvg": 2.45,
        "diff": 0.10,
        "diffRate": 4.08,
        "rank": 5
      },
      {
        "regionId": "R002",
        "regionName": "遵义市",
        "price": 2.35,
        "nationalAvg": 2.45,
        "diff": -0.10,
        "diffRate": -4.08,
        "rank": 8
      }
    ]
  }
}
```

---

## 4. 产品管理接口

### 4.1 获取产品列表

**接口地址：** `GET /product/list`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| categoryId | String | 否 | 分类ID |
| keyword | String | 否 | 关键词搜索 |
| pageNum | Integer | 否 | 页码（默认1） |
| pageSize | Integer | 否 | 每页数量（默认20） |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "pageNum": 1,
    "pageSize": 20,
    "list": [
      {
        "productId": "P001",
        "productName": "白菜",
        "categoryId": "C001",
        "categoryName": "蔬菜",
        "spec": "一级",
        "unit": "千克",
        "isActive": true
      }
    ]
  }
}
```

### 4.2 获取产品详情

**接口地址：** `GET /product/{productId}`

**路径参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| productId | String | 是 | 产品ID |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "productId": "P001",
    "productName": "白菜",
    "categoryId": "C001",
    "categoryName": "蔬菜",
    "spec": "一级",
    "unit": "千克",
    "description": "新鲜白菜",
    "isActive": true,
    "createTime": "2026-01-01T00:00:00Z",
    "updateTime": "2026-02-07T00:00:00Z"
  }
}
```

### 4.3 获取产品分类

**接口地址：** `GET /product/category`

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "categoryId": "C001",
      "categoryName": "蔬菜",
      "parentId": null,
      "children": [
        {
          "categoryId": "C00101",
          "categoryName": "叶菜类",
          "parentId": "C001"
        }
      ]
    },
    {
      "categoryId": "C002",
      "categoryName": "水果",
      "parentId": null
    }
  ]
}
```

---

## 5. 市场管理接口

### 5.1 获取市场列表

**接口地址：** `GET /market/list`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| regionId | String | 否 | 地区ID |
| marketType | String | 否 | 市场类型（wholesale/retail） |
| keyword | String | 否 | 关键词搜索 |
| pageNum | Integer | 否 | 页码（默认1） |
| pageSize | Integer | 否 | 每页数量（默认20） |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 50,
    "pageNum": 1,
    "pageSize": 20,
    "list": [
      {
        "marketId": "M001",
        "marketName": "贵阳农产品批发市场",
        "marketType": "wholesale",
        "regionId": "R001",
        "regionName": "贵阳市",
        "address": "贵阳市云岩区",
        "latitude": 26.6470,
        "longitude": 106.6301,
        "isActive": true
      }
    ]
  }
}
```

### 5.2 获取市场详情

**接口地址：** `GET /market/{marketId}`

**路径参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| marketId | String | 是 | 市场ID |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "marketId": "M001",
    "marketName": "贵阳农产品批发市场",
    "marketType": "wholesale",
    "regionId": "R001",
    "regionName": "贵阳市",
    "address": "贵阳市云岩区",
    "latitude": 26.6470,
    "longitude": 106.6301,
    "contact": "0851-12345678",
    "isActive": true,
    "createTime": "2026-01-01T00:00:00Z",
    "updateTime": "2026-02-07T00:00:00Z"
  }
}
```

---

## 6. 地区管理接口

### 6.1 获取地区列表

**接口地址：** `GET /region/list`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| parentId | String | 否 | 上级地区ID |
| level | Integer | 否 | 行政级别（1省/2市/3区县） |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "regionId": "R001",
      "regionName": "贵阳市",
      "province": "贵州省",
      "city": "贵阳市",
      "district": null,
      "level": 2,
      "parentId": "R000",
      "children": [
        {
          "regionId": "R00101",
          "regionName": "云岩区",
          "province": "贵州省",
          "city": "贵阳市",
          "district": "云岩区",
          "level": 3,
          "parentId": "R001"
        }
      ]
    }
  ]
}
```

---

## 7. 预警管理接口

### 7.1 获取预警列表

**接口地址：** `GET /alert/list`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| productId | String | 否 | 产品ID |
| regionId | String | 否 | 地区ID |
| alertLevel | String | 否 | 预警级别（level1/level2/level3） |
| isHandled | Boolean | 否 | 是否处理 |
| startDate | String | 否 | 开始日期（YYYY-MM-DD） |
| endDate | String | 否 | 结束日期（YYYY-MM-DD） |
| pageNum | Integer | 否 | 页码（默认1） |
| pageSize | Integer | 否 | 每页数量（默认20） |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 30,
    "pageNum": 1,
    "pageSize": 20,
    "list": [
      {
        "alertId": "A001",
        "productId": "P001",
        "productName": "白菜",
        "regionId": "R001",
        "regionName": "贵阳市",
        "alertTime": "2026-02-07T08:00:00Z",
        "alertLevel": "level1",
        "alertType": "暴涨",
        "currentDate": "2026-02-07",
        "currentPrice": 3.50,
        "normalRangeMin": 2.30,
        "normalRangeMax": 2.80,
        "deviationRate": 35.71,
        "predictedPrice": 2.65,
        "predictionError": 32.08,
        "isHandled": false
      }
    ]
  }
}
```

### 7.2 处理预警

**接口地址：** `PUT /alert/{alertId}/handle`

**路径参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| alertId | String | 是 | 预警ID |

**请求参数：**
```json
{
  "handleResult": "已通知相关部门"
}
```

**响应数据：**
```json
{
  "code": 200,
  "message": "处理成功"
}
```

---

## 8. 预测分析接口

### 8.1 获取价格预测

**接口地址：** `GET /predict/{productId}`

**路径参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| productId | String | 是 | 产品ID |

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| regionId | String | 否 | 地区ID |
| predictDays | Integer | 否 | 预测天数（默认7） |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "productId": "P001",
    "productName": "白菜",
    "regionId": "R001",
    "regionName": "贵阳市",
    "modelName": "Prophet",
    "modelVersion": "1.0.0",
    "trainEndDate": "2026-02-06",
    "predictions": [
      {
        "predictDate": "2026-02-07",
        "predictedPrice": 2.60,
        "confidenceLower": 2.40,
        "confidenceUpper": 2.80,
        "confidenceLevel": 0.95
      },
      {
        "predictDate": "2026-02-08",
        "predictedPrice": 2.62,
        "confidenceLower": 2.42,
        "confidenceUpper": 2.82,
        "confidenceLevel": 0.95
      }
    ]
  }
}
```

### 8.2 获取预测模型信息

**接口地址：** `GET /predict/models`

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "modelName": "Prophet",
      "modelVersion": "1.0.0",
      "description": "Facebook Prophet时间序列预测模型",
      "trainDate": "2022026-02-06",
      "accuracy": 0.92,
      "isActive": true
    },
    {
      "modelName": "LSTM",
      "modelVersion": "1.0.0",
      "description": "长短期记忆网络模型",
      "trainDate": "2026-02-06",
      "accuracy": 0.88,
      "isActive": false
    }
  ]
}
```

---

## 9. 报表导出接口

### 9.1 导出分析报告

**接口地址：** `GET /report/export`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| reportType | String | 是 | 报告类型（price_trend/alert_summary/prediction） |
| productId | String | 否 | 产品ID |
| regionId | String | 否 | 地区ID |
| startDate | String | 否 | 开始日期（YYYY-MM-DD） |
| endDate | String | 否 | 结束日期（YYYY-MM-DD） |
| format | String | 否 | 导出格式（pdf/excel，默认pdf） |

**响应数据：**
```
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="report_20260207.pdf"
```

---

## 10. 数据可视化接口

### 10.1 获取市场热力图数据

**接口地址：** `GET /visualization/market/heatmap`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| productId | String | 是 | 产品ID |
| date | String | 否 | 日期（YYYY-MM-DD，默认当天） |

**响应数据：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "productId": "P001",
    "productName": "白菜",
    "date": "2026-02-07",
    "heatmapData": [
      {
        "regionId":