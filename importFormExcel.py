import os
import sys
from urllib import request
import re
import django
import datetime
from time import sleep
sys.path.append('../cf/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'cf.settings'
django.setup()
from web.models import Contest,Student
import xlrd
