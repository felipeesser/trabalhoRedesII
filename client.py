from audioStream import *
import socket

class Client:

  def __init__(self, port):
    self.inStream = StreamManager.startStream(isInput=True)
    self.outStream = StreamManager.startStream(isInput=False)
    self.audioInputSocket = socket.socket(type=socket.SOCK_DGRAM)
    self.audioOutputSocket = socket.socket(type=socket.SOCK_DGRAM)
    self.audioInputSocket.bind(('0.0.0.0', port + 50))
    self.audioOutputSocket.bind(('0.0.0.0', port))
  
  def operateCall(self, receivingAddress):
    while True:
      outgoingData = self.inStream.read(StreamManager.CHUNK)
      self.audioInputSocket.sendto(outgoingData, receivingAddress)
      incomingData = self.audioOutputSocket.recv(StreamManager.CHUNK*2)
      self.outStream.write(incomingData)
      
if __name__ == '__main__':
  client = Client(4000)
  client.operateCall(('127.0.0.1', 4000))
  
