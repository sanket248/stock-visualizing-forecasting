# Generated by Django 4.0.1 on 2022-02-18 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualize', '0004_companyfundamentals_rev2018_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyfundamentals',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='companyfundamentals',
            name='sector',
            field=models.CharField(max_length=100),
        ),
    ]
