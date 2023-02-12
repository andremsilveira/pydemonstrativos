import pandas as pd

class CVM():
    ''' Class for CVM functions '''
    def __init__(self):
        pd.options.display.float_format = '{:,.2f}'.format
        pd.set_option('display.max_rows', 400)
        
        self.ano_inicio = 2012
        self.ano_termino = 2021

        self.arquivos_cvm = ['dfp_cia_aberta_DRE_con_{}.csv','dfp_cia_aberta_DFC_MI_con_{}.csv',
                        'dfp_cia_aberta_BPP_con_{}.csv','dfp_cia_aberta_BPA_con_{}.csv',
                        'dfp_cia_aberta_DRA_con_{}.csv', 'dfp_cia_aberta_DVA_con_{}.csv']

        #Criar lista com anos - ano inicio até ano fim.

        self.lista_anos = []

        while self.ano_inicio <= self.ano_termino:
            self.lista_anos.append(self.ano_inicio)
            self.ano_inicio += 1

            
        #Criação de links para download
        #Link Google Cloud onde estao os arquivos armazenados
        self.google_cloud_link = 'https://storage.googleapis.com/demonstrativosfinanceiros/{}'


        #Criação do link de acordo com os anos.
        self.links_gcloud_sem_data = []
        self.links_gcloud = []

        for arquivo in self.arquivos_cvm:
            self.links_gcloud_sem_data.append(self.google_cloud_link.format(arquivo))
            
        for link in self.links_gcloud_sem_data:
            for ano in self.lista_anos:
                self.links_gcloud.append(link.format(ano))

            
    #FUNÇÕES - GERAÇÃO DE RELATÓRIO        
            
    def gerar_dfp(self, demonstrativo, ano_analise, empresa):
        link_dfp = [sentence for sentence in self.links_gcloud if all(w in sentence for w in [demonstrativo, str(ano_analise)])][0]
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

    def relatorio_2anos_empresa(dfp, ano, empresa):
        dfp_gerado = CVM.gerar_dfp(dfp, ano, empresa)
        return dfp_gerado

    def relatorio_4anos_empresa(dfp, ano, empresa):
        dfp_gerado1 = CVM.gerar_dfp(dfp, ano-2, empresa)
        dfp_gerado = CVM.gerar_dfp(dfp, ano, empresa)
        dfp_geral = pd.merge(dfp_gerado1, dfp_gerado)
        return dfp_geral

    #Listar contas
    def listar_contas(demonstrativo):
        for conta in demonstrativo['DS_CONTA'].unique():
            print(conta)

    #retornar dados conta
    def retornar_conta(demonstrativo, conta):
        return demonstrativo.loc[demonstrativo['DS_CONTA'] == conta]

    #retornar dados conta
    def retornar_valores(demonstrativo, conta):
        a = demonstrativo.loc[demonstrativo['DS_CONTA'] == conta]
        return a.values[0][3:]

    #Retornar Tabela com 2 contas
    def retornar_tabela(dfc1, conta1, dfc2, conta2):
        a = CVM.retornar_conta(dfc1, conta1)
        a = a.iloc[:, lambda a: [2,3,4,5,6]]
        b = CVM.retornar_conta(dfc2, conta2)
        b = b.iloc[:, lambda b: [2,3,4,5,6]]
        c = pd.concat((a,b))
        return c

    #Listar total de empresas listadas por Ano
    def listar_empresas_ano(self, ano):
        link_dfp = [sentence for sentence in self.links_gcloud if all(w in sentence for w in ['BPA', str(ano)])][0]
        dfp_dados_brutos = pd.read_csv(link_dfp, encoding='ISO-8859-1', sep=';')
        for empresa in dfp_dados_brutos['DENOM_CIA'].unique():
            print(empresa)
            
    #Retornar tabela com duas contas e resultado divisao        
    def tabela_com_divisao_resultados(self, dfp1, conta1, dfp2, conta2, nome_divisao):
        a = self.retornar_tabela(dfp1, conta1,dfp2, conta2)
        primeiro_resultado = a.iloc[:, lambda a: [1,2,3,4]].iloc[0]
        segundo_resultado = a.iloc[:, lambda a: [1,2,3,4]].iloc[1]
        return pd.DataFrame(segundo_resultado/primeiro_resultado, columns=[[nome_divisao]]).T          