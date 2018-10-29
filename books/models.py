from django.db import models

# Create your models here.
class TBook(models.Model):

    book_name = models.CharField(max_length=128)
    book_author = models.CharField(max_length=64)
    book_publish = models.CharField(max_length=128)
    publish_time = models.DateField()
    revision = models.IntegerField()
    book_isbn = models.CharField(max_length=64)
    word_count = models.CharField(max_length=64)
    page_count = models.IntegerField()
    open_type = models.CharField(max_length=20)
    book_paper = models.CharField(max_length=64)
    book_wrapper = models.CharField(max_length=64)
    book_category = models.ForeignKey('TCatagory', models.DO_NOTHING, db_column='book_category')
    book_price = models.DecimalField(max_digits=10, decimal_places=2)
    book_dprice = models.DecimalField(max_digits=10, decimal_places=2)
    editor_recommendation = models.IntegerField()
    content_introduction = models.CharField(max_length=2000)
    author_introduction = models.CharField(max_length=2000)
    menu = models.CharField(max_length=2000)
    media_review = models.CharField(max_length=2000)
    digest_image_path = models.CharField(max_length=2000)
    product_image_path = models.ImageField(upload_to="my_cover")
    series_name = models.CharField(max_length=128)
    printing_time = models.DateField()
    impression = models.CharField(max_length=64)
    stock = models.IntegerField()
    shelves_date = models.DateField()
    customer_socre = models.DecimalField(max_digits=3, decimal_places=2)
    book_status = models.DecimalField(max_digits=1, decimal_places=0)
    sales = models.IntegerField()

    class Meta:
        db_table = 't_book'

class TCatagory(models.Model):

    category_name = models.CharField(max_length=20)
    book_counts = models.DecimalField(max_digits=10, decimal_places=0)
    category_pid = models.DecimalField(max_digits=20, decimal_places=0,null=True)

    class Meta:
        db_table = 't_catagory'