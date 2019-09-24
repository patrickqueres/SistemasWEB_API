# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 21:36:42 2019

@author: patri
"""

import os
import json, requests
import pandas as pd

LIMPAR = "clear"

def buscarSIAFI():
    # Leitura das variaveis
    print ("--------------------------------------")
    print ("## PORTAL TRANSPARÊNCIA - Busca do código do órgão (SIAFI) ##")
    descricao = input('Digite a descrição: ')
    
    paginas = 5 # define o numero maximo de paginas
    df_sigla = pd.DataFrame() # inicializa o dataframe
    
    ### Gerando a consulta
    # gera a URL
    for pag_atual in range(1,int(paginas),1):
        url = "http://www.transparencia.gov.br/api-de-dados/orgaos-siafi?descricao=" + descricao + "&pagina=" + str(pag_atual)
        response = requests.get(url)
        dados_json = json.loads(response.content)
        df = pd.io.json.json_normalize(dados_json)
        df.columns
        df_sigla = [df_sigla, df]
        df_sigla = pd.concat(df_sigla)
        
    if df_sigla.empty:
        print ("A consulta não retornou resultados. Verifique os parâmetros.")
    else:
        print (df_sigla)
        codigo = int(input('Digite o numero do index desejado: '))
        codigoOrgao_s = (df_sigla.iloc[codigo][0])
        print ("A sigla da " + df_sigla.iloc[codigo][2] + " foi armazenada.")
        return codigoOrgao_s
    
    
def buscarViagens(codigoOrgao):
    '''
    # Le as variaveis
    data_ida_inicial = input('Digite a data de ida inicial: ')
    data_ida_final = input('Digite a data de ida final: ')
    data_volta_inicial = input('Digite a data de volta inicial: ')
    data_volta_final = input('Digite a data de volta final: ')
    codigoOrgao = input('Digite o código do órgão (SIAFI): ')
    '''
    # POUPA TEMPO!
    mesano = input('Digite mês/ano (ex: 03/2019): ')
    data_ida_inicial = "01/"+mesano
    data_ida_final = "31/"+mesano
    data_volta_inicial = "01/"+mesano
    data_volta_final = "31/"+mesano
    #codigoOrgao = "26236" # uff 26236
    
    
    paginas = 20 # quantidade maxima de páginas a pesquisar
    df_principal = pd.DataFrame() # inicializa o dataframe vazio
    
    ### Gerando 
    
    # gera a URL
    for pag_atual in range(1,int(paginas),1):
        url = "http://www.transparencia.gov.br/api-de-dados/viagens?dataIdaDe=" + data_ida_inicial.replace('/', '%2F') + "&dataIdaAte=" + data_ida_final.replace('/', '%2F') + "&dataRetornoDe=" + data_volta_inicial.replace('/', '%2F') + "&dataRetornoAte=" + data_volta_final.replace('/', '%2F') + "&codigoOrgao=" + codigoOrgao + "&pagina=" + str(pag_atual)
        response = requests.get(url)
        dados_json = json.loads(response.content)
        df = pd.io.json.json_normalize(dados_json)
        df.columns
        df_principal = [df_principal, df]
        df_principal = pd.concat(df_principal)
    
    
    if df_principal.empty:
        print ("A consulta não retornou resultados. Verifique os parâmetros.")
    else:
        local_do_csv = 'viagens.csv'
        df_principal.to_csv (local_do_csv, index=True, header=True, encoding="utf-8", sep=";")
        print ("A consulta foi salva no arquivo " + local_do_csv)


def main():
    
    codigoOrgao = 0
    opcao = -1
    while opcao != 6:
        os.system(LIMPAR)
        print ("--------------------------------------")
        print ("PORTAL TRANSPARÊNCIA - Busca de Viagens a serviço")
        print ("1. Buscar código do órgão (SIAFI)")
        print ("2. Executar API")
        		
        print ("6. Sair")
        opcao = int(input("\nEscolha uma opção: "))
        
        if opcao==1:
            codigoOrgao = buscarSIAFI()
        
        if opcao==2:
            if codigoOrgao == 0:
                codigoOrgao = buscarSIAFI()
            else: 
                buscarViagens(codigoOrgao)
        
        if opcao==6:
            break;
            

main()