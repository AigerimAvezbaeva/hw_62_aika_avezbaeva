from django.db import models


class Project(models.Model):
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата и время создания'
    )
    completed_at = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата и время окончания'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        default='No name'
    )
    description = models.TextField(
        max_length=3000,
        verbose_name='описание'
    )

    def __str__(self):
        return self.name
