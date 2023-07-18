class Foo(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


obj1 = Foo("IT部门")
print(obj1)  # 输出对象时，如果想要定制显示的内容。

obj2 = Foo("销售部")
print(obj2)  # 输出对象时，如果想要定制显示的内容。
