#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

# Permite funcionalidades para interações com o sistema operacional e ao ambiente Python
import os, sys

# Corrige o path para chamar as funcionalidades do projeto
sys.path.append(os.getcwd())

# Importa as funcionalidades padrões do projeto
from shared.utils.resources import *

# Limpa o terminal
terminal_clear(True)

# Obtém o nome do scripts
file_name: str = Path(__file__).name

# Obtém o diretório completo do script com o nome do arquivo .py
full_path_file: Path = Path(__file__).parent

# Obtém o diretório da pasta do script
path_file_folder: Path = Path(__file__).parent.parent

# Obtém o diretório da pasta do script
path_file_folder_name: str = Path(__file__).parent.parent.name

# Obtém o diretório da pasta do script
log_file_name: str = str(f'{Path(__file__).parent.parent.name}_{file_name}')

# Configura o logger
logger: logging.Logger = logging_config(python_file = log_file_name,
                                        fg_log_file = False,
                                        log_file_path = Path.cwd() / 'py-sql-tasks' / 'logs')

# Mensagem de inicialização
logger.info(f'Iniciando o script {cyan(path_file_folder_name+'/'+file_name)} no diretório {green(full_path_file)}.')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Caminho para o arquivo .env
env_path: Path = Path(path_file_folder / '.env')

print(env_path)

# Carregar variáveis de ambiente
load_dotenv(env_path)

def check_env_variables(env_vars, *variables):
    '''
    Verifica se todas as variáveis de ambiente especificadas foram carregadas.
    Retorna True se todas as variáveis foram encontradas, False caso contrário.
    '''
    for var in variables:
        if var not in env_vars:
            return False
    return True

# Carrega as variáveis de ambiente do arquivo .env
env_vars = dotenv_values(env_path)

# Verifica se todas as variáveis de ambiente foram carregadas
required_variables = ['API_KEY', 'DATABASE_URL']
if check_env_variables(env_vars, *required_variables):
    print("Todas as variáveis de ambiente foram carregadas.")
else:
    print("Algumas variáveis de ambiente não foram carregadas.")


exit()

# Lista as variáveis de ambiente do arquivo .yaml
lista_variaveis: list = list(lista_variaveis_yaml(arquivo_yaml))

# Define os tokens de acesso ao banco de dados
server_name: str = os.getenv('SERVER_NAME')
#database_name: str = variaveis_yaml['banco_de_dados']['DATABASE_NAME']
username: str = variaveis_yaml['banco_de_dados']['USERNAME']
password: str = variaveis_yaml['banco_de_dados']['PASSWORD']
trusted_connection: str = variaveis_yaml['banco_de_dados']['TRUSTED_CONNECTION']

# Define a constante que receberá a conexão
CONEXAO: Connection = None
'''
    Cria uma conexão com o banco de dados usando os parâmetros fornecidos.\n
    O intuito é utilizar a constante `CONEXAO` para ser acessível por outros scripts, caso o parâmetro não seja preenchido no chamar da função
    
    Argumentos:
        `username` (str): Nome de usuário para autenticação no banco de dados.
        `password` (str): Senha de autenticação no banco de dados.
        `server_name` (str): Nome do servidor do banco de dados.
        `database_name` (str): Nome do banco de dados.
        `trusted_connection` (bool): Se deve usar uma conexão confiável (True) ou não (False).
        
    Retorno:
        `Connection`: A conexão estabelecida com o banco de dados.
'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Define o o nome do arquivo dinâmico para a exportação
def gerar_nome_arquivo_com_data(nome_arquivo: str = 'py-export', formato: int = 1) -> str:
    '''
    Formatos disponíveis (desconsiderar separadores): 
        `1`: 2024-12-01 23:59:59
        `2`: 2024-12-01
        `3`: 24-12-01 23:59:59
        `4`: 24-12-01
        `5`: 01-12-2024 23:59:59
        `6`: 01-12-2024
        `7`: 01-12-24 23:59:59
        `8`: 01-12-24
    '''
    # Mapeia os formatos disponíveis para os respectivos formatos de data e hora
    formatos_disponiveis: dict = {
        1: '%Y%m%d-%H%M%S',
        2: '%Y%m%d',
        3: '%y%m%d-%H%M%S',
        4: '%y%m%d',
        5: '%d%m%Y-%H%M%S',
        6: '%d%m%Y',
        7: '%d%m%y-%H%M%S',
        8: '%d%m%y', 
    }
    
    # Verifica se o formato especificado está disponível
    if formato not in formatos_disponiveis:
        logger.alert(f'O formato {red(formato)} não está disponível. O formato foi definido como {red(formatos_disponiveis[1])}.')
        formato = formatos_disponiveis[1]
    else:
        formato = formatos_disponiveis[formato]
        
    # Formata a data e hora atual no formato desejado
    data_formatada = datetime.now().strftime(formato)
    
    # Constrói e retorna o nome do arquivo
    nome_do_arquivo = nome_arquivo + '_' + data_formatada
    logger.info(f'O nome dinâmico para o arquivo foi definido como {cyan(nome_do_arquivo)}.')
    
    return nome_do_arquivo

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# class ConectorBancoDados(object):
#     '''
#     Permite estabelecer uma conexão com o banco de dados do tipo SQL Server, utilizando o Pyodbc como engine.
#     '''
#     def __init__(self, username: str, password: str, server_name: str, database_name: str, trusted_connection: bool) -> None:
#         '''
#         Inicializa a classe ConectorBancoDados com os parâmetros necessários para criar uma conexão com o banco de dados.

#         Parâmetros:
#             `username` (str): Nome de usuário para autenticação.
#             `password` (str): Senha para autenticação.
#             `server_name` (str): Nome do servidor.
#             `database_name` (str): Nome do banco de dados.
#             `trusted_connection` (bool): True se a autenticação for baseada em Windows, False caso contrário.
#         '''
#         self.username: str = username
#         self.password: str = password
#         self.server_name: str = server_name
#         self.database_name: str = database_name
#         self.trusted_connection: bool = trusted_connection
#         self.engine: Optional[Engine] = None

#     def criar_engine(self) -> Engine:
#         '''
#         Cria e retorna uma instância do SQLAlchemy Engine.

#         Retorna:
#             `create_engine` (Engine): Instância do SQLAlchemy Engine.
#         '''
#         if not all([self.username, self.password, self.server_name, self.database_name]):
#             logger.error('Parâmetros de entrada inválidos.')
#             return None
                
#         if self.trusted_connection:
#             connection_string: str = f'mssql+pyodbc://{self.username}:{self.password}@{self.server_name}/{self.database_name}?driver=ODBC+Driver+17+for+SQL+Server'
#         else:
#             connection_string: str = f'mssql+pyodbc://{self.server_name}/{self.database_name}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
        
#         try: 
#             self.engine = create_engine(connection_string)
#             logger.info('A engine de conexão com o banco de dados foi criada.')     
#             return self.engine
#         except Exception as e:
#             logger.error(f'Erro ao criar a engine: {e}')
#             return None

#     def criar_conexao(self) -> Connection:
#         '''
#         Valida e cria a conexão criada pela engine.

#         Retorna:
#             `conn` (Connection): Conexão estabelecida.
#         '''
#         try:
#             if self.engine is None:
#                 logger.error('A engine não foi inicializada.')
#                 return None
#             conn: Connection = self.engine.connect()
#             logger.info('A conexão com o banco de dados foi estabelecida.')
#             return conn
#         except Exception as e:
#             logger.error(f'Erro ao estabelecer a conexão: {e}')
#             return None

#     def estabelecer_conexao(self) -> Optional[Connection]:
#         '''
#         Cria uma engine de conexão com o banco de dados e retorna a conexão estabelecida.

#         Retorna:
#             `conn` (Connection): Conexão estabelecida.
#         '''
#         if self.criar_engine() is None:
#             return None
#         return self.criar_conexao()

#     def desconectar_engine(self) -> None:
#         '''
#         Encerra a conexão criada pela engine.
#         '''
#         try:
#             if self.engine is None:
#                 logger.error('A engine não foi inicializada.')
#                 return
#             self.engine.dispose()
#             logger.info('A conexão com o banco de dados foi encerrada.')
#         except Exception as e:
#             logger.error(f'Erro ao encerrar a conexão: {e}')


# db_connector = ConectorBancoDados(username, password, server_name, database_name, trusted_connection)
# conn = db_connector.estabelecer_conexao()
# # Use a conexão 'conn' para executar consultas, etc.
# # Quando terminar, você pode desconectar a engine chamando:
# db_connector.desconectar_engine()

# exit()


#----------------------------------------------------------------------------------------------------------------------------------------------------------------#




# Cria a engine de conexão com o banco de dados
def criar_engine(username: str, password: str, server_name: str, database_name: str, trusted_connection: bool) -> Engine:
    '''
    Cria e retorna uma instância do SQLAlchemy Engine.

    Parâmetros:
        `username`: Nome de usuário para autenticação.
        `password`: Senha para autenticação.
        `server_name`: Nome do servidor.
        `database_name`: Nome do banco de dados.
        `trusted_connection`: True se a autenticação for baseada em Windows, False caso contrário.

    Retorna:
        `create_engine`: Instância do SQLAlchemy Engine.
    '''
    # Validação de entrada
    if not all([username, password, server_name, database_name]):
        logger.error('Parâmetros de entrada inválidos.')
        return finalizar_script(False)
    
    # Cria a string de conexão
    if trusted_connection:
        logger.info(f'Tipo de conexão definida como {magenta('Autenticação do Windows')}.')
        connection_string = f'mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server'
    else:
        logger.info(f'Tipo de conexão definida como {magenta('Autenticação do SQL Server')}')
        connection_string = f'mssql+pyodbc://{server_name}/{database_name}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    
    # Cria a engine com a string de conexão
    try: 
        engine = create_engine(connection_string)
        logger.info(f'A {('engine de conexão')} com o banco de dados foi criada.')     
        return engine
    except Exception as e:
        logger.error(f'Erro ao criar a engine: {e}')
        return finalizar_script(False)
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Valida e cria a conexão criada pela engine
def criar_conexao(engine: Engine) -> Connection:
    
    try:
        conn: Connection = engine.connect()
        logger.info(f'A conexão com o banco de dados foi {('estabelecida')}.')
        return conn
    except Exception as e:
        logger.error(f'Error testing the connection: {e}')
   
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Cria uma engine de conexão com o banco de dados e retorna a conexão estabelecida       
def estabelecer_conexao(username: str, password: str, server_name: str, database_name: str, trusted_connection: bool) -> Connection:
    '''
    Cria uma engine de conexão com o banco de dados e retorna a conexão estabelecida.
    '''
    # Cria a engine
    engine = criar_engine(username, password, server_name, database_name, trusted_connection)
    
    # Se a criação da engine falhar, retornamos None
    if engine is None:
        return None
    
    # Se a criação da engine for bem-sucedida, criamos a conexão
    conn = criar_conexao(engine)
    
    # Retorna a conexão estabelecida
    return conn
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Encerra a conexão criada pela engine
def desconectar_engine(engine: Engine) -> None:
    try:
        engine.dispose()
        logger.info(f'A conexão com o banco de dados foi {yellow('encerrada')}.')
    except Exception as e:
        logger.error(f'Erro ao encerrar a conexão: {e}')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Define a conexão como global
def conexao_global(conexao: Connection) -> Connection:
    # Define a conexão como global
    if conexao is None:
        global CONEXAO
        conexao = CONEXAO
        return conexao

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Executa uma consulta SQL
def executa_consulta(consulta_sql: str, conexao: Connection = None) -> CursorResult:

    conexao = conexao_global(conexao)

    # Executa a query estabelecida
    try: 
        resultado_query = conexao.execute(text(consulta_sql))
        logger.info(f'Consulta executada com sucesso')
        logger.debug(f'Consulta: {italic(consulta_sql)}')
        resultado_query.close()
        return resultado_query
    
    except Exception as e:
        logger.error(f'Erro ao executar a consulta: {e}')  

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Resume uma consulta para o número de linhas desejado
def resume_consulta(consulta_sql: str, linhas: int = 5, conexao: Connection = None) -> CursorResult:
    
    conexao = conexao_global(conexao)

    # Executa a consulta resumida
    try:
        consulta_sql_resumida = conexao.execute(text(f'SELECT TOP {linhas} * FROM ({consulta_sql}) AS X'))
    except Exception as e:
        logger.error(f'Erro ao executar e resumir a consulta: {e}')
    return consulta_sql_resumida

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
        
# Exporta o DataFrame para o formato .csv
def exportar_dataframe(df: DataFrame, caminho_exportacao: Path, codificacao: str, qualificador: str, delimitador: str) -> None:

    try:
        if isinstance(df, DataFrame):
            df.to_csv(caminho_exportacao, encoding=codificacao, index=False, quotechar=qualificador, sep=delimitador)
            logger.info(f'DataFrame exportado com sucesso para "{caminho_exportacao}".')
        else:
            logger.error('O objeto fornecido não é um DataFrame.')
    except Exception as e:
        logger.error(f'Erro ao exportar o DataFrame: {e}')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Formata o DataFrame com bordas redondas
def formatar_dataframe(dataframe: DataFrame) -> str:
    '''
    Formata o DataFrame com bordas redondas e imprime no terminal.

    Parâmetros:
        `dataframe`: O DataFrame a ser formatado.
        `return_formatted`: Se `True`, retorna o DataFrame formatado. Default é `False`.

    '''
    # Formata o DataFrame com bordas redondas
    df_formatado = tabulate(dataframe, headers='keys', tablefmt='rounded_grid')
    logger.debug('Formatação do DataFrame executada com sucesso.')

    # Imprime o DataFrame formatado
    return df_formatado
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Cria o DataFrame da consulta
def query_para_dataframe(consulta_sql: str, top: int = None, formatar: bool = False, conexao: Connection = None) -> DataFrame:

    conexao = conexao_global(conexao)

    try:
        df = pd.read_sql(consulta_sql, conexao)
        logger.debug(f'A consulta SQL foi formatada em Dataframe.')
        
        # Redefine o índice para começar em 1
        df.index += 1

    except Exception as e:
        logger.error(f'Erro ao executar a consulta: {e}')

    # Define se deve mostrar o índice
    dt = df.head(top) if top is not None else df
    
    if formatar:
        df = formatar_dataframe(df)
        
    return df

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Abre o arquivo e lê seu conteúdo
def abrir_arquivo_sql(diretorio_arquivo: Path):
    try:
        with open(diretorio_arquivo, 'r') as arquivo:
            arquivo_sql = arquivo.read().strip() # Removendo espaços em branco antes e depois do texto
            extensao = diretorio_arquivo.suffix
            
            if extensao != '.sql':
                logger.error(f'O arquivo {red(diretorio_arquivo.name)} não é um arquivo válido no formato {cyan(".sql")}.')
                finalizar_script(False)
            else:
                logger.info(f'O arquivo {cyan(diretorio_arquivo.name)} foi encontrado na pasta {green(diretorio_arquivo.parent.name)}.')
            return arquivo_sql
    except Exception as e:
        logger.error(f'Erro ao abrir o arquivo {red(diretorio_arquivo.name)}: {e}')


#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def extrair_lista_de_consultas(arquivo_sql: str, classificador: str = None) -> list:
    
    # Dicionário para armazenar os SELECTs
    consultas = {}

    # Divide o conteúdo do arquivo em linhas
    linhas = str(arquivo_sql).split('\n')

    titulo = None
    consulta = ''
            
    if classificador is None:
        classificador = '--'

    for linha in linhas:
        # Verifica se a linha é um título de consulta
        if linha.startswith(classificador):
            if titulo is not None:
                
                # Remove espaços em branco desnecessários
                consultas[titulo] = consulta.strip()
                consulta = ''
                
            # Remove o prefixo '--' e espaços em branco
            titulo = linha.strip(classificador).strip()  
        else:
            consulta += linha + '\n'

    # Adiciona o último SELECT ao dicionário
    if titulo is not None:
        consultas[titulo] = consulta.strip()

    return consultas

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def exportar_dataframes_para_pasta(consultas: Union[dict, DataFrame], pasta_destino: Path, nome_arquivo: str = None, formato_data: int = 1, substituir: bool = False) -> None:
    # Retorna o status da substituição de arquivos
    status_substituicao: str = 'ativada' if substituir else 'desativada'
    logger.alert(f'Substituição de arquivos {yellow(status_substituicao)} ao exportar para a pasta {green(pasta_destino.name)}.')

    for chave, consulta_sql in (consultas.items() if isinstance(consultas, dict) else [(nome_arquivo, consultas)]):
        df = consulta_sql if isinstance(consulta_sql, DataFrame) else query_para_dataframe(consulta_sql)

        if nome_arquivo is None:  # Caso não seja fornecido um nome de arquivo
            if chave is None:  # Se a chave também for None, usamos 'exportacao' como nome de arquivo
                nome_arquivo_com_data = gerar_nome_arquivo_com_data('exportacao', formato_data)
            else:  # Caso contrário, usamos a chave como nome de arquivo
                nome_arquivo_com_data = gerar_nome_arquivo_com_data(chave, formato_data)
        else:  # Caso um nome de arquivo seja fornecido
            if chave is None:  # Se a chave também for None, usamos o nome fornecido
                nome_arquivo_com_data = gerar_nome_arquivo_com_data(nome_arquivo, formato_data)
            else:  # Caso contrário, combinamos a chave com o nome fornecido
                nome_arquivo_com_data = f'{chave}_{gerar_nome_arquivo_com_data(nome_arquivo, formato_data)}'

        nome_arquivo_com_data = re.sub(r'[^a-zA-Z0-9_]', '', str(nome_arquivo_com_data))

        # Caminho do arquivo com o nome definido
        caminho_arquivo = pasta_destino / f'{nome_arquivo_com_data}.csv'

        if caminho_arquivo.exists():
            if substituir:
                os.remove(caminho_arquivo)
                df.to_csv(caminho_arquivo, index=False)
                logger.info(f'O arquivo {cyan(caminho_arquivo.name)} existente em {green(pasta_destino.name)} foi substituído.')
            else:
                logger.alert(f'O arquivo {cyan(caminho_arquivo.name)} já existe na pasta {green(pasta_destino.name)}.')
        else:
            df.to_csv(caminho_arquivo, index=False)
            logger.info(f'O arquivo {cyan(caminho_arquivo.name)} foi exportado para a pasta {green(pasta_destino.name)}.')



#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Define a main
def main() -> None:

    # Define as variáveis do arquivo de exportação
    nome_arquivo: str = 'exportacao'
    nome_arquivo_dinamico: str = gerar_nome_arquivo_com_data(nome_arquivo, 2) + '.csv'
    classificador: str = '--'
    codificacao: str = 'utf-8'
    qualificador: str = '"'
    delimitador: str = ';'

    # Define as variáveis de diretórios
    diretorio_raiz: Path = Path.cwd()
    diretorio_projeto: Path  = Path(diretorio_raiz / 'py-sql-tasks')
    diretorio_scripts_sql: Path = diretorio_projeto / 'data' / 'scripts'
    diretorio_output: Path = diretorio_projeto / 'data' / 'output'
    diretorio_arquivo_sql: Path = diretorio_scripts_sql / 'SELECT_DB.sql'
    diretorio_arquivo_output: Path = diretorio_output / nome_arquivo_dinamico
                
    consultas_sql = abrir_arquivo_sql(diretorio_arquivo_sql)
    dicionario_consultas = extrair_lista_de_consultas(consultas_sql, classificador)
                
    consulta_1: str = dicionario_consultas[list(dicionario_consultas.keys())[0]]
    consulta_2: str = dicionario_consultas[list(dicionario_consultas.keys())[1]]  
 
    consulta_1 = query_para_dataframe(consulta_1)
    
    
    exportar_dataframes_para_pasta(consulta_1, diretorio_output)
    
    exit()
    
    consulta_1: DataFrame = query_para_dataframe(consulta_1, formatar = False)
   
    
    exportar_dataframe(consultas_sql, diretorio_arquivo_output, codificacao, qualificador, delimitador)
    
    terminate_script()
    

    #print(json.dumps(consultas, indent=4, ensure_ascii=False))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Executa o script chamando a função main
if __name__ == '__main__':
    
    # Define a conexão a constante
    try: 
        CONEXAO: Connection = estabelecer_conexao(username, password, server_name, database_name, trusted_connection) 
    except Exception as e:
        logger.error(f'Erro ao estabelecer a conexão global: {e}')
    
    # Executa o script
    try:
        main()
    except Exception as e:
        logger.error(f'Erro durante a execução do script: {e}')
