# Generated by Django 2.2.11 on 2020-03-30 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manifest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_step', models.TextField()),
                ('_type', models.TextField()),
                ('_value', models.TextField()),
                ('_desc', models.TextField()),
                ('_imported_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
