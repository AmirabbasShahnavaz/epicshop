from django.db import models


class State(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    parent = models.ForeignKey('self',null=True,blank=True, on_delete=models.CASCADE, verbose_name='والد')

    def __str__(self):
        return self.title