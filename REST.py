from cmath import log
import json
import requests
from credentials import *
from prettytable import PrettyTable  
requests.packages.urllib3.disable_warnings()

  
class SDWAN:
    def __init__(self, vmanage_ip, username, password):
        self.vmanage_ip = vmanage_ip
        self.conn = self.login(username, password)  

    def login(self,username,password):
        jessionid = f'https://{self.vmanage_ip}:8443/'+'j_security_check'
        vManage_Token = f'https://{self.vmanage_ip}:8443/'+'dataservice/client/token'
        login = {'j_username' : username, 'j_password' : password}
        conn = requests.session()
        conn.post(url=jessionid, data=login, verify=False)
        conn.headers['X-XSRF-TOKEN'] = conn.get(url=vManage_Token, verify=False).text
        return conn

    def get(self,url_api):  
        response = self.conn .get(url = f'https://{self.vmanage_ip}:8443/dataservice'+url_api, verify=False)
        return json.loads(response.content)

    def devices(self):
        devices = self.get('/device')
        x = PrettyTable()
        x.field_names = ["Device Name", "System-IP", "reacheable",'certificate', "device model", "version", 'uuid']
        x.title = 'SDWAN Routers'
        c = PrettyTable()
        c.field_names = ["Device Name", "System-IP", "reacheable",'certificate', "device model", "version", 'uuid']
        c.title = 'Controllers'
        for i in devices['data']:
            if i['personality'] == 'vedge':
                x.add_row([i['host-name'], i['system-ip'], i['reachability'], i['certificate-validity'],i['device-model'], i['version'], i['uuid']])
            else:
                c.add_row([i['host-name'], i['system-ip'], i['reachability'], i['certificate-validity'],i['device-model'], i['version'], i['uuid']])
        return c, x

SDWAN_API = SDWAN(cvmanage_ip, cusername, cpassword)


#/device - list devices




SDWAN_API.devices()