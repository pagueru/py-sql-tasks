#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

'''
- A ideia do utils.py é trazer funcionalidades padrões para os projetos simultâneos
- Para isso, importa as principais bibliotecas utilizadas nos projetos
- Enquanto o projeto não tomar forma para ganhar um repositório próprio, será mantido em py-sandbox para experimentação
'''

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# - Importação de bibliotecas - #

# Permite funcionalidades para interações com o sistema
import os

# Permite que os comandos sejam executados em segundo plano
import subprocess

# Permite funcionalidades para interações com o sistema
import sys

# Fornece funcionalidades para a medição e maniputalação de datas
from datetime import datetime

# Permite funcionalidades para o interpretador
import sys

# 
import shutil

# Possibilita a anotação de tipos indicando que uma variável, argumento ou valor de retorno deve ser uma lista.
from typing import List, Any

# 
from pathlib import Path

# Habilita o logging para retorno de mensagens de erro e informações no terminal
import logging 

# Fornece funcionalidades para a edição de cores e estilos de texto no terminal
from colorama import init, Fore, Style

# 
from datetime import datetime

# 
from functools import wraps

# 
import inspect

# Habilita o Pandas e fornece a manipulação do arquivo Excel em um DataFrame
import pandas as pd

# 
from tabulate import tabulate as tb

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Limpa o terminal
os.system('cls' if os.name == 'nt' else 'clear')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Inicializa o Colorama
init(autoreset=True)

def underline(texto: str = '') -> str:
    '''Formata o texto para underline no terminal.'''
    return str('\033[4m' + str(texto) + Style.RESET_ALL)

def bold(texto: str = '') -> str:
    '''Formata o texto para bold no terminal.'''
    return str(Style.BRIGHT + str(texto) + Style.RESET_ALL)

def italic(texto: str = '') -> str:
    '''Formata o texto para italic no terminal.'''
    return str('\x1B[3m' + str(texto) + Style.RESET_ALL)

def cyan(texto: str = '') -> str:
    '''Formata o texto cyan no terminal.'''
    return str(Fore.CYAN + str(texto) + Style.RESET_ALL)

def green(texto: str = '') -> str:
    '''Formata o texto green no terminal.'''
    return str(Fore.GREEN + str(texto) + Style.RESET_ALL)

def red(texto: str = '') -> str:
    '''Formata o texto red no terminal.'''
    return str(Fore.RED + str(texto) + Style.RESET_ALL)

def magenta(texto: str = '') -> str:
    '''Formata o texto magenta no terminal.'''
    return str(Fore.MAGENTA + str(texto) + Style.RESET_ALL)    

def yellow(texto: str = '') -> str:
    '''Formata o texto magenta no terminal.'''
    return str(Fore.YELLOW + str(texto) + Style.RESET_ALL)                            
 
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Formata a data e hora como uma string
def define_data_hora_formatada() -> datetime.strftime:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Retorna uma mensagem manual de configuração do logger
def logger_manual(level_name: str = None) -> str:

    if level_name is None:
        level_name = 'info'.upper()
    else:
        level_name.upper()
    return print(f'{define_data_hora_formatada()} - {green('INFO')} - Nível de logger configurado como {format_logging(level_name)}.')


#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Define um novo nível de log personalizado
logging.addLevelName(25, 'ALERT')

# Define o método para chamar o novo nível
def alert(self, message, *args, **kws):
    self._log(25, message, args, **kws) 
    
# Vincula o novo nível de log ao objeto logging
logging.Logger.alert = alert

# Mapeia os níveis de log para cores correspondentes 
def format_logging(levelname: str):
    colors = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ALERT': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA,
        'CUSTOM': Fore.MAGENTA
    }
    return f'{colors.get(levelname, '')}{levelname}{Style.RESET_ALL}'

# Configura o logger para retorno de mensagens de erro e informações no terminal
def configurar_logger(atributo_nome: str = __name__, level_name: str = 'info') -> logging.Logger:
    try:
        # Define um formatador personalizado
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname_formatted)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        # Adiciona um filtro para adicionar o levelname formatado
        class LevelnameFormatter(logging.Filter):
            def filter(self, record):
                record.levelname_formatted = format_logging(record.levelname)
                return True
        
        # Cria e configura o logger
        logger: logging.Logger = logging.getLogger(atributo_nome)     
        
        # Configura o nível de log
        match level_name.lower():
            case 'info':
                logger.setLevel(logging.INFO)
            case 'debug':
                logger.setLevel(logging.DEBUG)
            case 'warning':
                logger.setLevel(logging.WARNING)
            case 'error':
                logger.setLevel(logging.ERROR)
            case 'critical': 
                logger.setLevel(logging.CRITICAL)
            case _:
                logger.setLevel(logging.INFO)
                
        # Adiciona o formatador ao logger
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.addFilter(LevelnameFormatter())
        logger.addHandler(handler)
        
    except Exception as e:
        raise Exception(f'Ocorreu um erro ao configurar o logger:\n{e}')
    return logger

# Configura o logger
logger = configurar_logger('utils.py')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Configura a funcionalidade para limpar o terminal
def limpar_terminal(bool: bool = True) -> None:
    try:

        # Detecta automaticamente o comando de limpeza do terminal
        limpar_comando = 'cls' if os.name == 'nt' else 'clear'  # 'nt' para Windows e 'clear' para Linux ou macOS

        # Executa o comando de limpeza do terminal
        subprocess.run(limpar_comando, shell=True, check=True)

        # Retorna mensagem no terminal
        logger.info('Terminal limpo.') if bool else None
            
    except Exception as e:
        logger.error(f'Erro ao limpar o terminal:\n{e}')
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Permite a tipagem de parâmetros
from typing import NewType, Union, List
        
# Permite que os comandos sejam executados em segundo plano
def executar_comandos_bash(comandos: List[str]) -> None:  # type: ignore
    for comando in comandos:
        # Permite executar comandos no sistema operacional a partir de um script Python.
        subprocess.run(comando, shell=True) # shell=True torna o comando executável
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Formatação do DataFrame com bordas redondas
def formatar_dataframe(dataframe: pd.DataFrame, flag: bool=False) -> pd.DataFrame:
    try: 
        if flag:
            print(tb(dataframe, headers='keys', tablefmt='rounded_grid'))
        else:
            print(tb(dataframe.head(), headers='keys', tablefmt='rounded_grid'))
    except Exception as e:
        logger.error(f'Ocorreu um erro ao formatar o DataFrame:\n{e}\n')
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Permite a tipagem de parâmetros
from typing import NewType, NoReturn, Callable

# Finaliza o script
def finaliza_script() -> NoReturn:
    logger.info(f'Finalizando o script...')
    exit()
    
# Finaliza o script com erro
def finaliza_script_com_erro() -> NoReturn:
    logger.info(f'Finalizando o script devido a um erro.')
    exit()

# Declara um tipo extensões de arquivos (exemplo: '.csv', '.txt', '.py'...)
FileExtension = NewType('FileExtension', str)

def valida_extensao_de_texto(extensao: FileExtension) -> bool:
    # Lista de extensões de texto válidas
    text_extensions = ['.sql','.txt', '.csv', '.json', '.xml', '.html', '.md', '.log', '.env', '.yml', '.yaml', '.py']
    
    if extensao.find('.') == -1:
        logger.error(f'A string "{extensao}" não é uma extensão válida de arquivo.')
        exit()

    if extensao.lower() in text_extensions:
        return True
    else:
        logger.info(f'A extensão "{extensao}" não está na lista de extensões válidas. É possível que ocorram erros no script.')
        return True

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def configurar_arquivo_log(diretorio_do_arquivo: Path = None, fg_nome_dinamico: bool = True) -> None:
    '''Configuração do arquivo de log.'''
    try:
        # Configuração do logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)  # Define o nível de log para INFO

        # Criação do manipulador de arquivo para o log
        if diretorio_do_arquivo is None:
            logger.alert('Nenhum diretório de log foi especificado.')
            diretorio_raiz = Path.home() / 'Desktop' / 'logs'
            nome_script = Path(__file__).stem
            nome_arquivo_log = f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt' if fg_nome_dinamico else '_log.txt'
            diretorio_do_arquivo = diretorio_raiz / f'{nome_script}_py' / nome_arquivo_log

            # Cria o diretório de log se ele não existir
            if not diretorio_do_arquivo.parent.exists():
                diretorio_do_arquivo.parent.mkdir(parents=True, exist_ok=True)

        # Criação do manipulador de arquivo para o log
        log_file_handler = logging.FileHandler(diretorio_do_arquivo)
        log_file_handler.setLevel(logging.INFO)

        # Formatação do log
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_file_handler.setFormatter(formatter)

        # Adiciona o manipulador de arquivo ao logger
        logger.addHandler(log_file_handler)

        logger.info(f'Arquivo de log definido no diretório: {diretorio_do_arquivo}')

    except Exception as e:
        logger.error(f'Erro ao configurar o arquivo de log: {e}')

def main():
    print('Olá mundo')

if __name__ == '__main__':
    configurar_arquivo_log()
    main()


#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def linha_atual() -> int:
    '''Retorna o nível da linha atual'''
    current_frame = inspect.currentframe().f_lineno
    return current_frame

def erro_execucao(parametro_decorador: str):
    def decorator_erro_execucao(func: Callable) -> Callable:
        '''Decorator para capturar e registrar erro na execução da função.'''
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if parametro_decorador == 'debug':
                    #logger.debug(f'Executando a função {format_1(func.__name__)} na linha {format_4(linha_atual())}')
                    logger.debug(f'Executando a função {cyan(func.__name__)}')
                return func(*args, **kwargs)
            except Exception as e:
                # Captura e registra o erro
                logger.error(f'Erro ao executar a função {red(func.__name__)}: {bold(e)}')
        return wrapper
    return decorator_erro_execucao

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
