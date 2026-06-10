import ply.lex as lex
from datetime import datetime
import os

#====================================
#=== INICIO PARTE: JULIO CEVALLOS ===
#====================================

# Diccionario de palabras reservadas asignadas 
reserved= {
    'int': 'INT',
    'float': 'FLOAT',
    'double': 'DOUBLE',
    'char': 'CHAR',
    'string': 'STRING',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE'
}

# Lista de TOKENS
tokens= [
    'IDENTIFICADOR',
    'NUMERO_ENTERO',
    'NUMERO_FLOTANTE',
    'CADENA',
    'CARACTER',
    # Operadores Aritmeticos
    'MAS', 'MENOS', 'MULT', 'DIV', 'MOD',
    # Operadores relacionales
    'IGUAL_IGUAL', 'DIFERENTE', 'MENOR_IGUAL', 'MAYOR_IGUAL', 'MENOR', 'MAYOR',
    # Asignacion y Delimitadores base
    'IGUAL', 'PUNTO_COMA', 'COMA', 'PUNTO', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 
    'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER'
] + list(reserved.values())

# Expresiones Regulares para Operadores Aritmeticos
t_MAS= r'\+'
t_MENOS= r'-'
t_MULT= r'\*'
t_DIV= r'/'
t_MOD= r'%'

# Expreisones Regulares para Operadores Relacionales
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

# Reglas con funciones con TOKENS complejos (con orden de prioridad)
def t_NUMERO_FLOTANTE(t):
    r'\d+\.\d+'
    t.value= float(t.value)
    return t

def t_NUMERO_ENTERO(t):
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

#====================================
#==== FIN PARTE: JULIO CEVALLOS =====
#====================================


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

def t_newline(t):
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

#=============================================
#=== FUNCION PARA GENERAR LOGS AUTOMATICOS ===
#=============================================

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
    resultado_log= "\nERRORES LEXICOS ENCONTRADOS:\n"
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

validar_algoritmo("algoritmo_julio.cs", "JulioCevallos")