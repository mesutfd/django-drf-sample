# Generated by Django 5.0.3 on 2024-03-16 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0003_article_character_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published',
            field=models.BooleanField(db_default=True),
        ),
    ]