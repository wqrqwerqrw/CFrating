import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'cf.settings'
django.setup()
from web.models import Contest,Student



def main():
    if Student.objects.all().count() != 0:
        for x in Student.objects.all().order_by('last_update_time'):
            print(str(x).encode('utf-8'),end=' : ')
            try:
                x.update()
                print('get success')
            except:
                print('get failed')

if __name__ == "__main__":
    main()
