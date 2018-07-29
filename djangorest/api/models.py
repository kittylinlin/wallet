from django.db import models

# Create your models here.


class Bill(models.Model):
    category = models.CharField(max_length=255)
    # Car, Food & Drink, Shopping, Entertainment
    description = models.CharField(max_length=255)
    amount = models.IntegerField()
    date = models.DateField(null=True)
    miscellaneous = models.CharField(max_length=255, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='bill', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.category)
