import time
import datetime
import argparse
import jwt
import M2Crypto
import requests
from Crypto.PublicKey import RSA
from models import DB
from utils_functions import get_token, get_arguments, get_start_date, get_table_name, call_google_api
import json

def main():
  """
  Main function to launch the parser

  Parser arguments : 
    dimensions
    metrics
    application
    siteid
    table
    since
  """

  parser = argparse.ArgumentParser(description='Process resource to reach')
  parser.add_argument('--dimensions', type=str, default="",
                      help='Dimensions you want. Seperate by a ","')
  parser.add_argument('--metrics', type=str,
                      help='Metrics you want separate by a ","')
  parser.add_argument('--application', type=str,
                      help='ga for Google Analytic', default="ga")
  parser.add_argument('--siteid', type=str, help='Site id')
  parser.add_argument('--table', type=str, help='Table name')
  parser.add_argument('--mode', type=str, help='Table name', default="prod")
  parser.add_argument('--since', type=str, default="month",
                      help='Retrieve info since',
                      choices=['day', 'week', 'month', 'year'] )
  
  args = parser.parse_args()

  #Setting mode
  debug = False
  if args.mode == "debug":
    debug = True
    print time.time()
    print "get_token"

  #Retrieve token
  access_token = get_token()

  if debug == True:
    print time.time()
    print "Make call google"
  
  #Retrieve api informations
  rep = call_google_api(access_token, args)

  if debug ==True:
    print time.time()

  content = rep.json()
  
  if debug == True:
    print time.time()
    print content

  headers = content.get("columnHeaders")

  query_infos = content.get("query")
  rows = content.get("rows")
  table_name = query_infos.get("metrics")
  site_id = query_infos.get("ids")[3:]

  if args.dimensions != "":
    table_name = "_".join(args.metrics.split(",") + args.dimensions.split(","))
  else:
    table_name = "_".join(args.metrics.split(",")) 

  d = DB()
  elements = {"site_id" : "INTEGER",
              "from_date" : "DATE",
              "to_date" : "DATE",
              "infos" : "STRING",
              "data": "STRING"
              }
  
  model_to_save = d.get_model(table_name.encode('ascii', 'ignore'), elements)
  model_to_save.infos = headers
  model_to_save.site_id = site_id  
  model_to_save.to_date = datetime.datetime.today().isoformat() 
  model_to_save.from_date = get_start_date(args.since)  
  model_to_save.data = json.dumps(content.get(u"rows"))[1:-1]
  model_to_save.save()

  if debug == True:
    print time.time()
    print "Finish"
  

if __name__ == "__main__":
  main()
