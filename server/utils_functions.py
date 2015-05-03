import jwt
import time
import requests
import ConfigParser
from datetime import date, timedelta

config =ConfigParser.ConfigParser()
config.read("conf.cfg")

def get_token():
  """
  Retrieve access token with a JWT token
  """
  f = open("token", "r")
  token = f.readline()
  f.close()
  token_splitted = token.split(",")
  if time.time() < float(token_splitted[1]) :
    return token_splitted[0]
  
  key = jwt.rsa_load(config.get("api", "private_key"))
  token = jwt.encode({
         "iss" : config.get("api", "iss"),
         "scope" : config.get("api", "scope"),
         "aud":"https://accounts.google.com/o/oauth2/token",
         "exp":int(time.time()) + 3600,
         "iat":int(time.time())
          },key, "RS256")
  
  payload = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
  url = "https://accounts.google.com/o/oauth2/token"
  
  rep = requests.post(url, headers = headers, data=payload)
  rep_as_json = rep.json()
  
  f = open("token", "w")
  f.write(rep_as_json.get("access_token")+","+str(time.time()+3600))
  f.flush()
  f.close()

  return rep_as_json.get("access_token")

def get_arguments(str_arg, application):
  """
  Build url arguments
  """
  if str_arg is None:
    return ""
  arguments_list = str_arg.split(",")
  string_to_return = ""
  for arg in arguments_list:
    string_to_return = string_to_return + application + ":" + arg + "," 
  return string_to_return[0:-1]

def get_table_name(table_name):
  """
  Retrieve table name to store infos
  """
  string_to_return = ""
  for tab in table_name:
    string_to_return += tab[3:] +"_"
  return string_to_return[0:-1]

def get_start_date(str_arg):
  """
  Base on the since arguement find the start date for the request
  """
  return {
    'day': "today",
    'week': (date.today()-timedelta(days=time.gmtime()[6])).isoformat(),
    'month': (date.today()-timedelta(days=time.gmtime()[2]-1)).isoformat(),
    'year': str(time.gmtime()[7]-1)+"daysAgo",
  }[str_arg]


def call_google_api(access_token, args):
  headers = {"Authorization" : "Bearer "+access_token}
  url ="https://www.googleapis.com/analytics/v3/data/ga?ids=ga:"+args.siteid
  url += "&start-date=" + get_start_date(args.since) +"&end-date=today"
  if  args.dimensions != "":
    url += "&dimensions=" + get_arguments(args.dimensions, args.application)
  url += "&metrics=" + get_arguments(args.metrics, args.application)

  return requests.get(url, headers = headers)
