from django.db import models


class Audit(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class customer_profile(Audit):
    class Meta:
        db_table = "ec_customers"

    customer_id = models.BigAutoField(primary_key=True)

    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)