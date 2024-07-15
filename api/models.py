from django.db import models


class BondPost(models.Model):
    bond_name = models.CharField(max_length=50)
    isin = models.CharField(max_length=12, unique=True)
    bond_value = models.BigIntegerField()
    interest_rate = models.FloatField()
    purchase_date = models.DateTimeField()
    due_date = models.DateTimeField()
    yields_freq = models.IntegerField()

    def __str__(self) -> str:
        return self.bond_name + ' ' + self.isin
