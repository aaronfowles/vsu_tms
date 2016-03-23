#!/usr/bin/python

import sys
import requests

if __name__=='__main__':
    client = requests.session()
    
    app_url = 'http://178.62.111.80:8001/app/login/'

    csrftoken = client.get(app_url).cookies['csrftoken']
    prev_url = str(app_url)
    app_url = 'http://178.62.111.80:8001/app/create_task_list/'


    r = client.get(app_url,data={'csrfmiddlewaretoken':csrftoken},headers=dict(Referer=prev_url))
    print(r.status_code)
