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



def main():
    while True:
        if Student.objects.all().count() != 0:
            x = Student.objects.all().order_by('last_update_time')[0]
            # x = Student.objects.get(cf_id='ZZHzzh0_0')
            print(str(x).encode('utf-8'))
            try:
                x.update()
            except:
                pass
        sleep(120)


if __name__ == "__main__":
    main()
