
from django.db import migrations

from django.db import migrations, models
import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

def add_initial_balance(apps, sch_editor):
    InitialBalance = apps.get_model('schol_library', 'InitialBalance')
    hz= InitialBalance.objects.all()
    for item in hz:
        item.save()
        print(item)


class Migration(migrations.Migration):

    dependencies = [
        ('schol_library', '0159_auto_20200518_1548'),
    ]

    operations = [ migrations.RunPython(add_initial_balance)

    ]
