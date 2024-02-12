from django.db import models


class AttributeName(models.Model):
    id = models.IntegerField(primary_key=True)
    nazev = models.CharField(max_length=128, default="")
    kod = models.CharField(max_length=128, default="")
    zobrazit = models.BooleanField(default=True)


class AttributeValue(models.Model):
    id = models.IntegerField(primary_key=True)
    hodnota = models.CharField(max_length=128, default="")


class Attribute(models.Model):
    id = models.IntegerField(primary_key=True)
    nazev_atributu_id = models.ForeignKey(AttributeName, on_delete=models.CASCADE)
    hodnota_atributu_id = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    nazev = models.CharField(max_length=256, default="")
    description = models.TextField(default="")
    cena = models.CharField(max_length=128, default="")
    mena = models.CharField(max_length=128, default="")
    published_on = models.CharField(max_length=256, default="", null=True)
    is_published = models.BooleanField(default=True)


class ProductAttributes(models.Model):
    id = models.IntegerField(primary_key=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    obrazek = models.TextField(default="")


class ProductImage(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    obrazek_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    nazev = models.CharField(max_length=256, default="")


class Catalog(models.Model):
    id = models.IntegerField(primary_key=True)
    nazev = models.CharField(max_length=256, default="")
    obrazek_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    products_ids = models.ManyToManyField(Product)
    attributes_ids = models.ManyToManyField(Attribute)
