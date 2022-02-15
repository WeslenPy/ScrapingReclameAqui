#Category Company
from requests_html import HTMLSession
import json
from crud import CRUD


class CategoryGet:

    def __init__(self,save=False) -> None:
        #URL
        self.url = 'https://www.reclameaqui.com.br/categoria/'

        self.listCategory = []

    def getAllCategory(self):

        #Estabelecendo Conexão

        with HTMLSession() as Session:
            response  = Session.get(self.url)
            count= 0
            response.html.render(sleep=10,timeout=20)

            #Pegando todos os links contidos do HTML
            links = response.html.absolute_links
            for link in links:
                #Verificando se categoria está contido no link
                if 'categoria' in str(link).split('/'):
                    count +=1
                    category = str(link.split('/')[2])
                    if category != '':
                        #Adicionando a lista de categorias
                        self.listCategory.append(category)
            
                    print(category)
            print('Busca Encerrada!')

        #Criando um log das Categorias 
        with open('listCategory.txt','w') as t: 
            for c in self.listCategory: t.write(c+'\n')
        return self.listCategory
                    

class CompanyBot:

    def __init__(self,jsonFile:str='CompanyData.json'):

        #URL
        self.url = 'https://www.reclameaqui.com.br/categoria/'

        self.jsonCompany = {}
        self.jsonFile= jsonFile


    def jsonFileLoads(self):
        try:
            #Buscando por JSON
            with open(self.jsonFile,'r') as js:
                read = json.loads(js.read())
                if len(read) >100:
                    #Retornando o JSON
                    return read
                #Iniciando a busca por empresas caso não haja um JSON
                self.getCompany()
        except FileNotFoundError:
            #JSON não encontrado
            print(f'Arquivo {self.jsonFile} não encontrado!')
            #Inicando  a busca por empresas 
            self.getCompany()
        except json.decoder.JSONDecodeError:
            self.getCompany()
        except Exception as erro:
            print(erro)
            
    def getCompany(self):
        #Pegando todas as categorias 
        categorys = CategoryGet().getAllCategory()  

        with HTMLSession()  as Session:
        
            for category in categorys:
                
                response = Session.get(self.url+category)
                response.html.render(sleep=10,timeout=20)
                self.jsonCompany[category] = []
                #Pegando todos os links do HTML
                for link in response.html.absolute_links:
                    #Verificando se empresa está contigo no link
                    if 'empresa' in str(link).split('/'):
                        company = str(link.split('/')[-1])
                        if company != '':
                            print(company,'FOUND')
                            #Adicionando a empresa a sua categoria 
                            self.jsonCompany[category].append(company)
        #Gerando o JSON 
        with open('CompanyData.json','w') as c: json.dump(self.jsonCompany,c,indent=4)

if __name__ == '__main__':
    CRUD()
    #Inicializando o Carrregamento do JSON
    CompanyBot().jsonFileLoads()
