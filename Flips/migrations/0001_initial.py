# Generated by Django 5.1.3 on 2024-11-24 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_a', models.CharField(default='Heads', max_length=128)),
                ('option_a_weight', models.FloatField(default=0.5)),
                ('option_b', models.CharField(default='Tails', max_length=128)),
                ('option_b_weight', models.FloatField(default=0.5)),
                ('outcome_rating', models.IntegerField(default=2)),
                ('comment', models.CharField(default='', max_length=256)),
            ],
        ),
    ]