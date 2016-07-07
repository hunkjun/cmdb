from winservices.models import winconf
from salt.client import LocalClient
from asset.utils import logs,notification





class servicesPublish:
    def __init__(self,user,ip):
        self.user = user
        self.ip = ip
        self.obj = winconf.objects.all()
        self.salt = LocalClient()


    def deployServices(self,env,services):
        self.env = env
        self.services = services
        result = []
        obj = winconf.objects.filter(env=self.env).filter(servicename=self.services)
        for name in obj:

            
            stop = self.salt.cmd(name.hostname.saltname,'cmd.run',['net stop %s' % name.servicename])
            result.append(stop)
            update = self.salt.cmd(name.hostname.saltname,'cmd.run',['svn up %s --username=%s --password=%s' % (name.localpath,name.username,name.password)])
            result.append(update)
            start = self.salt.cmd(name.hostname.saltname,'cmd.run', ['net start %s' % name.servicename])
            result.append(start)

            action = 'deploy ' + name.servicename
            logs(self.user,self.ip,action,result)
            servicename = name.servicename.strip('"')
            notification(name.hostname.saltname,servicename,start,self.user)



        return result



