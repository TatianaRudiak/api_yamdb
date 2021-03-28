import csv
import os
import sys

import django

from yamdb.models import CustomUser

project_dir = "/home/tatiana/Dev/api_yamdb/api_yamdb"

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

django.setup()

data = csv.reader(open("data/users.csv"), delimiter=',')

for row in data:
    if row[1] != 'username':
        user = CustomUser()
        user.username = row[1]
        user.email = row[2]
        user.role = row[3]
        user.save()
