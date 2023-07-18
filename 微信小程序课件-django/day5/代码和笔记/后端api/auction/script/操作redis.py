import redis

conn = redis.Redis(host='192.168.16.86', port=6379)
# conn.set('foo', 'Bar')
#
result = conn.get('+8615131255089')
print(result)
# conn.flushall()
print(conn.keys())

