from django.db import models
from django.utils.text import slugify
from datetime import time

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Client(models.Model):
    client_email = models.EmailField(unique=True, verbose_name='e-mail')
    name = models.CharField(max_length=150, verbose_name='Название(ФИО)')
    description = models.TextField(max_length=500, verbose_name='Комментарий', **NULLABLE)


class Mailing(models.Model):
    MAILING_STATUS = (
        ('create', ' Создано'),
        ('start', 'Запущена'),
        ('stop', 'Завершена')
    )
    MAILING_PERIOD = (
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно')
    )

    name = models.CharField(max_length=150, )
    status = models.CharField(max_length=6, choices=MAILING_STATUS, default='create', verbose_name='Статус')
    period = models.CharField(max_length=6, choices=MAILING_PERIOD, default='daily', verbose_name='Периодичность')
    send_day = models.IntegerField(verbose_name='день от начала периода', default=1)
    start_date = models.DateField(verbose_name='Дата начала', **NULLABLE)
    finish_date = models.DateField(verbose_name='дата завершения', **NULLABLE)


class MailingMessage(models.Model):
    name = models.CharField(max_length=150, verbose_name='Тема')
    slug = models.CharField(max_length=150, verbose_name='Слаг', db_index=True)
    content = models.TextField(verbose_name='Текст сообщения')

    def __str__(self):
        return f'Сообщение: {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            title = str(self.name)
            string = title.translate(
                str.maketrans("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                              "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"))
            self.slug = slugify(string)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('name',)


class RecipientList(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    recipient = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Получатель')
