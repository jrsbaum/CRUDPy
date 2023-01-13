from pymongo import MongoClient
import certifi


MONGODB_URL = 'mongodb+srv://dbUserJrs:<password>@cluster0.23sjuth.mongodb.net/?retryWrites=true&w=majority'
cert = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGODB_URL, tlsCAFile=cert)
        db = client["dbb_produtos_app"]
    except ConnectionError:
        print('Erro de conexao com o banco de dados')
    return db


