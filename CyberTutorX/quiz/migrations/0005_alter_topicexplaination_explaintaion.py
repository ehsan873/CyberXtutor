# Generated by Django 4.2.1 on 2023-09-30 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_topicexplaination_for_class_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicexplaination',
            name='explaintaion',
            field=models.TextField(blank=True),
        ),
    ]
