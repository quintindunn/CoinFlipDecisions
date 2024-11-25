from django.conf import settings
from django.db import models


class Flip(models.Model):
    private = models.BooleanField(default=False, null=False)

    option_a = models.CharField(max_length=128, default="Heads", blank=False, null=False)
    option_a_weight = models.FloatField(default=0.5, null=False)

    option_b = models.CharField(max_length=128, default="Tails", blank=False, null=False)
    option_b_weight = models.FloatField(default=0.5,  null=False)

    outcome_rating = models.IntegerField(default=0)  # 0 == unrated, 1 == Bad, 2 == Neutral, 3 == Happy
    comment = models.CharField(max_length=256, default="")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
