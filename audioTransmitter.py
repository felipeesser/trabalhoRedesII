import socket
from audioStream import *

if __name__ == '__main__':
  inSocket = socket.socket(type=socket.SOCK_DGRAM)
  inStream = StreamManager.startStream(True)
  while True:
    data = inStream.read(StreamManager.CHUNK)
    print('Buffer size: {}'.format(len(data)))
    inSocket.sendto(data, ('127.0.0.1', 4000))
