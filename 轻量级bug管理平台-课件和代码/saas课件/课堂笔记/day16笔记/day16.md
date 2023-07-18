# day16

- 杨礼，未到
- 毕云峰，fk没有做；自己不知道如何实现。
- 朱鑫朝，未到
- 高楚凡，未到
- 武爱华，是否空列表/空值, -> []  ; 
- 邵婉婷，未到
- 洪力君，家里停电今天补。
- 江栋，没来及。



## 今日概要

- 筛选
  - choices
  - fk
  - select2
- 邀请成员
- 概览

注意：提前准备支付宝沙箱环境 + ”沙箱版支付宝“



## 今日详细

### 1.筛选

#### 1.2 FK

#### 1.3 select2



### 2.邀请

#### 2.1 表结构设计

| ID   | 有效期 | 数量 | 使用数量 | 创建者 | 邀请码   | 项目 |
| ---- | ------ | ---- | -------- | ------ | -------- | ---- |
| 1    | 24     |      |          | 4      | asdfasdf | 88   |
|      |        |      |          |        |          |      |
|      |        |      |          |        |          |      |

```python
class ProjectInvite(models.Model):
    """ 项目邀请码 """
    project = models.ForeignKey(verbose_name='项目', to='Project')
    code = models.CharField(verbose_name='邀请码', max_length=64, unique=True)
    count = models.PositiveIntegerField(verbose_name='限制数量', null=True, blank=True, help_text='空表示无数量限制')
    use_count = models.PositiveIntegerField(verbose_name='已邀请数量', default=0)
    period_choices = (
        (30, '30分钟'),
        (60, '1小时'),
        (300, '5小时'),
        (1440, '24小时'),
    )
    period = models.IntegerField(verbose_name='有效期', choices=period_choices, default=1440)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo', related_name='create_invite')
```

#### 2.2 开发

##### 2.2.1 对话框

##### 2.2.2 生成邀请码

##### 2.2.3 访问

### 3.概览

![image-20200402114520023](assets/image-20200402114520023.png)

#### 3.1 详细

#### 3.2 问题

#### 3.3 成员

#### 3.4 动态

#### 3.5 问题趋势



## 今日作业

- 筛选

  - FK
  - select2

  筛选：CheckFilter/SelectFilter

- 邀请
  - 数据库实现
  - 【可选】redis 哈希
- 概览部分
- 【预习】
  - highcharts，专门用于画图的js库。
  - daterangepicker，专门用于选择时间区间的插件。
  - 支付宝支付
    - 沙箱环境，虚拟钱 ； 沙箱版支付宝（安卓）
    - 正式环境，真钱；





















































































