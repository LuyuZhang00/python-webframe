import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payment.settings")
django.setup()

from app01 import models


models.Goods.objects.create(title="指甲刀",price=1000)
models.Goods.objects.create(title="砍刀",price=2000)