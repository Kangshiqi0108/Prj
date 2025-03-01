PrjName：混合分组实现平台

核心功能  
动态分组策略：基于遗传算法实现多维度（能力/性别/风格）权重配置，支持同质/异质化分组  
数据管理：Excel 文件批量导入学习者数据（FastAPI + Pandas）  
安全认证：JWT 令牌鉴权 + 邀请码注册机制  

技术实现  
后端
FastAPI 构建 RESTful API，SQLModel 操作 MySQL  
熵值法量化特征离散度，scikit-opt 库实现遗传算法优化  
- 日志分级管理（业务/访问日志），CORS 跨域支持  

前端  
Vue3 响应式界面，动态表单配置分组策略  
路由守卫控制权限，Fetch API 实现文件上传与结果展示  
