# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0002_convertedfiles_json_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convertedfiles',
            name='config_file',
        ),
    ]
