# Generated by Django 4.1.3 on 2022-12-20 20:33

import Job.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0004_expressionofintesertoffer'),
    ]

    operations = [
        migrations.AddField(
            model_name='expressionofintesert',
            name='EOI',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.RESTRICT, to='Job.expressionofintesertoffer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expressionofintesertoffer',
            name='Document',
            field=models.FileField(
                upload_to=Job.models.eoi_offer_get_folder_name),
        ),
    ]
