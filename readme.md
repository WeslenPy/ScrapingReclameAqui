
# Scraping Reclame Aqui

# Overview

Este pequeno programa faz requisições síncronas a API do Reclame Aqui,
contando com 166 proxies para mascarar sua rota, dificultando a identificação e bloqueio do IP,
usando o tunelamento por proxy.

# Requirements

Python 3.7+

fake-useragent==0.1.11
requests-html==0.10.0
requests==2.11.1


# Mode of Use

ScrapingAPI(header,headerSecondary,limitComplaint=100,maxError=5,Session=True)

Os dois primeiros parâmetros são os headers, sendo relativos a cada API.

===
    Parâmetros opcionais
        maxError, Session e limitComplaint
===

Passando o parâmetro maxError você define um limite máximo de erros referente as requisições,
após o limite máximo ser excedido, a próxima requisição é feita.(Passando para a próxima empresa)

Usando o parâmetro Session você salva a sessão na qual parou, podendo continuar na próxima vez
que executar o script.

Utilizando o parâmetro limitComplaint você define a quantidade que você deseja de reclamações por empresa.(Será referente as páginas)

searchName é usado como um filtro, para buscar apenas por empresas especificas, podendo ser passada como uma lista ou uma única string.