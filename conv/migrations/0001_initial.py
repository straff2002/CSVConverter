# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configurations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('config_name', models.CharField(max_length=64)),
                ('config_text', models.TextField()),
                ('upload_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date uploaded')),
            ],
        ),
        migrations.CreateModel(
            name='ConvertedFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=64)),
                ('xml_text', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('config_file', models.ForeignKey(to='conv.Configurations')),
            ],
        ),
    ]
