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
* 列表类页面及接口带分页功能,p 为页码
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
	category:'0:profession, 1: skill, 2: 用户个人标签,3:资讯'
	hot:'热度'
}
```

###### 收藏
```
collect {
	f_id: 被收藏的_id,
	category:'0:资讯、1：项目、2：招聘职位',
	uid:用户
}
```

###### 页面

1. `用户登录` '/login'
2. `用户注册` '/join' 
3. `邮件认证` '/checkmail'
4. `个人信息设置` '/profile'
5. `修改密码`	 '/setpwd'
6. `登出地址` '/logout'
7. `忘记密码`	 '/forgot_password'
8. `密码重置` '/resetpwd'


###### 站内接口

1. (status,account|msg)     (post'/m/account/login', 'username,password') //用户登录;Cookie 记录 uid, nickname
2. (status,account|msg)     (post'/m/auth/login', 'siteid,otherid,name') //用户登录
3. (status,account|msg)     (get'/m/account/info/(_id)')                //用户信息, _id 用户ID,可变参数
4. (status,msg)     		(post'/m/account/update', 'city,icon,profession,skill,nickname,description,labels') //更新当前登录用户资料
5. (status,account|msg)		(post'/m/account/join','username,password') //需要进行username 的邮箱格式验证
6. (status,label|msg)		(post'/m/label/add','name,category')	//添加标签
7. (status,list(label)|msg) (get'/m/label/suggest','key,category')	//标签智能提示 key 为关键词
8. (status,list(label)|msg) (get'/m/label/list/(category)')		//获取分类标签


### 资讯

###### 资讯字典
```
news {
	title:'标题，3~18',
	body: '内容',
	category:分类listname,
	labels:标签 list(),
	author:作者_id,
	city: 城市_id
}
```

###### 资讯分类字典
```
category {
	name:'名称',
	listname:'唯一代号, 英文字母+数字',
	parent:'父节点_id',
	count: int ,分类下资讯条数
}
```

###### 资讯评论字典
```
comment {
	news_id : 资讯_id,
	body : 内容,
	author : 作者,
	ref : 引用评论_id
}
```

###### 页面

1. `资讯` '/news/(listname)?p=1'  // listname 为分类代号 ,listname 为空时，显示所有资讯
2. `资讯详情` '/news/info/(_id)' // _id 为资讯_id ; 资讯详情下方有评论信息列表
3. `投递新闻` '/news/create'		// 投递新闻
4. `标签资讯列表` '/news/label?key=xxx' //按标签查询生成资讯列表，可接受多个key; key 应为完整的label 


###### 站内接口

1. (status,list(comment)|msg)     (get'/m/comment/list', 'news_id,p') // 获取资讯评论列表
2. (status,comment|msg)			  (post'/m/comment/post','news_id,body,author,ref') //发布资讯评论
3. (status,news|msg)			  (post'/m/news/create','title、body、category,labels,author') //发布资讯
4. (status,list(news)|msg)		  (get'/m/news/label','key') //按标签查询生成资讯列表
5. (status,msg)					  (post'/m/news/delete','_id') //删除资讯

### 项目

###### 项目字典
```
project {
	name:项目名称，
	city:城市id,
	description:简介,
	advantage：优势,
	partner：合伙人 list （智能标签）,
	status: 状态 (0:好主意、1：项目计划书、2：产品原型、3:测试、4：正式上线、5：已有收入、6：已有营利),
	author:发起人,
	apply：申请人列表及状态 list {
		name:合伙标签,
		uid:申请用户,
		status:状态 0:申请, 1:合作中
		}
	
}
```

###### 页面

1. `项目列表` '/project/(label)?p=1' 标签可选 支持分页
2. `项目详情` '/project/info/_id'    项目详情显示项目状态、合作人申请数、成功合作人数
3. `创建项目` '/project/create'	     项目项目 合作人为 智能标签 用户编辑时可删除、添加
4. `申请加入` '/project/join/_id?uid=xx?partner=xxx' 
