from django.db import models


class Match(models.Model):

    valuer = models.ForeignKey(
        'person.Person',
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='The one who evaluates',
        default=0,
    )
    expectant = models.ForeignKey(
        'person.Person',
        on_delete=models.CASCADE,
        related_name='evaluated',
        verbose_name='The one who is being evaluated',
        default=0,
    )
    mark = models.BooleanField(
        verbose_name='Is valuer likes expectant',
    )

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    objects = models.Manager()
