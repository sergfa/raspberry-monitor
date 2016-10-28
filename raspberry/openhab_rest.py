
import requests, base64

class OpenhabRestHelper:

    def __init__(self, openhab_host, openhab_port, username, password):
        
         self.openhab_host = openhab_host
         self.openhab_port = openhab_port
         self.username = username
         self.password = password
         self.auth = base64.encodestring(('%s:%s' % (self.username, self.password)).encode()).decode().replace('\n', '')
     
    def post_command(self, key, value):
        """ Post a command to OpenHAB - key is item, value is command """
        url = 'http://%s:%s/rest/items/%s'%(self.openhab_host, self.openhab_port, key)
        req = requests.post(url, data=value, headers=self.basic_header())
        if req.status_code != requests.codes.ok:
            req.raise_for_status()    
            
    def put_status(self, key, value):
       """ Put a status update to OpenHAB  key is item, value is state """
       url = 'http://%s:%s/rest/items/%s/state'%(self.openhab_host, self.openhab_port, key)
       req = requests.put(url, data=value, headers=self.basic_header())
       if req.status_code != requests.codes.ok:
           req.raise_for_status()
           
    def basic_header(self):
        """ Header for OpenHAB REST request - standard """
        return {
            "Authorization" : "Basic %s" %self.auth,
            "Content-type": "text/plain"}
def test():
    openhab = OpenhabRestHelper("localhost", "8080", "test", "test")
    openhab.put_status("test", True)

