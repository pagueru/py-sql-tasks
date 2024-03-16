#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

# Importação de bibliotecas atrás do __init__.py
from __init__ import *

# Importa as funcionalidades padrões do projeto
from utils.utils import *

# Limpa o terminal
limpar_terminal(True)

# Define se deve mostrar o log de execução das funções
logger_execucao_funcao = 'info'

# Configura o logger
logger = configurar_logger(__name__, logger_execucao_funcao)

# Define a mensagem de nivel de logger
logger_manual(logging.getLevelName(logger.level))

# Configura o arquivo de log
configurar_arquivo_log()

# Obtém o nome do script
nome_script = Path(__file__).name

# Obtém o diretório completo do script com o nome do arquivo .py
diretorio_completo_script_arquivo = Path(__file__).parent

# Obtém o diretório da pasta do script
diretorio_pasta_script = Path(__file__).parent.parent

# Mensagem de inicialização
logger.info(f'Iniciando o script {cyan(nome_script)} no diretório {green(diretorio_completo_script_arquivo)}.')

exit()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#


# Carrega as variáveis encontradas no arquivo .env como variáveis de ambiente 
caminho_dotenv = os.path.join(os.path.dirname(__file__), 'tokens.env') # Caminho completo do arquivo 'tokens.env' no diretório
load_dotenv(caminho_dotenv) # Execução do carregamento

# Define os tokens de acesso ao banco de dados
server_name = getenv('SERVER_NAME')
database_name = getenv('DATABASE_NAME')
username = getenv('USERNAME')
password = getenv('PASSWORD')
trusted_connection = getenv('TRUSTED_CONNECTION') # Define o tipo de conxão (False = Autenticação do Windows; True = Autenticação com usuário e senha)

# Define os tokens de exportação
nome_arquivo = getenv('NOME_ARQUIVO')
diretorio_arquivo = getenv(r'DIRETORIO_ARQUIVO')
caminho_exportacao=f'{diretorio_arquivo}\\{nome_arquivo}'

# Define os tokens de codificação
codificacao = getenv('CODIFICACAO')
qualificador = getenv('QUALIFICADOR')
delimitador = getenv('DELIMITADOR')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Verifica se todas as variáveis estão definidas
def verifica_variaveis_dotenv(*args):
    for variaveis in args:
        if os.getenv(variaveis) is None:
            logging.info(f'A variável de ambiente "{variaveis}" não foi definida. Verifique o arquivo .env.')
            sys.exit()
    logger.info('Todas as variáveis de ambiente foram definidas.')

verifica_variaveis_dotenv(
    'SERVER_NAME',
    'DATABASE_NAME',
    'USERNAME',
    'PASSWORD',
    'TRUSTED_CONNECTION',
    'NOME_ARQUIVO',
    'DIRETORIO_ARQUIVO',
    'CODIFICACAO',
    'QUALIFICADOR',
    'DELIMITADOR'
)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Define o o nome do arquivo dinâmico para a exportação
def nome_arquivo_data(inicio_nome_arquivo,formato=1):
    
    # Mapeia os formatos disponíveis para os respectivos formatos de data e hora
    formatos_disponiveis = {
        1: '%Y%m%d-%H%M%S',
        2: '%Y%m%d'
    }
    
    # Verifica se o formato especificado está disponível
    if formato not in formatos_disponiveis:
        logger.error(f'O formato "{formato}" não está disponível.')
        sys.exit()
    
    # Retorna o formato selecionado
    logger.info(f'O formato dinâmico para o nome do arquivo foi selecionado como: "{formato}" ( {formatos_disponiveis[formato]} ).')
    
    # Formata a data e hora atual no formato desejado
    data_formatada = datetime.now().strftime(formatos_disponiveis[formato])
    
    # Constrói e retorna o nome do arquivo
    nome_do_arquivo = f'{inicio_nome_arquivo}_{data_formatada}.csv'
    logger.info(f'O nome dinâmico para o arquivo foi definido como: "{nome_do_arquivo}".')
    return nome_do_arquivo

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Testa a conexão de uma engine
def testar_conexao(engine):

    # Tenta estabelecer a conexão
    try:
        logger.info(f'Tentando estabelecer a conexão.')
        engine.connect()
        logger.info(f'A conexão foi estabelecida com sucesso.')
    except Exception as e:
        logger.error(f'Ocorreu um erro durante a conexão:\n{e}')
    return engine

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Cria a engine de conexão com o banco de dados
def criar_engine(username, password, server_name, database_name, trusted_connection):
    
    # Cria a string de conexão
    if trusted_connection == True:
        logger.info(f'Tipo de conexão definida como Autenticação do Windows.')
        connection_string = f'mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server'
    else:
        logger.info(f'Tipo de conexão definida como Autenticação do SQL Server')
        connection_string = f'mssql+pyodbc://{server_name}/{database_name}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    
    # Cria a engine com a string de conexão
    try: 
        engine = create_engine(connection_string)
        logger.info(f'A engine foi criada com sucesso.')
    except Exception as e:
        logger.error(f'Erro ao criar a engine:\n{e}')

    # Testa a conexão criada pela engine
    testar_conexao(engine)

    # Retorna a engine
    return engine

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Formata o DataFrame com bordas redondas
def formatar_dataframe(dataframe):

    print(tb(dataframe, headers='keys', tablefmt='rounded_grid'))
    logger.info(f'Formatação do DataFrame executada com sucesso.')
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Resume uma consulta para o número de linhas desejado
def resuma_consulta(sql_query, n_linhas):
    
    # Atribui a engine
    engine = global_engine

    # Executa a consulta resumida
    with engine.connect() as conexao:
        sql_query_resumida = conexao.execute(text(f'SELECT TOP {n_linhas} * FROM ({sql_query}) AS X'))
    return sql_query_resumida

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Cria o DataFrame da consulta
def query_para_dataframe(engine, sql_query):

    # Cria o DataFrame
    try:
        df = pd.read_sql(sql_query, engine)
        logger.info(f'DataFrame com base na consulta criado com sucesso.')

    except Exception as e:
        logger.error(f'Erro ao executar a consulta:\n{e}')

    return df

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Executa uma consulta SQL
def executa_query(engine, sql_query):

    # Executa a query estabelecida
    try: 
        with engine.connect() as conexao:
            resultado_query = conexao.execute(text(sql_query))
        logger.info(f'Query executada com sucesso.')
        return resultado_query
    
    except Exception as e:
        logger.error(f'Erro ao executar a consulta:\n{e}')

    finally:
        conexao.close()
        logger.info(f'Conexão encerrada com sucesso.')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
        
# Exporta o DataFrame para o formato .csv
def exportar_dataframe(df, caminho_exportacao, codificacao, qualificador, delimitador):

    try:
        if isinstance(df, pd.DataFrame):
            df.to_csv(caminho_exportacao, encoding=codificacao, index=False, quotechar=qualificador, sep=delimitador)
            logger.info(f'DataFrame exportado com sucesso para "{caminho_exportacao}".')
        else:
            logger.error('O objeto fornecido não é um DataFrame pandas.')
    except Exception as e:
        logger.error(f'Erro ao exportar o DataFrame:\n{e}')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Abre o arquivo e lê seu conteúdo
def abrir_arquivo_texto(caminho_arquivo):
    
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            arquivo_texto = arquivo.read().strip() # Removendo espaços em branco antes e depois do texto
            extensao_arquivo = os.path.splitext(caminho_arquivo)[1] # Obtendo a extensão do arquivo
        logger.info(f'Arquivo "{extensao_arquivo}" aberto com sucesso.')
    except Exception as e:
        logger.error(f'Erro ao abrir o arquivo "{extensao_arquivo}":\n{e}')
    return arquivo_texto

caminho_arquivo_sql = r'C:\Users\rapha\Desktop\consultas_extracao.sql'
caminho_arquivo_json = r'C:\Users\rapha\Desktop\consultas_extracao.json'

arquivo_sql = abrir_arquivo_texto(caminho_arquivo_sql)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Obtem as consultas de um arquivo .sql
''' O arquivo precisa estar com consultas demartadas por "--#" '''
def obter_consultas_sql(caminho_arquivo, nome_arquivo_exportacao):
    
    # Atribui a extensão do arquivo a uma variável
    extensao_arquivo = os.path.splitext(caminho_arquivo)[1]
    
    # Verifica se a extensão do arquivo é .sql
    if extensao_arquivo != '.sql':
        logger.error(f'Extensão do arquivo "{extensao_arquivo}" inválido. A extensão do arquivo deve ser ".sql".')
        sys.exit()
    
    # Usar expressão regular para encontrar todas as posições de "--#"
    lista_correspondencias = [correspondencia.start() for correspondencia in re.finditer(r'--#\s', arquivo_sql)]

    # Inicializar uma lista para armazenar as consultas em formato de dicionário
    consultas = []

    # Para cada posição encontrada, encontrar a próxima posição ou o final do arquivo
    for indice, corresp_inicio in enumerate(lista_correspondencias):
        if indice < len(lista_correspondencias) - 1:
            corresp_fim = lista_correspondencias[indice + 1]
        else:
            corresp_fim = len(arquivo_sql)
        
        # Nome da consulta dinâmico
        nome_consulta = f'consulta_{indice + 1}'
        
        # Obtendo a consulta e removendo o texto do "--#" até a primeira quebra de linha
        consulta = arquivo_sql[corresp_inicio:corresp_fim].strip()
        consulta_sem_comentario = re.sub(r'--#.*\n', '', consulta)
        
        # Armazenar a consulta como um item de dicionário com o nome dinâmico
        consulta_dict = {
            nome_consulta: consulta_sem_comentario
        }
        consultas.append(consulta_dict)

    # Define o caminho do arquivo JSON com o nome dinâmico
    diretorio_arquivo = os.path.dirname(caminho_arquivo)
    caminho_arquivo_json = f'{diretorio_arquivo}\{nome_arquivo_exportacao}.json'

    # Converter a lista de consultas em formato JSON
    json_consultas = json.dumps(consultas, indent=4, ensure_ascii=False)

    # Salvar o JSON em um arquivo
    with open(caminho_arquivo_json, 'w') as json_arquivo:
        json_arquivo.write(json_consultas)
    logger.info(f'Arquivo salvo em formato .json com sucesso em: "{caminho_arquivo_json}"')
    logger.info(f'Prévia do arquivo gerado:\n{json_consultas}')
    return caminho_arquivo_json

obter_consultas_sql(caminho_arquivo=caminho_arquivo_sql, nome_arquivo_exportacao='sql_dict')


sys.exit()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Define a main
def main() -> None:
        
    # Define a consulta
    obter_consultas_sql(caminho_arquivo_sql,'exportacao_teste')
    
    sql_query = '''
    SELECT *
    FROM TB_FILMES
    WHERE GENERO = 'DRAMA'
    '''

    # Atribui a engine
    global_engine = criar_engine(username, password, server_name, database_name, trusted_connection)

    # Executa a consulta e atribui o DataFrame
    df = query_para_dataframe(global_engine, sql_query)

    # Define o nome do arquivo .csv
    arquivo_csv = nome_arquivo_data(caminho_exportacao)

    # Exporta o DataFrame
    exportar_dataframe(df=df, caminho_exportacao=arquivo_csv, codificacao=codificacao, qualificador=qualificador, delimitador=delimitador)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Executa o script chamando a função main
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f'Erro durante a execução do script: {e}')