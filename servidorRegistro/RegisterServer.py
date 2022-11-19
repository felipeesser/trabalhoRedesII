from socketserver import *
from Connection import *
from address import *
from psycopg2 import DatabaseError

class RegisterServer(BaseRequestHandler):
  
  dbConnection = Connection('../servidorRegistro/credentials.json')

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
        self.request.sendall('inserido, {}'.format(name).encode('utf-8'))  
      
      elif command == 'listar_contatos':
        result = list(map(lambda x: x.toJson(), self.dbConnection.read_all()))
        self.request.sendall('resposta, {}'.format(result).encode('utf-8'))
        
      elif command == 'consulta':
        arguments = processedMessage[1:]
        if len(arguments) != 1: raise Exception('Insufficient number of arguments')
        name = arguments[0]
        endereco = self.dbConnection.read_by_name(name)
        if endereco.endIP != None: 
          self.request.sendall('resposta, {}'.format(endereco.toJson()).encode('utf-8'))
        else: self.request.sendall('resposta, nao_cadastrado'.encode('utf-8'))
      
      elif command == 'remocao':
        arguments = processedMessage[1:]
        if len(arguments) != 1: raise Exception('Insufficient number of arguments')
        name = arguments[0]
        endereco = self.dbConnection.delete_by_name(name)
        self.request.sendall('removido, {}'.format(name).encode('utf-8'))
        # else: self.request.sendall('resposta, nao_cadastrado'.encode('utf-8'))
      
      else: self.request.sendall('comando_desconhecido'.encode('utf-8'))
    
    except (Exception) as error:
      print('Error processing command: {}'.format(error))
      if isinstance(error, DatabaseError):
        if 'duplicate key' in str(error):
          self.request.sendall('ja_criado, {}'.format(name).encode('utf-8'))
      else:
        if str(error) == 'Insufficient number of arguments':
          self.request.sendall('argumentos_insuficientes'.encode('utf-8'))

if __name__ == '__main__':
  host, port = '0.0.0.0', 9999
  with TCPServer((host, port), RegisterServer) as server:
    server.serve_forever()