# Generated by Django 4.1.3 on 2022-12-01 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_agence_groupimage_image_member_product_productimage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='Post',
            field=models.CharField(default='System Designer', max_length=200),
            preserve_default=False,
        ),
    ]
