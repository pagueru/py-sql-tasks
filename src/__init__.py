#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

# Permite funcionalidades para interações relacionadas ao ambiente Python
import sys

# Permite funcionalidades para interações com o sistema operacional
import os

# Fornece funcionalidades orientada a objetos para trabalhar com caminhos de arquivos de sistena
from pathlib import Path

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def configurar_path(imprimir_linhas: bool = False) -> list:
    """
    Configura o path do sistema para incluir o diretório pai do diretório atual.
    
    Isso permite o acesso a módulos relacionados ao projeto que estejam localizados
    em diretórios adjacentes.
    
    Parâmetros:
        bool (opcional): Define se as linhas de caminho devem ser impressas na tela.
    
    Retorna:
        list: Uma lista contendo os diretórios no path do sistema, incluindo o diretório pai.
    """
    try:
        # Obtém o diretório do arquivo atual
        diretorio_atual = Path(__file__).parent
        
        # Obtém o diretório pai do diretório atual
        diretorio_pai = diretorio_atual.parent
        
        # Adiciona o diretório pai ao sys.path
        sys.path.append(str(diretorio_pai))
        
        # Adiciona o diretório da pasta 'utils'
        sys.path.append(Path.cwd() / diretorio_pai / 'utils')  
        
        # Adiciona o diretório da pasta 'utils'
        sys.path.append(Path.cwd() / diretorio_pai / 'config')  
        
        # Iterar sobre cada caminho em sys.path e imprimir linha por linha
        if bool == True:
            for path in sys.path:
                print(path)
        
        # Retorna sys.path atualizado
        return sys.path
    
    except Exception as e:
        print('Erro ao configurar o caminho:', e)
        return sys.path  # Retorna sys.path mesmo em caso de erro

configurar_path()

# Importar arquivo utils/__init__.py
from utils.__init__ import *

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#