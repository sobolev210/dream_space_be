# Generated by Django 4.1.3 on 2022-11-20 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dream_space', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('address', models.CharField(max_length=500, null=True)),
                ('logo', models.FileField(null=True, upload_to='')),
            ],
        ),
    ]
