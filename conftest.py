import os
import sys
import django

ems_root = os.path.abspath(os.path.dirname(__file__))
if ems_root not in sys.path:
    sys.path.insert(0, ems_root)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
