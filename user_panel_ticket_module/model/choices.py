from django.db import models


class TicketStatus(models.TextChoices):
    Pending = 'Pending', 'درحال بررسی'
    AnsweredByUser = 'AnsweredByUser', 'پاسخ داده شده توسط کاربر'
    AnsweredByAdmin = 'AnsweredByAdmin' , 'پاسخ داده شده'
    Closed = "Closed" , "بسته شده"

class TicketPriorities(models.TextChoices):
    Normal = 'Normal', 'معمولی'
    Important = 'Important', 'مهم'
    MuchImportant = 'MuchImportant' , 'بسیار مهم'

class TicketSections(models.TextChoices):
    Technical= 'Technical', 'بخش فنی'
    Finance = 'Finance', 'بخش مالی'
    HR = 'HR' , 'منابع انسانی'