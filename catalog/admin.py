from django.contrib import admin

from catalog import models

# Register your models here.
admin.site.register(models.AttributeName)
admin.site.register(models.AttributeValue)
admin.site.register(models.Attribute)
admin.site.register(models.Product)
admin.site.register(models.ProductAttributes)
admin.site.register(models.Image)
admin.site.register(models.ProductImage)
admin.site.register(models.Catalog)
