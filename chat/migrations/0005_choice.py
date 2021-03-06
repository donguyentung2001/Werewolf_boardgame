# Generated by Django 3.0.8 on 2020-08-08 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_groupchat_ready_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_one', models.TextField(default='')),
                ('option_two', models.TextField(default='')),
                ('option_three', models.TextField(default='')),
                ('option_one_count', models.IntegerField(default=0)),
                ('option_two_count', models.IntegerField(default=0)),
                ('option_three_count', models.IntegerField(default=0)),
            ],
        ),
    ]
