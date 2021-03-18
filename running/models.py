# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from smart_selects.db_fields import ChainedForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

class Continents(models.Model):
    name = models.CharField(max_length=16, blank=True, null=True)
    cname = models.CharField(max_length=16, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('洲')
        managed = False
        db_table = 'continents'

    def __str__(self):
        return self.cname if self.cname else ""

class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    continent_id = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    full_cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = _('国家')
        managed = False
        db_table = 'countries'

    def __str__(self):
        return self.cname if self.cname else ""

class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    country_id = models.IntegerField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('美属区域')
        managed = False
        db_table = 'area'

    def __str__(self):
        return self.cname if self.cname else ""

class States(models.Model):
    state_id = models.AutoField(primary_key=True)
    country_id = models.ForeignKey(Countries, db_column='country_id', null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    code_full = models.CharField(max_length=255, blank=True, null=True)
    area_id = models.ForeignKey(Area, db_column='area_id', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = _('省')
        managed = False
        db_table = 'states'

    def __str__(self):
        return self.cname if self.cname else self.name if self.name else ""

class Cities(models.Model):
    city_id = models.AutoField(primary_key=True)
    state_id = models.ForeignKey(States, db_column='state_id', null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    code_full = models.CharField(max_length=9)

    class Meta:
        verbose_name_plural = _('市')
        managed = False
        db_table = 'cities'

    def __str__(self):
        return self.cname if self.cname else self.name if self.name else ""

class Regions(models.Model):
    id = models.AutoField(primary_key=True)
    city_id = models.ForeignKey(Cities, db_column='city_id', null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=50, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    code_full = models.CharField(max_length=12)

    class Meta:
        verbose_name_plural = _('县')
        managed = False
        db_table = 'regions'

    def __str__(self):
        return self.cname if self.cname else ""
