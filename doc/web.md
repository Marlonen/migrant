## Migrant 数据字典、页面及站内接口设计

### 备注
```
* 所有数据表都有_id 这个字段,
* 所有表的添加时间都包含在_id 表中,并由_id 生成
* 所有表都包含status 字段, -1：记录失效，0 or None : 初始, 其它见详情
* 未申明数据类型的字段默认为 字符串Char
* 接口通信返回都是JSON 格式, 格式为 {status:True|False, data:data}
* 接品格式说明 eg: (status,account|msg)     (post'/m/account/login', 'username,password') //用户登录;Cookie 记录 uid, nickname
 	> (status,account|msg) 返回信息 {status:True|False, data:account|msg}
 	> (post'/m/account/login', 'username,password') post|get 是Request method, 
 	> '/m/account/login' 为url
 	> 'username,password' 为请求参数
 	> //用户登录;Cookie 记录 uid, nickname : 注解说明
```

### 用户中心

###### 用户字典
```
account {
	'username':'用户名 (邮件格式)',
	'password':'密码, 4~18个',
	'isadmin':'是否为管理员',
	'nickname':'呢称, 2~12个有效字符',
	'profession':'职业 （由系统自动学习管理标签), list()',
	'skill':'技能 （由系统自动学习管理标签) list()',
	'description':'简介',
	'labels':'个人标签 （由系统自动学习管理标签)',
	'status':'int 0 : 注册成功, 1: 邮件激活, 2: 老乡认证',
	'icon':'头像地址'
}
```
###### 标签
```
label {
	name:'标签内容',
	category:'0:profession, 1: skill, 2: 用户个人标签'
	hot:'热度'
}
```

###### 页面

1. `用户登录` -'/login'
2. `用户注册` -'/reg' 

###### 站内接口

1. (status,account|msg)     (post'/m/account/login', 'username,password') //用户登录;Cookie 记录 uid, nickname
2. (status,account|msg)     (post'/m/auth/login', 'siteid,otherid,name') //用户登录
3. (status,account|msg)     (get'/m/account/info(/_id)')                //用户信息,_id 用户ID
4. (status,msg)     		(post'/m/account/update', 'city,icon,profession,skill,nickname,description,labels') //更新当前登录用户资料
5. (status,account|msg)		(post'/m/account/reg',)

