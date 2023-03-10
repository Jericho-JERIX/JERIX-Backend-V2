# Generated by Django 4.1.2 on 2022-12-29 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_discordmessage_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discordmessageattachment',
            name='message_id',
            field=models.ForeignKey(db_column='message_id', on_delete=django.db.models.deletion.CASCADE, to='api.discordmessage'),
        ),
        migrations.AlterField(
            model_name='discordmessageemoji',
            name='message_id',
            field=models.ForeignKey(db_column='message_id', on_delete=django.db.models.deletion.CASCADE, to='api.discordmessage'),
        ),
        migrations.AlterField(
            model_name='discordmessagementionchannel',
            name='message_id',
            field=models.ForeignKey(db_column='message_id', on_delete=django.db.models.deletion.CASCADE, to='api.discordmessage'),
        ),
        migrations.AlterField(
            model_name='discordmessagementionrole',
            name='message_id',
            field=models.ForeignKey(db_column='message_id', on_delete=django.db.models.deletion.CASCADE, to='api.discordmessage'),
        ),
        migrations.AlterField(
            model_name='discordmessagementionuser',
            name='message_id',
            field=models.ForeignKey(db_column='message_id', on_delete=django.db.models.deletion.CASCADE, to='api.discordmessage'),
        ),
    ]
