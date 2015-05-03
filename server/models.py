import peewee
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("conf.cfg")

database = peewee.MySQLDatabase(config.get("db", "db_name"),
                                user=config.get("db", "db_user"),
                                password=config.get("db", "db_pass"))
class BaseModel(peewee.Model):  

  class Meta:
    database = database 

class Infos(BaseModel):
  """
  Metrics and dimensions to retrieve
  """
  metrics = peewee.TextField()
  dimensions = peewee.TextField(null=True)

  def __unicode__(self):
    return "%s & %s" % (self.metrics, self.dimensions)

class Client(BaseModel):
  """
  Represent a clien model with a website
  in db client table
  """
  site_id = peewee.IntegerField() 
  name = peewee.TextField()
  site_name = peewee.TextField()

  def __unicode__(self):
    return "%s @ %s" % (self.name, self.site_name)


class ClientToInfos(BaseModel):
  """
  Create a link between client and infos
  """
  client = peewee.ForeignKeyField(Client, related_name='get_infos')
  infos = peewee.ForeignKeyField(Infos)

  def __unicode__(self):
    return "%s %s" % (self.client, self.infos)

class DB(object):

  def get_type(self, str_type):
    return {
      "STRING"  : peewee.TextField(),
      "INTEGER" : peewee.IntegerField(), 
      "DATE" : peewee.DateTimeField() 
    }[str_type]

  def get_db(self):
    return database

  def get_peewee_fields(self, elements):
    elements_to_return = {}
    for element in elements.iteritems():
      elements_to_return.update({element[0] : self.get_type(element[1])})
    return elements_to_return

  def get_model(self, table, elements):
    elements = self.get_peewee_fields(elements)
    myModelClass = type(table, (BaseModel,), elements)
    mdl = myModelClass()
    mdl.create_table(fail_silently = True)
    return mdl
