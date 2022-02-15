from headers import header,headerSecondary
from json.decoder import JSONDecodeError
from scrappingCC import CompanyBot
from threading import Thread
from crud import CRUD
import requests
import csv


class ThreadCRUD(Thread):
    def __init__(self,**kwargs):
        super().__init__()
        self.data = kwargs

    def run(self):

        print(f'Reclamação {self.data["id"]} inserida, company {self.data["Company"]}!\n')

        #Insere a nova reclamção no Banco de Dados SQL
        CRUD.Insert("INSERT OR IGNORE INTO Complaint(id,Title,Company,Local,Date,Complaint,Status) VALUES (?,?,?,?,?,?,?)",
                    insert=(self.data['id'],self.data['Title'],self.data['Company'],self.data['Local'],self.data['Date'],self.data['Complaint'],self.data['Status'],))



class ScrapingAPI:
    def __init__(self,header:dict,hearderSecondary:dict,searchName:str=None,limitComplaint:int=100,maxError:int=5,Session:bool=False):

        #define headers

        self.header = header
        self.headerSecondary = hearderSecondary

        # define variables

        self.companys = CompanyBot().jsonFileLoads()
        self.limitComplaint = limitComplaint
        self.maxError = maxError
        self.enableSession = Session
        self.indexProxies = 0
        self.logError = 0
        self.company = ''
        self.session =0
        self.proxies = []

        #urls api

        self.apiCompany = f'https://iosite.reclameaqui.com.br/raichu-io-site-v1/company/shortname/'
        self.api = f'https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/10/'
        self.endpoint = '?company='

        #start functions
        self.loadProxys()
        if self.enableSession: self.sessionRecovery()

        if type(searchName) ==str:
            self.getIdCompany(searchName)
            
        elif type(searchName) in [list,tuple]:
            for _id in searchName:
                self.getIdCompany(_id)
        else:
            self.companyJson()


    def sessionRecovery(self):
        try:
            #Carrega o logSession
            with open('logSession.csv','r') as s: self.session = len(list(csv.reader(s,delimiter=',')))
        except FileNotFoundError:
            #Define o logSession como não encontrado
            self.enableSession = False
            print('Arquivo logSession.csv não encontrado!')
    #loading proxys 
    def loadProxys(self,proxiesFile:str='proxys.txt'):
        #Carrega os proxies
        with open(proxiesFile,'r') as px:
            for line in px.readlines():
                #Adicionando todos os proxies a uma lista
                self.proxies.append({'http':'http://'+line.replace('\n','')})

    #Json Name Company start
    def companyJson(self):

        countSession = 0
        #Percorrendo as chaves do JSON
        for cp in self.companys:
            #Usando as chaves para acessar a mesma
            for c in self.companys[cp]:
                #Verificando se é possivel reaver a sessão
                if self.enableSession and self.session !=0:
                    countSession+=1
                    if countSession == self.session:
                        self.enableSession = False
                else:
                    self.company = c
                    #Pegando o ID da empresa
                    self.getIdCompany(c)

    #get ID the Company

    def getIdCompany(self,comp):    

        #API de busca
        api = str(self.apiCompany+comp)

        try:
            #Request GET para a API
            response = requests.get(api,headers=self.headerSecondary)
            break_point = False
            #Verificando o status code
            if str(response.status_code) =='200':
                r = response.json() 
                #Acessando a quantidade de Reclamações e Verificando o valor Padrão
                limit =  int(r['panels'][0]['index']['totalComplains']) if self.limitComplaint == 100 else self.limitComplaint

                if limit <10:limit = 0

                #Iniciando um loop para a quantidade de Reclamações
                for page in range(0,limit,10):
                    #Iniciando o logError como zero
                    self.logError =0
                    #Pegando os dados da API
                    if not self.getData(r['id'],page):
                        #Salvando a sessão
                        self.sessionSave(comp,r['id'],'NOT_FOUND')
                        break
                    else:
                        break_point = True

                #Salvando a sessão
                if break_point:self.sessionSave(comp,r['id'],'FOUND')

        #Tratamento de Exceções 
        except requests.exceptions.SSLError:pass
        except TimeoutError:print('Tempo Esgotado!')
        except Exception as error:print('ERROR:',error)

    #get Json data    
    def getData(self,_id,page):

        #API DATA COMPANY
        api = str(self.api+str(page)+self.endpoint+str(_id))
        print(_id)

        try:
            resp = requests.get(api,headers=self.header,proxies=self.proxies[self.indexProxies],timeout=5)
            #Acessando as Reclamações referentes a Empresa
            data = resp.json()['complainResult']['complains']['data']
            if data !=[]:
                for i in data:

                    #Criando um Objeto com os dados da API
                    js ={'Title':i['title'],'Local':f"{i['userCity']}-{i['userState']}",'id':i['legacyId'],'Date':i['created'],
                        'Complaint':i['description'],'Status':i['status'],'Company':i['companyName']}
                    
                    #Iniciando uma Thread
                    th = ThreadCRUD(**js)
                    th.start()

                    print(str(page)[:-1],'-',i['companyName'])


        #Tratamento de Exceções
        except JSONDecodeError:
            # print(self.company,'- Not Found Json:',str(page)[:-1])
            self.indexProxies+=1
            self.logError +=1

            if self.indexProxies >=len(self.proxies):
                self.indexProxies = 0

            if self.logError >self.maxError:
                return False

        except TimeoutError:
            print('Tempo esgotado!')

        except Exception as erro:
            #LOG DE ERRO
            with open('log.txt','a') as  log:
                log.write(str(erro)+'\n')
                log.write(str(data)+'\n')

        return True

    def sessionSave(self,comp,_id,_type):
        #Salvando Sessão
        if self.session <= 0: self.session = 1
        if self.session or self.enableSession:
            with open('logSession.csv','a',newline='') as s: csv.writer(s).writerows([[comp,_id,_type]])


if __name__ =='__main__':
    CRUD()
    listSearchCompany = ['vivo-celular-fixo-internet-tv']
    ScrapingAPI(header,headerSecondary,searchName=listSearchCompany,maxError=100,Session=True)