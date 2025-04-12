from django.db import models


class District(models.Model):
    division_id = models.IntegerField()
    name = models.CharField(max_length=255)
    bn_name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    long = models.DecimalField(max_digits=10, decimal_places=7)

    class Meta:
        db_table = "districts"

    def __str__(self):
        return self.name
