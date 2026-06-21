import ply.lex as lex
from datetime import datetime
import os

# Diccionario de palabras reservadas asignadas 
reserved= {
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'string': 'STRING',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR', 
    'return': 'RETURN',
    'new': 'NEW',
    'List': 'LIST',
    'Dictionary': 'DICTIONARY',
    'class': 'CLASS',
    'Main': 'MAIN',
    'static': 'STATIC',
    'public': 'PUBLIC',
    'private': 'PRIVATE',
    'using': 'USING',
    'var': 'VAR',
    'Console': 'CONSOLE',
    'Write': 'WRITE',
    'WriteLine': 'WRITELINE',
    'ReadLine': 'READLINE'
}

# Lista de TOKENS
tokens= (
    'IDENTIFICADOR',
    'ENTERO',
    'FLOTANTE',
    'CADENA',
    'CARACTER',
    # Operadores Aritmeticos
    'MAS', 'MENOS', 'MULT', 'DIV', 'MOD',
    # Operadores Logicos
    'AND', 'OR', 'NOT',
    # Operadores relacionales
    'IGUAL_IGUAL', 'DIFERENTE', 'MENOR_IGUAL', 'MAYOR_IGUAL', 'MENOR', 'MAYOR',
    # Asignacion y Delimitadores base
    'IGUAL', 'PUNTO_COMA', 'COMA', 'PUNTO', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 
    'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER',
    # Declaracion Lambda
    'FLECHA_LAMBDA'
) + tuple(reserved.values())

# Expresiones Regulares para Operadores Aritmeticos
t_MAS= r'\+'
t_MENOS= r'-'
t_MULT= r'\*'
t_DIV= r'/'
t_MOD= r'%'

#Expresiones Regulares para Operadores Logicos
t_AND= r'&&'
t_OR= r'\|\|'
t_NOT= r'!'

# Expresiones Regulares para Operadores Relacionales
t_IGUAL_IGUAL=r'=='
t_DIFERENTE= r'!='
t_MENOR_IGUAL= r'<='
t_MAYOR_IGUAL= r'>='
t_MENOR= r'<'
t_MAYOR= r'>'

# Asignación y Fin de Sentencia
t_IGUAL= r'='
t_PUNTO_COMA= r';'
t_COMA= r','
t_PUNTO= r'\.'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'

# Token para funciones lambda/expresion corta
# Ejemplo: int Duplicar(int n) => n*2
# IMPORTANTE: debe ir ANTES de t_IGUAL para que => no se tokenice como = y >
def t_FLECHA_LAMBDA(t):
    r'=>'
    return t

# Reglas con funciones con TOKENS complejos (con orden de prioridad)
def t_FLOTANTE(t):
    r'\d+\.\d+'
    t.value= float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value=int(t.value)
    return t

def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_CARACTER(t):
    r'\'([^\\\n]|(\\.))?\''
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type= reserved.get(t.value, 'IDENTIFICADOR')
    return t

#=========================================
#=== ESTRUCTURA GENERAL DEL ANALIZADOR ===
#=========================================

# Reglas Globales (PLY funcione bien)
t_ignore= ' \t'

def t_COMENTARIO_SIMPLE(t):
    r'//.*'
    pass

def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno+= t.value.count('\n')
    pass

def t_NUEVA_LINEA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para manejar errores
errores_lexicos= []
def t_error(t):
    error_msg= f"Caracter ilegal '{t.value[0]}' en la linea {t.lexer.lineno}"
    errores_lexicos.append(error_msg)
    t.lexer.skip(1)

# Construccion del Analizador Lexico
lexer= lex.lex()

#===========================================================
#=== FUNCION PARA GENERAR LOGS AUTOMATICOS - SOLO LEXICO ===
#===========================================================

def validar_algoritmo(archivo_codigo, nombre_desarrollador):
    global errores_lexicos
    errores_lexicos= []

    #Leer archivos de prueba
    with open(archivo_codigo, 'r', encoding='utf-8') as f:
        data= f.read()
    
    lexer.input(data)

    #Recolectar TOKENS
    resultado_log= f"---LOG ANALISIS LEXICO---\nArchivo: {archivo_codigo}\n\nTOKENS RECONOCIDOS:\n"
    for tok in lexer:
        resultado_log += f"Token:{tok.type}, Valor: '{tok.value}', Linea: {tok.lineno}\n"
    
    #Registrar Errores
    resultado_log+= "\nERRORES LEXICOS ENCONTRADOS:\n"
    if errores_lexicos:
        for err in errores_lexicos:
            resultado_log += err + "\n"
    else:
        resultado_log += "Ninguno.\n"
    
    #Generar archivo
    fecha_hora= datetime.now().strftime("%d-%m-%Y-%Hh%M")
    nombre_archivo= f"logs/lexico-{nombre_desarrollador}-{fecha_hora}.txt"

    os.makedirs('logs', exist_ok=True)
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(resultado_log)
    
    print(f"Análisis completado. Log guardado en: {nombre_archivo}")

#=============================================
#========== EJECUCICION DE PRUEBAS ===========
#=============================================

# Descomenta la línea del archivo que quieras probar
#validar_algoritmo("algoritmo_julio.cs", "JulioCevallos")
#validar_algoritmo("algoritmo_steven.cs", "StevenBarzola")
#validar_algoritmo("algoritmo_IssacMaza.cs", "IssacMaza")
#validar_algoritmo("algoritmo_clases.cs", "StevenBarzola")