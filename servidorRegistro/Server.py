from socketserver import *
from Connection import *

class RegisterServer(BaseRequestHandler):

  def __init__(self, request, client_address, server: BaseServer) -> None:
    super().__init__(request, client_address, server)
    self.dbConnection = Connection('servidorRegistro/credentials.json')
    self.dbConnection.create_table()

  def handle(self):
    self.data = self.request.recv(1024).strip()
    print("{} wrote:".format(self.client_address[0]))
    print(str(self.data)[1:].strip('\''))
    # just send back the same data, but upper-cased
    # self.request.sendall(self.data.upper())

if __name__ == '__main__':
  host, port = '0.0.0.0', 9999
  with TCPServer((host, port), RegisterServer) as server:
    server.serve_forever()