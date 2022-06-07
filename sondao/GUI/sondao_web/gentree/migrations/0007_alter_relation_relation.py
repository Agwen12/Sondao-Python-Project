# Generated by Django 4.0.5 on 2022-06-07 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gentree', '0006_alter_relation_relation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='relation',
            field=models.CharField(choices=[('CHILD', 'CHILD'), ('FULL_ADOPTED_CHILD', 'FULL_ADOPTED_CHILD'), ('PARTIAL_ADOPTED_CHILD', 'PARTIAL_ADOPTED_CHILD'), ('SIBLING', 'SIBLING'), ('PARENT', 'PARENT'), ('FULL_ADOPTED_PARENT', 'FULL_ADOPTED_PARENT'), ('PARTIAL_ADOPTED_PARENT', 'PARTIAL_ADOPTED_PARENT'), ('SPOUSE', 'SPOUSE'), ('EX_SPOUSE', 'EX_SPOUSE')], max_length=30, verbose_name='Relation type'),
        ),
    ]
