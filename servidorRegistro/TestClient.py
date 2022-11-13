from socket import *

class TestClient:

  def sendMessage(self, address, message):
    serverSocket = create_connection(address)
    serverSocket.send(message)
    data = serverSocket.recv(1024)
    print('data: {}'.format(data.decode('utf-8')))
  
if __name__ == '__main__':
  testClient = TestClient()
  # testClient.sendMessage(('127.0.0.1', 9999), 'registro, maria, 127.0.0.1, 9001'.encode('utf-8'))
  # testClient.sendMessage(('127.0.0.1', 9999), 'consulta, maria'.encode('utf-8'))
  testClient.sendMessage(('127.0.0.1', 9999), 'remocao, maria'.encode('utf-8'))
