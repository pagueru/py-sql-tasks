#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

# Permite funcionalidades para interações relacionadas ao ambiente Python
import sys

# Fornece funcionalidades orientada a objetos para trabalhar com caminhos de arquivos de sistena
from pathlib import Path

# Fornece funcionalidades para manipulação de datas e horas
from datetime import datetime

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def configure_path(print_lines: bool = False) -> list[str] | None:
    '''   
    Configura o path do sistema para incluir o diretório pai do diretório atual.
    
    Isso permite o acesso a módulos relacionados ao projeto que estejam localizados
    em diretórios adjacentes.
    
    Parâmetros:
        print_lines (bool, opcional): Se True, imprime cada linha do path.
    
    Retorna:
        List[str] or None: Uma lista contendo os diretórios no path do sistema, incluindo o diretório pai,
                           ou None em caso de erro.
    '''
    try:
        # Adiciona o diretório de trabalho atual ao sys.path
        current_working_path = Path.cwd()
        sys.path.append(str(current_working_path))
        sys.path.append(str(Path(r'C:\Users\rapha\Documents\GitHub\py-sql-tasks\src')))
        sys.path.append(str(Path(__file__).resolve().parent.parent))
        
        # Imprime cada linha do path se `print_lines` for True
        if print_lines:
            for num, path_item in enumerate(sys.path, start=1):
                print(f'{num:2}. {path_item}')
        return sys.path
    
    except Exception as e:
        # Registra o erro usando um logger
        print(f'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {'\033[31mERROR\033[0m'} - Erro ao corrigir o path: {e}.')
        return None

# Executa a correção do path
configure_path()

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#