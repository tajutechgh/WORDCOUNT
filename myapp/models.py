from django.db import models
 
#Create your models here.
class WordCount(models.Model):
    text = models.TextField(max_length=500)
