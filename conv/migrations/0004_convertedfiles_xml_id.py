# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0003_remove_convertedfiles_config_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='convertedfiles',
            name='xml_id',
            field=models.CharField(default=23, max_length=10),
            preserve_default=False,
        ),
    ]
