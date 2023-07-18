data = "中"
res = data.encode('utf-8')
print(res)  # b'\xe4\xb8\xad'


data = "国"
res = data.encode('gbk')
print(res)  # b'\xb9\xfa'
