# Generated by Django 4.1.3 on 2022-12-20 14:28

import Job.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0003_alter_email_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpressionOfIntesertOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=1000)),
                ('Description', models.TextField()),
                ('Document', models.FileField(upload_to=Job.models.offer_get_folder_name)),
                ('Actif', models.BooleanField(default=True)),
                ('CheckEmail', models.EmailField(max_length=254)),
                ('CreatedAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-id',),
                'abstract': False,
            },
        ),
    ]