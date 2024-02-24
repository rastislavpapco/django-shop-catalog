from django.db import models


class BaseModel(models.Model):
    id = models.IntegerField(primary_key=True)
    objects = models.Manager()

    class Meta:
        abstract = True


class AttributeName(BaseModel):
    name = models.CharField(max_length=128, default="")
    code = models.CharField(max_length=128, default="")
    show = models.BooleanField(default=True)


class AttributeValue(BaseModel):
    value = models.CharField(max_length=128, default="")


class Attribute(BaseModel):
    attribute_name_id = models.ForeignKey(AttributeName, on_delete=models.CASCADE)
    attribute_value_id = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)


class Product(BaseModel):
    name = models.CharField(max_length=256, default="")
    description = models.TextField(default="")
    price = models.CharField(max_length=128, default="")
    currency = models.CharField(max_length=128, default="")
    published_on = models.CharField(max_length=256, default="", null=True)
    is_published = models.BooleanField(default=True)


class ProductAttributes(BaseModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Image(BaseModel):
    image = models.TextField(default="")


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default="")


class Catalog(BaseModel):
    name = models.CharField(max_length=256, default="")
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    products_ids = models.ManyToManyField(Product)
    attributes_ids = models.ManyToManyField(Attribute)
