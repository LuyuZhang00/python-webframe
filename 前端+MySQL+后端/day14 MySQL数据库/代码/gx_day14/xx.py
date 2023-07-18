import requests

USER_LIST = []


def register():
    """ 用户注册 """

    # 1.循环提示用户输入  用户名  密码（输入q/Q 停止注册）

    # 2.将用户名和密码构建成字典 {"name":"用户输入密码","pwd":"用户输入的密码"}，并添加到全局变量 USER_LIST中


def show_users():
    """ 查询用户信息 """

    # 1. 获取全局变量中USER_LIST，并实现所有的用户信息

    # 2. 构造每一行数据，然后输出（每个用户的密码的后四位用 * 代替），例如：
    """输出
    用户名：wupeiqi，密码：123f****
    用户名：wupeiqi，密码：123f****
    用户名：wupeiqi，密码：123f****
    """




def run():
    func_dict = {
        "1": register,
        "2": show_users,
    }
    print("欢迎使用xx系统")
    while True:
        print("1.注册；2.查看用户列表")
        choice = input("请输入序号：")
        if choice.upper() == 'Q':
            return
        func = func_dict.get(choice)
        if not func:
            print("输入错误")
            continue
        func()


run()
