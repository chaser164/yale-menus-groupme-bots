# Generated by Django 5.0.6 on 2024-07-07 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pref',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pref_string', models.CharField(max_length=300)),
                ('bot_id', models.CharField(max_length=50)),
                ('groupchat_url', models.URLField()),
            ],
        ),
    ]
