class Endereco():
    def __init__(self,nome,endIP,porta):
        self.nome=nome
        self.endIP=endIP
        self.porta=porta

    def tostring(self):
        if self.nome and self.porta and self.endIP:
            print(self.nome,self.endIP,self.porta)
        else:
            print('Objeto vazio')

