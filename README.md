migrant 回归线
=======

回归线：高新人才的 回乡创业、就业、生活平台；

假如你还在考虑回老家可以做什么，回家怎么才能发展的好，回归线，是你不错的选择。

相关链接
-----------

* [设计需求文档](https://github.com/comger/migrant/wiki)
* [技术文档及约定](https://github.com/comger/migrant/blob/master/doc/web.md)


项目相关技术
=======
python、mongodb、redis、bootstrap, android ,ios, kpages, jquery, html5；


项目现已使用MIT开源协议，欢迎大家加入我们的开源项目,和我们一起完善这个项目；一起开发、一起学习、一起为社会做点事吧。
=======


#### 项目依赖

```
   软件：python, mongodb, redis ；
   python 包：kpages( easy_install kpages) 
   
   mongodb 启动指令为 mongod --dbpath you data path
   redis 启动指令为 redis-server 
   
```

#### 使用mongodb dump 数据

```
mongorestore  -d migrant --directoryperdb dump/migrant
如果需要备份数据,请使用  mongodump -d migrant -o dump

dump数据中的测试账号为： admin , adminpwd
```

#### Kpages

```
基于Tornado的开发包，提供地址路由、配置、测试、性能分析、数据库及内存连接上下文管理等，如果你想用Tornado提供一些高性能的服务接口，这会给你很大的帮助的。
详情请查看：https://github.com/comger/kpages
```


### web 服务启动方式 
```
python apprun.py  或 ./apprun.py
可配置参数
     config=CONFIG  set config for server
     port=PORT      set http port for server
     debug          Debug mode.
     ndebug         No Debug mode.
```



### 执行测试案例
```
    python tool.py --test test_city.DemoCase.testprint :test testprint method
    python tool.py --test test_city.DemoCase           :test methods in DemoCase class
    python tool.py --test test_city                    :test methods in test_city.py
    python tool.py --test all                          :test methods in app's __conf__.UTEST_DIR
```




