from models import Client
import subprocess
import json


clients = Client.select()
for client in clients:
  for info in client.get_infos :
    try : 
      subprocess.call(["python", "analytics.py", "--siteid="+str(client.site_id), "--metrics="+info.infos.metrics,"--dimensions="+info.infos.dimensions ])
    except : 
      subprocess.call(["python", "analytics.py", "--siteid="+str(client.site_id), "--metrics="+info.infos.metrics])
