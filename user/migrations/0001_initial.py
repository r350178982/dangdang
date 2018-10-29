# Generated by Django 2.0.2 on 2018-10-25 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=50, null=True)),
                ('user_password', models.CharField(max_length=200, null=True)),
                ('user_name', models.CharField(max_length=30, null=True)),
                ('user_status', models.DecimalField(decimal_places=0, max_digits=1, null=True)),
                ('user_salt', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 't_user',
            },
        ),
    ]
