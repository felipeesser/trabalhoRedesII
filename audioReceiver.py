import socket
from audioStream import *

if __name__ == '__main__':
  inSocket = socket.socket(type=socket.SOCK_DGRAM) #socket udp
  inSocket.bind(('0.0.0.0', 4000))
  outStream = StreamManager.startStream(False)
  while True:
    data = inSocket.recv(StreamManager.CHUNK * 4)
    outStream.write(data)