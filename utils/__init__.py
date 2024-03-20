#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

# - Importação de Bibliotecas - #

# Permite funcionalidades para interações com o sistema operacional
import os

# Permite funcionalidades para interações relacionadas ao ambiente Python
import sys

# Permite que os comandos sejam executados em segundo plano
import subprocess

# Permite a manipulação e carregamento de variáveis de ambiente em um arquivo .yaml
import yaml

# Fornece funcionalidades para a medição e maniputalação de datas
from datetime import datetime

# Fornece funcionalidades para a manipulação de arquivos e diretórios
import shutil

# Possibilita a anotação de tipos indicando que uma variável, argumento ou valor de retorno deve ser uma lista
from typing import List, Any

# Habilita o logging para retorno de mensagens de erro e informações no terminal
import logging 

# Fornece funcionalidades para a edição de cores e estilos de texto no terminal
from colorama import init, Fore, Style

# Fornece classes para manipulação de datas e horas de forma eficiente
from datetime import datetime

# Oferece ferramentas para trabalhar com funções e objetos chamáveis, incluindo funcionalidades de programação funcional
from functools import wraps

# Fornece funções para examinar as propriedades e estruturas de objetos
import inspect

# Habilita o Pandas e fornece a manipulação do arquivo Excel em um DataFrame
import pandas as pd

# Fornece formatações de dados tabulares em formato de tabela para exibição em consoles ou arquivos de texto
from tabulate import tabulate as tb

# Fornece funcionalidades orientada a objetos para trabalhar com caminhos de arquivos de sistena
from pathlib import Path

# Permite a definição de tipos e anotações de tipos para variáveis, argumentos de função e valores de retorno
from typing import NewType, NoReturn, Callable, Union, List

# Habilita o SQL Alchemy e fornece a interação com bancos de dados relacionais
import sqlalchemy
from sqlalchemy import create_engine, text, Connection, Engine
from sqlalchemy.engine import Connection, Engine, CursorResult

# Habilita o Pandas e fornece a manipulação do arquivo Excel em um DataFrame
import pandas as pd
from pandas import DataFrame

# Permite codificar e decodificar dados no formato .json
import json

# Habilita funcionalidades para buscar e manipular padrões de texto
import re

# Habilidta funcionalidades SQL para manipular dados relacionais em memória
import duckdb
from duckdb import connect, DuckDBPyRelation as DuckDB_Dataframe

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#