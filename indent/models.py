from django.db import models

# Create your models here.
from books.models import TBook
from user.models import TUser


class TAddress(models.Model):
    name = models.CharField(max_length=20)
    detail_address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    telphone = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20)
    user = models.ForeignKey(TUser, models.DO_NOTHING)

    class Meta:
        db_table = 't_address'


class TOrder(models.Model):
    id = models.CharField(max_length=60,primary_key=True)
    num = models.DecimalField(max_digits=20, decimal_places=0)
    create_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    order_addrid = models.ForeignKey(TAddress, models.DO_NOTHING, db_column='order_addrid')
    order_uid = models.ForeignKey(TUser, models.DO_NOTHING, db_column='order_uid')
    status = models.DecimalField(max_digits=1, decimal_places=0)

    class Meta:
        db_table = 't_order'


class TOrderitem(models.Model):
    shop_bookid = models.ForeignKey(TBook, models.DO_NOTHING, db_column='shop_bookid')
    shop_ordid = models.ForeignKey("TOrder", models.DO_NOTHING, db_column='shop_ordid')
    shop_num = models.DecimalField(max_digits=20, decimal_places=0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 't_orderitem'

