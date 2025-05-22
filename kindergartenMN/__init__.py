import pymysql
pymysql.install_as_MySQLdb()

from .celery import app as celery_app

default_app_config = 'kindergartenMN.apps.KindergartenmnConfig'
