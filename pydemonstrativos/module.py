import pandas as pd
# pd.options.display.float_format = '{:,.2f}'.format
# pd.set_option('display.max_rows', 400)
# Essas confs precisam ser no pc do usuário, aqui só retorna dados
class CVM():
    def about():
        print("CVM - Demonstrativos Financeiros - Dados CVM")
    
    def create_links_api(init_year, last_year):
        year_List = lista_anos = [ano for ano in range(init_year, last_year+1)]

        arquivos_cvm = ['dfp_cia_aberta_DRE_con_{}.csv','dfp_cia_aberta_DFC_MI_con_{}.csv',
                        'dfp_cia_aberta_BPP_con_{}.csv','dfp_cia_aberta_BPA_con_{}.csv',
                        'dfp_cia_aberta_DRA_con_{}.csv', 'dfp_cia_aberta_DVA_con_{}.csv']
        
        links_gcloud_sem_data = []
        links_gcloud = []
        
        google_cloud_link = 'https://storage.googleapis.com/demonstrativosfinanceiros/{}'

        for arquivo in arquivos_cvm:
            links_gcloud_sem_data.append(google_cloud_link.format(arquivo))

        for link in links_gcloud_sem_data:
            for ano in lista_anos:
                links_gcloud.append(link.format(ano))

        return links_gcloud

    def create_dfp(demonstrativo, ano_analise, empresa, links_gcloud):
        link_dfp = [sentence for sentence in links_gcloud if all(w in sentence for w in [demonstrativo, str(ano_analise)])][0]
        dfp_dados_brutos = pd.read_csv(link_dfp, encoding='ISO-8859-1', sep=';')
        
        ultimo = dfp_dados_brutos.loc[dfp_dados_brutos['ORDEM_EXERC'] == 'ÚLTIMO']
        penultimo = dfp_dados_brutos.loc[dfp_dados_brutos['ORDEM_EXERC'] == 'PENÚLTIMO']

        ultimo_ano = ultimo['DT_FIM_EXERC'][1][:4]
        penultimo_ano = penultimo['DT_FIM_EXERC'][0][:4]

        ultimo = ultimo[['DENOM_CIA','CD_CONTA','DS_CONTA', 'VL_CONTA']]
        ultimo.columns = ['DENOM_CIA','CD_CONTA','DS_CONTA', ultimo_ano]

        penultimo = penultimo[['DENOM_CIA','CD_CONTA','DS_CONTA', 'VL_CONTA']]
        penultimo.columns = ['DENOM_CIA','CD_CONTA','DS_CONTA', penultimo_ano]

        dfp_geral = pd.merge(penultimo, ultimo)
        dfp_geral = dfp_geral.loc[dfp_geral['DENOM_CIA']==empresa]
        
        return dfp_geral
    
    def relatorio_empresa(dfp, ano, empresa, time_years=2): #Por padrão sempre será 2anos
        if time_years==2:
            return CVM.create_dfp(dfp, ano, empresa)
        elif time_years==4:
            return pd.merge(CVM.gerar_dfp(dfp, ano-2, empresa), CVM.gerar_dfp(dfp, ano, empresa))
        else:
            return ("ERROR: Só é gerado relatórios de 2 ou 4 anos de empresas, valores diferentes que isso não são válidos.")

    def listar_contas(demonstrativo):
        # O certo aqui seria retornar apernas demonstrativo['DS_CONTA'].unique() como uma lista e o usuário usar.
        for conta in demonstrativo['DS_CONTA'].unique():
            print(conta) #Não é boa prática usar um print em um pacote de função

    def retornar_conta(demonstrativo, conta):
        return demonstrativo.loc[demonstrativo['DS_CONTA'] == conta]

    def retornar_valores(demonstrativo, conta):
        return demonstrativo.loc[demonstrativo['DS_CONTA'] == conta].values[0][3:]
    
    def retornar_tabela(dfc1, conta1, dfc2, conta2):
        # Essa função aqui pode melhorar, está fazendo muitos fors desnecessários.
        a = CVM.retornar_conta(dfc1, conta1)
        a = a.iloc[:, lambda a: [2,3,4,5,6]]
        b = CVM.retornar_conta(dfc2, conta2)
        b = b.iloc[:, lambda b: [2,3,4,5,6]]
        c = pd.concat((a,b))
        return c
    
    def listar_empresas_ano(links_gcloud, ano):
        link_dfp = [sentence for sentence in links_gcloud if all(w in sentence for w in ['BPA', str(ano)])][0]
        dfp_dados_brutos = pd.read_csv(link_dfp, encoding='ISO-8859-1', sep=';')
        for empresa in dfp_dados_brutos['DENOM_CIA'].unique():
            print(empresa) #Não é boa prática usar um print em um pacote de função
            
    #Retornar tabela com duas contas e resultado divisao        
    def tabela_com_divisao_resultados(dfp1, conta1, dfp2, conta2, nome_divisao):
        a = CVM.retornar_tabela(dfp1, conta1,dfp2, conta2)
        primeiro_resultado = a.iloc[:, lambda a: [1,2,3,4]].iloc[0]
        segundo_resultado = a.iloc[:, lambda a: [1,2,3,4]].iloc[1]
        return pd.DataFrame(segundo_resultado/primeiro_resultado, columns=[[nome_divisao]]).T          