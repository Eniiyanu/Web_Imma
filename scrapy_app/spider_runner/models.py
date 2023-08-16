from django.db import models

class Spider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    command = models.CharField(max_length=255)
    spider_file = models.CharField(max_length=255)
    spider_class = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# models.py

class SpiderExecution(models.Model):
    spider_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
