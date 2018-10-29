from django.db import models

# Create your models here.
class TUser(models.Model):
    user_email = models.CharField(max_length=50,null=True)
    user_password = models.CharField(max_length=200,null=True)
    user_name = models.CharField(max_length=30,null=True)
    user_status = models.DecimalField(max_digits=1, decimal_places=0,null=True)
    user_salt = models.CharField(max_length=10,null=True)

    class Meta:
        db_table = 't_user'