# Generated by Django 4.0.1 on 2022-02-02 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualize', '0003_companyfundamentals_div_companyfundamentals_volume'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyfundamentals',
            name='rev2018',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='companyfundamentals',
            name='rev2019',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='companyfundamentals',
            name='rev2020',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='companyfundamentals',
            name='rev2021',
            field=models.BigIntegerField(null=True),
        ),
    ]