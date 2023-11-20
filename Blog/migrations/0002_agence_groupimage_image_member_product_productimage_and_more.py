# Generated by Django 4.1.3 on 2022-12-01 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=1000)),
                ('Address', models.CharField(max_length=1000)),
                ('Phone', models.CharField(max_length=1000)),
                ('Fax', models.CharField(max_length=1000)),
                ('CreatedAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-id',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=300)),
                ('CreatedAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-id',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Link', models.ImageField(upload_to='Gallery')),
                ('Group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Blog.groupimage')),
            ],
            options={
                'ordering': ('-id',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=1000)),
                ('Profile', models.ImageField(upload_to='Member Profile')),
                ('Phone', models.CharField(max_length=20)),
                ('Email', models.EmailField(max_length=150)),
                ('CreatedAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-id',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=1000)),
                ('Description', models.TextField()),
                ('CreatedAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-id',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='Product Image')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Blog.product')),
            ],
            options={
                'ordering': ('-id',),
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Gallery',
        ),
    ]
