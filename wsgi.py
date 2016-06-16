#import os
#from os.path import join,dirname,abspath
# 
#PROJECT_DIR = dirname(dirname(abspath(__file__)))#3
#import sys # 4
#sys.path.insert(0,PROJECT_DIR) # 5
# 
#os.environ["DJANGO_SETTINGS_MODULE"] = "xin_show.settings" # 7
# 
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
import os
import sys

from django.core.wsgi import get_wsgi_application


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + os.sep

sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'xin_show.settings'

application = get_wsgi_application()