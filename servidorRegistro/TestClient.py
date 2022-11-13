from socket import *

class TestClient:

  def __init__(self):
    self.tcpSocket = socket(AF_INET, SOCK_STREAM)
    self.tcpSocket.bind(('0.0.0.0', 5000))

  def sendMessage(self, address):
    self.tcpSocket.connect(address)
    self.tcpSocket.send(b'Olar')
    self.tcpSocket.close()
  
if __name__ == '__main__':
  testClient = TestClient()
  testClient.sendMessage(('127.0.0.1', 9999))
  