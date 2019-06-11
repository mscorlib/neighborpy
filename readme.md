## Neighborpy
-----------
### 简介：  
使用 sk-learn 实现的简单 nearest neighbor 库  
外部接口采用 Flask 开发  
简单、易用


### 接口

|api|method|body|返回值|描述|
|---------|---------|---------|---------|---------|
|/api/engine/ping|GET||'pong'|简单测活接口|
|/api/engine/db/keys|GET||list[str]|获取所有库名|
|/api/engine/db|POST|{'key':str}|bool|创建库|
|/api/engine/db|DELETE|{'key':str}|bool|删除库|
|/api/engine/item|POST|{'db_key':str,'key':str,'feature':[dim]}|bool|添加向量|
|/api/engine/items|POST|[{'db_key':str,'key':str,'feature':[dim]}]|bool|批量添加向量|
|/api/engine/item|DELETE|{'db_key':str,'key':str,'feature':[dim]}|bool|删除向量|
|/api/engine/query|POST|{'db_key':str,'feature':[dim],'take':int}|bool|添加向量|


### 编译

##### 安装 cython
```
pip install cython
```

##### 编译
删除 build 文件夹
```
py build.py
```

将自动编译目标到 build 文件夹


### 运行

##### 启动服务
```
py app.py
```

construct_blueprint() 方法不传入 Storage 对象则使用内存存储数据，仅用于测试、DEMO

### 性能

硬件环境：i7 7700HQ 16G DDR4-2400  
___
    数量：300K  
    维度：128  
    build：5.3s  
    query：89ms  
___
    数量：100K  
    维度：128  
    build：1.98s  
    query：22ms  

### todo：
- [ ] 使用文件持久化 storage_file
- [ ] redis 超过 300k ndarray 持久化后加载出错

