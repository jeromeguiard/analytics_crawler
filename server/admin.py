from flask import Flask
from flask.ext import admin
from flask.ext.admin.contrib.peewee import ModelView
import os
import subprocess
from peewee import *
from models import *
app = Flask(__name__)


class ClientAdmin(ModelView):
  pass
class InfosAdmin(ModelView):
  pass
class ClientToInfosAdmin(ModelView):
  pass

if __name__ == '__main__':
  import logging
  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  admin = admin.Admin(app, 'Peewee Models')
  admin.add_view(ClientAdmin(Client))
  admin.add_view(InfosAdmin(Infos))
  admin.add_view(ClientToInfosAdmin(ClientToInfos))
  Client.create_table(fail_silently=True)
  Infos.create_table(fail_silently=True)
  ClientToInfos.create_table(fail_silently=True)
  app.run(debug=True)
