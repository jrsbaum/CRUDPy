class Produto:
    def __init__(self, nome, preco, quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def toDBColletion(self):
        return {
            'name': self.nome,
            'prince': self.preco,
            'quantity': self.quantidade
        }