import socket
from audioStream import *

if __name__ == '__main__':
  inSocket = socket.socket(type=socket.SOCK_DGRAM)
  inStream = StreamManager.startStream(True)
  # inSocket.bind(('0.0.0.0', 4000)) # descomentar se quiser transmitir para outro IP
  ip = '127.0.0.1'
  while True:
    data = inStream.read(StreamManager.CHUNK)
    print('Buffer size: {}'.format(len(data)))
    inSocket.sendto(data, (ip, 4000))
