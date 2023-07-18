# day14 问题管理

## 今日概要

- 添加问题
- 问题列表 + 分页
- 编辑问题
  - 回复
  - 问题变更

## 今日详细

### 1.添加问题

#### 1.1 数据初始化

#### 1.2 添加数据（成功之后刷新）

#### 1.3 错误提示

#### 1.4 扩展【可选】

```
- bootstrap-select
- 下拉框渲染（自定义插件）
```

### 2.问题列表和分页

#### 2.1 问题列表

#### 2.2 分页

```
http://127.0.0.1:8002/manage/9/issues/?page=1
http://127.0.0.1:8002/manage/9/issues/?page=2
- 数据库获取数据
	models.User.objects.all()[0:10]
	models.User.objects.all()[10:20]
	....
- 显示页码
	- 当前访问的页码
	- 显示11个页面（前5个、后5个）
```



### 3.编辑问题

#### 3.1 编辑页面展示

#### 3.2 问题讨论（回复嵌套）

| ID   | 内容 | 类型     | 评论者 | 时间 | FK自己 | FK问题 |
| ---- | ---- | -------- | ------ | ---- | ------ | ------ |
|      |      | 回复     |        |      |        |        |
|      |      | 修改记录 |        |      |        |        |
|      |      |          |        |      |        |        |

```python
class IssuesReply(models.Model):
    """ 问题回复"""

    reply_type_choices = (
        (1, '修改记录'),
        (2, '回复')
    )
    reply_type = models.IntegerField(verbose_name='类型', choices=reply_type_choices)

    issues = models.ForeignKey(verbose_name='问题', to='Issues')
    content = models.TextField(verbose_name='描述')
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo', related_name='create_reply')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复', to='self', null=True, blank=True)
```

##### 3.2.1 ajax请求获取

- 获取评论
- js嵌套展示

##### 3.2.2 评论&回复

- 回复
- 评论



## 今日作业

1. 创建项目时，初始化`问题类型`
2. 添加时数据的合理性
3. 数据展示 & 分页
4. 编辑
   1. markdown插件处理
   2. 多级评论和回复
5. 问题变更
   - 给其他标签绑定change事件，发送评论 + 页面增加
   - markdown插件 -> 点击确定修改























