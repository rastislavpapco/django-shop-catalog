from django.db import models


class BaseModel(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        abstract = True


class AttributeName(BaseModel):
    nazev = models.CharField(max_length=128, default="")
    kod = models.CharField(max_length=128, default="")
    zobrazit = models.BooleanField(default=True)


class AttributeValue(BaseModel):
    hodnota = models.CharField(max_length=128, default="")


class Attribute(BaseModel):
    nazev_atributu_id = models.ForeignKey(AttributeName, on_delete=models.CASCADE)
    hodnota_atributu_id = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)


class Product(BaseModel):
    nazev = models.CharField(max_length=256, default="")
    description = models.TextField(default="")
    cena = models.CharField(max_length=128, default="")
    mena = models.CharField(max_length=128, default="")
    published_on = models.CharField(max_length=256, default="", null=True)
    is_published = models.BooleanField(default=True)


class ProductAttributes(BaseModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Image(BaseModel):
    obrazek = models.TextField(default="")


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    obrazek_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    nazev = models.CharField(max_length=256, default="")


class Catalog(BaseModel):
    nazev = models.CharField(max_length=256, default="")
    obrazek_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    products_ids = models.ManyToManyField(Product)
    attributes_ids = models.ManyToManyField(Attribute)
