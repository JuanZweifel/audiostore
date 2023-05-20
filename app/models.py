from django.db import models

# Create your models here.
class Categoria(models.Model):
    id_cat=models.AutoField(primary_key=True, null=False)
    nom_cat=models.CharField(max_length=50, null=False)

class Marca(models.Model):
    id_marca=models.AutoField(primary_key=True, null=False)
    nom_marca=models.CharField(max_length=50, null=False)