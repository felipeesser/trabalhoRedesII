import json
class Address():
    def __init__(self,nome,endIP,porta):
        self.nome=nome
        self.endIP=endIP
        self.porta=porta

    def toString(self):
        if self.nome and self.porta and self.endIP:
            return '{ ' + 'nome: {}, endIP: {}, porta: {}'.format(self.nome.strip(), self.endIP.strip(), self.porta.strip()) + ' }'
        else:
            print('Objeto vazio')

    def toJson(self):
        if self.nome and self.porta and self.endIP:
            return json.dumps(dict(nome=self.nome.strip(), endIp=self.endIP.strip(), porta=self.porta.strip()))
        else:
            print('Objeto vazio')

