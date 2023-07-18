from celery.result import AsyncResult
from s1 import app

result_object = AsyncResult(id="8b89c0fd-d5f1-4726-b0f9-839a075fd965", app=app)

# print(result_object.status)
data = result_object.get()
print(data)