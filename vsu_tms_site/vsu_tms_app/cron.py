#!/usr/bin/python

import sys
import requests

if __name__=='__main__':
    client = requests.session()

    host = 'http://178.62.111.80'
    port = ':8001/app/'
    
    app_url = host + port + 'login/'

    csrftoken = client.get(app_url).cookies['csrftoken']
    prev_url = str(app_url)
    app_url = host + port + 'create_task_list/'

    r = client.get(app_url,data={'csrfmiddlewaretoken':csrftoken},headers=dict(Referer=prev_url))
    print(r.status_code)
