# Generated by Django 5.2.4 on 2025-07-26 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_alter_conversation_id_alter_message_id_alter_user_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-sent_at']},
        ),
    ]
