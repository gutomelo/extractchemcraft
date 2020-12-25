# Tentando abrir o arquivo para análise de dados
try:
    arquivo = input("\nDigite o nome do arquivo:")
    # Abrindo o arquivo para leitura
    arq1 = open(arquivo, "r", encoding='utf8')

except IOError:
    print('Arquivo não encontrado, favor digitá-lo corretamente!')
    exit()

# Retornando ao início da linha do arquivo
arq1.seek(0)

# Armazenando aquivo numa variável
data_arq1 = arq1.read()

# Localizando texto de início de extração
d_inicio = data_arq1.find(' Total nuclear spin-spin coupling J (Hz): ')+43
#print(d_inicio)

# Localizando texto do final da extração
d_final = data_arq1.find('End of Minotr F.D. properties file',d_inicio,len(data_arq1))-2
#print(d_final)

# Salva os dados coletados
dados_coletados = data_arq1[d_inicio:d_final]
#print(dados_coletados)

# Removendo os espaços e esplitando por linha
data_arq2 = dados_coletados
data_arq2 = data_arq2.replace(' \n', ',#\n')
data_arq2 = data_arq2.replace(' -', ',-')
data_arq2 = data_arq2.replace('     ', '')
data_arq2 = data_arq2.replace('  ', ',')
data_arq2 = data_arq2.replace(' ', '')
#print(data_arq2)

# Agora esplitando por vírgula
data_split = data_arq2.split('\n')
#print(data_split)
full_data = []
for row in data_split:
    split_row = row.split("\n")
    split2=[]
    for i in split_row:
        split2 = i.split(",")
        full_data.append(split2)
#print(full_data) 

# Imprimindo o último dado bruto
for i in full_data:
    print(i)
    
# Abrindo e gravando o arquivo de log
with open(arquivo+'_log.txt','w') as arquivo:
    for i in full_data:
        arquivo.write(str(i)+'\n')
        
# ------------------ Função para localizar o elemnto segundo a coluna e linha
def funcao_calc(coluna,linha):
    try: 
        end_linha = 0
        end_coluna = 0
        valor = ''
        b_col = False
        b_lin = False
        
        #Procurando a coluna
        for i in full_data:
            for z in i:
                if z == coluna and '#' in i:
                    print('Coluna:',i)
                    end_coluna = i.index(z)          # Endereço da coluna            
                    end_linha = full_data.index(i)   # Endereço da linha da coluna
                    b_col = True
               
        #Procurando a linha
        for i in full_data:
            if full_data.index(i) > end_linha:
                if '#' in i:                         # Se encontrar a proxima linha de colunas encerra a procura
                        break
                elif i[0] == linha:                  # Se localinzar a linha solicitada
                    print('Linha',i)
                    valor = i[end_coluna+1]
                    b_lin = True
        
        if b_col and b_lin:                          # Só retorna valor se encontrar colune e linha
            return valor
        else:
            print('Coluna ou linha não encontrada!')
    
    except IndexError:
        print ("Erro: O valor solicitado não pertence a linha correspendente!")
    else:
        print ("Erro: O valor solicitado não pode ser encontrado na tabela!")    

# ------------------ Função para calcular a lista de elementos
def funcao_list(list_res):
    lista = list_res.split(",")
        
    if len(lista) % 2 != 0:
        return print('A lista de valores estão incompletos, favor preencher corretamente!')
    else:
        result_geral = []
        
        for i in lista:
            if lista.index(i) % 2 ==0:
                print('\nColuna:', i)
                print('Linha:', lista[lista.index(i)+1])
                
                result = funcao_calc(i,lista[lista.index(i)+1]) 
                if result:
                    val_final = func_convert(result)
                    print('O elemento encontrado foi:', result,'\n-->>' , val_final)
                    result_geral.append(val_final)
                else:
                    print('Os valores digitados não estão corretos, favor verificar!')
                    break

        
        print('\nA lista de valores encontrados foram:')
        for i in result_geral:
            print(i, end = " ")
        print('')  

# ------------------ Função que converte a string em valor decimal
def func_convert(string):
    try:
        valor_s = float(string[:-4])
        base = int(string[-2:])
        sinal_base = string[-3]

        if sinal_base == '+':
            return round(valor_s * 10 ** base,len(string[:-4]))
        elif sinal_base == '-':
            return round(valor_s * 1/(10 ** base),len(string[:-4]))

    except ValueError:
        print ("Erro: O valor não pode ser convertido!")
    else:
        print ("Erro: O valor não pode ser convertido!")


# ------------------ Função para entrada de dados
def Inputs():
    while True:
        try:
            val1 = input("\nDigite os valores de coluna e linha separado por vírgula:\n")
            if val1 == 'exit':
                print('Você decidiu sair, até mais, Obrigado!')
                exit()
            
            
        finally:
            if val1 == 'exit':
                exit()

            funcao_list(val1)
            

# CHAMANDO OS INPUTS PARA ENTRADA DE DADOS!
Inputs()