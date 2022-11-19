from socket import *
from callManager import CallManager

class CallServer:
  
  def __init__(self, ipAddress, port):
    self.inSocket = socket((ipAddress, port), SOCK_DGRAM)
    self.outSocket = socket((ipAddress, port + 1), SOCK_DGRAM)
  
