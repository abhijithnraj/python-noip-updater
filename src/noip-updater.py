# Import the abc module for abstract base classes
import abc
from ip_address.ip_locator import ISPDetector,IPAPIStrategy
# Define an abstract class for the subject
class Subject(abc.ABC):

    # Initialize the list of observers
    def __init__(self):
        self.observers = []

    # Register an observer to the subject
    def attach(self, observer):
        self.observers.append(observer)

    # Unregister an observer from the subject
    def detach(self, observer):
        self.observers.remove(observer)

    # Notify all the observers about a change in the subject
    def notify(self):
        for observer in self.observers:
            observer.update(self)

# Define an abstract class for the observer
class Observer(abc.ABC):

    # Define an abstract method for updating the observer
    @abc.abstractmethod
    def update(self, subject):
        pass


class InternetServiceProvider(abc.ABC):
    @abc.abstractmethod
    def getName(self)->str:
        pass
    @abc.abstractmethod
    def isValidforNoIp(self)->bool:
        pass
        
class BsnlISP(InternetServiceProvider):

    def getName(self)->str:
        return "Bharat Sanchar Nigam Ltd"
    def isValidforNoIp(self)->bool:
        return True

class ActISP(InternetServiceProvider):

    def getName(self)->str:
        return "Beam Telecom Pvt Ltd"
    def isValidforNoIp(self)->bool:
        return False

# Define a concrete class for the subject that checks whether an API is alive
class ISPStatusChecker(Subject):

    def __init__(self,service_providers:list[InternetServiceProvider]):
        super().__init__()
        self.ip = None
        self.valid_service_providers = list(filter(lambda x : x.isValidforNoIp() ,service_providers))
        assert(len(self.valid_service_providers)!=0)
        print(self.valid_service_providers)
        self.isp_detector = ISPDetector(IPAPIStrategy())
        print(self.isp_detector.get_provider())
        print(self.isp_detector.get_ip())


    def is_valid_provider(self,isp:str)->bool:
        for i in self.valid_service_providers:
            print(i.getName())
            if(i.getName().strip() == isp.strip()):
                return True
        return False
        
    # Check the API status and notify the observers if it changes
    def check_status(self):
        isp = self.isp_detector.get_provider()
        ip = self.isp_detector.get_ip()
        if(isp==None):
            return
        print("ISP: ",isp)
        if(self.is_valid_provider(isp)):
            if(ip!=self.ip):
                print(f"IP Change required. Current ip = {self.ip}, New IP = {ip}")
                self.ip = ip
                self.notify()
        else:
            return


from noip import NoIp
class NoIPUpdater(Observer):
    def __init__(self,hostname,username,password):
        self.dynDns = NoIp.DynDns()
        self.dynDns.setHostName(hostname)
        self.dynDns.setAuth(username,password)
    def update(self,subject):
        print("NOIP UPDATER: Trying to set the New IP")
        status = self.dynDns.update(subject.ip)
        if(status == 0):
            print("Success!")
        else:
            dynDnsStatus = NoIp.DynDnsStatus()
            if(dynDnsStatus.statusToString(status) != "NO CHANGE"):
                print("Error occurred")
                print(dynDnsStatus.statusToString(status))
               

hostname = ""
username = ""
password = ""
from credentials import * 
service_providers_list = [BsnlISP(),ActISP()]
isp_status_checker = ISPStatusChecker(service_providers_list)

noip_updater = NoIPUpdater(hostname,username,password)
isp_status_checker.attach(noip_updater)
import time
while True:
    isp_status_checker.check_status()
    time.sleep(1)