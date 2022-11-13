from socketserver import *
from Connection import *
from address import *
from psycopg2 import DatabaseError

class RegisterServer(BaseRequestHandler):

  
  dbConnection = Connection('servidorRegistro/credentials.json')

  def __init__(self, request, client_address, server: BaseServer) -> None:
    super().__init__(request, client_address, server)
    self.dbConnection.create_table()

  def handle(self):
    data = self.request.recv(1024).strip()
    print("{} wrote:".format(self.client_address[0]))
    message = data.decode('utf-8')
    processedMessage = message.split(', ')
    try:
      command = processedMessage[0]
      if command == 'registro':
        arguments = processedMessage[1:]
        if len(arguments) != 3: raise Exception('Insufficient number of arguments')
        name, address, port = arguments[0], arguments[1], arguments[2]
        self.dbConnection.insert(Address(name, address, port))
        self.request.sendall('confirmacao, {}'.format(name).encode('utf-8'))  
      
    except (Exception) as error:
      print('Error processing command: {}'.format(error))
      if isinstance(error, DatabaseError) and 'duplicate key' in str(error):
        self.request.sendall('ja_criado, {}'.format(name).encode('utf-8'))

    print(message)
    # just send back the same data, but upper-cased
    # self.request.sendall(self.data.upper())

if __name__ == '__main__':
  host, port = '0.0.0.0', 9999
  with TCPServer((host, port), RegisterServer) as server:
    server.serve_forever()