# Generated by Django 5.0.6 on 2024-07-07 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prefs', '0002_alter_pref_bot_id_alter_pref_groupchat_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pref',
            name='groupchat_id',
            field=models.CharField(default=1, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
