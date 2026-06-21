import ply.yacc as yacc
from lexer import tokens
from datetime import datetime
import os

# =============================================================================
# PRECEDENCIA DE OPERADORES
# Definido por: Julio Cevallos
# Garantiza que la jerarquía matemática y lógica se respete
# =============================================================================
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'IGUAL_IGUAL', 'DIFERENTE', 'MENOR', 'MENOR_IGUAL', 'MAYOR', 'MAYOR_IGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIV', 'MOD'),
)

# =============================================================================
# RAÍZ Y ESTRUCTURA GLOBAL DEL COMPILADOR
# Estructura compartida para integrar los aportes del grupo
# =============================================================================
def p_programa(p):
    '''programa : directiva_using lista_sentencias
                | lista_sentencias'''
    p[0] = p[1]

# Definido por: Steven Barzola — Para importar con using (ej: using System;)
def p_directiva_using(p):
    '''directiva_using : USING IDENTIFICADOR PUNTO_COMA'''
    pass

def p_lista_sentencias(p):
    '''lista_sentencias : sentencia lista_sentencias
                       | sentencia'''
    pass

# Fusión de sentencias por parte todos los integrantes
def p_sentencia(p):
    '''sentencia : declaracion
                 | declaracion_var
                 | asignacion
                 | impresion
                 | bucle_while
                 | declaracion_arreglo
                 | metodo_main
                 | estructura_if
                 | declaracion_lista
                 | metodo_void
                 | bucle_for
                 | declaracion_diccionario
                 | declaracion_funcion
                 | sentencia_return
                 | llamada_funcion_stmt'''
    pass


# Recuperación de errores — Definido por: Issac Maza
# Permite al parser continuar después de un error hasta el siguiente ';' o '}'
def p_sentencia_error(p):
    '''sentencia : error PUNTO_COMA
                 | error LLAVE_DER'''
    pass

# --- 1. BASE DEL LENGUAJE: TIPOS PRIMITIVOS ---
# Definido por: Julio Cevallos
def p_tipo_primitivo(p):
    '''tipo_primitivo : INT
                      | FLOAT
                      | CHAR
                      | STRING
                      | BOOL'''
    pass

# --- 2. DECLARACIÓN Y ASIGNACIÓN ---
# Definido por: Julio Cevallos (Soporta declaraciones simples y múltiples en una línea)
def p_declaracion(p):
    '''declaracion : tipo_primitivo lista_declaraciones PUNTO_COMA'''
    pass

def p_lista_declaraciones(p):
    '''lista_declaraciones : lista_declaraciones COMA elemento_declaracion
                           | elemento_declaracion'''
    pass

def p_elemento_declaracion(p):
    '''elemento_declaracion : IDENTIFICADOR IGUAL expresion
                           | IDENTIFICADOR'''
    pass

# Definido por: Julio Cevallos
def p_asignacion(p):
    '''asignacion : IDENTIFICADOR IGUAL expresion PUNTO_COMA'''
    pass

# Definido por: Steven Barzola — Declaración implícita con var (ej: var x = 5;)
def p_declaracion_var(p):
    '''declaracion_var : VAR IDENTIFICADOR IGUAL expresion PUNTO_COMA'''
    pass


# --- 3. REGLAS GENERALES: ENTRADA / SALIDA (I/O) ---
# Definido por: Julio Cevallos
def p_impresion(p):
    '''impresion : CONSOLE PUNTO WRITE PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA
                 | CONSOLE PUNTO WRITELINE PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA'''
    pass


# --- 4. EXPRESIONES ARITMÉTICAS, RELACIONALES Y LÓGICAS ---
# Definido por: Julio Cevallos
def p_expresion_operaciones(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | expresion MOD expresion
                 | expresion IGUAL_IGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion MENOR expresion
                 | expresion MENOR_IGUAL expresion
                 | expresion MAYOR expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion AND expresion
                 | expresion OR expresion'''
    pass

# Definido por: Julio Cevallos
def p_expresion_not(p):
    '''expresion : NOT expresion'''
    pass

# Definido por: Julio Cevallos
def p_expresion_agrupacion(p):
    '''expresion : PARENTESIS_IZQ expresion PARENTESIS_DER'''
    pass

# Definido por: Julio Cevallos
# Integración: agregada llamada_funcion_expr (Issac Maza) para soportar llamadas dentro de expresiones
def p_expresion_terminal(p):
    '''expresion : ENTERO
                 | FLOTANTE
                 | CADENA
                 | CARACTER
                 | IDENTIFICADOR
                 | TRUE
                 | FALSE
                 | lectura_teclado
                 | llamada_funcion_expr'''
    pass


# Definido por: Julio Cevallos
def p_lectura_teclado(p):
    '''lectura_teclado : CONSOLE PUNTO READLINE PARENTESIS_IZQ PARENTESIS_DER'''
    pass


# --- 5.1 ESTRUCTURA DE CONTROL ASIGNADA: BUCLE WHILE ---
# Definido por: Julio Cevallos
def p_bucle_while(p):
    '''bucle_while : WHILE PARENTESIS_IZQ expresion PARENTESIS_DER bloque'''
    pass


# Definido por: Julio Cevallos
# Modificado por: Steven Barzola — agregada alternativa de bloque vacío {}
def p_bloque(p):
    '''bloque : LLAVE_IZQ lista_sentencias LLAVE_DER
              | LLAVE_IZQ LLAVE_DER'''
    pass


# --- 5.2 ESTRUCTURA DE CONTROL ASIGNADA: IF/ELSE ---
# Definido por: Steven Barzola
# Soporta: if, if/else, y else if encadenado
def p_estructura_if(p):
    '''estructura_if : IF PARENTESIS_IZQ expresion PARENTESIS_DER bloque
                     | IF PARENTESIS_IZQ expresion PARENTESIS_DER bloque ELSE bloque
                     | IF PARENTESIS_IZQ expresion PARENTESIS_DER bloque ELSE estructura_if'''
    pass


# --- 5.3 ESTRUCTURA DE CONTROL ASIGNADA: BUCLE FOR ---
# Definido por: Issac Maza
# Soporta: for (int i = 0; i < 5; i = i + 1) { ... }
def p_bucle_for(p):
    '''bucle_for : FOR PARENTESIS_IZQ tipo_primitivo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA IDENTIFICADOR IGUAL expresion PARENTESIS_DER bloque'''
    pass


# --- 6.1 ESTRUCTURA DE DATOS ASIGNADA: ARREGLOS TRADICIONALES ---
# Definido por: Julio Cevallos (Soporta: int[] vec; o int[] vec = new int[5];)
def p_declaracion_arreglo(p):
    '''declaracion_arreglo : tipo_primitivo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR PUNTO_COMA
                           | tipo_primitivo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR IGUAL NEW tipo_primitivo CORCHETE_IZQ ENTERO CORCHETE_DER PUNTO_COMA'''
    pass


# --- 6.2 ESTRUCTURA DE DATOS ASIGNADA: LISTAS ---
# Definido por: Steven Barzola
# Soporta:
#   List<int> numeros;
#   List<string> nombres = new List<string>();
# No soporta anidados: List<List<int>>
def p_declaracion_lista(p):
    '''declaracion_lista : LIST MENOR tipo_primitivo MAYOR IDENTIFICADOR PUNTO_COMA
                         | LIST MENOR tipo_primitivo MAYOR IDENTIFICADOR IGUAL NEW LIST MENOR tipo_primitivo MAYOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''
    pass


# --- 6.3 ESTRUCTURA DE DATOS ASIGNADA: DICCIONARIOS ---
# Definido por: Issac Maza
# Soporta:
#   Dictionary<string, int> edades;
#   Dictionary<string, int> edades = new Dictionary<string, int>();
def p_declaracion_diccionario(p):
    '''declaracion_diccionario : DICTIONARY MENOR STRING COMA INT MAYOR IDENTIFICADOR PUNTO_COMA
                               | DICTIONARY MENOR INT COMA INT MAYOR IDENTIFICADOR PUNTO_COMA
                               | DICTIONARY MENOR STRING COMA INT MAYOR IDENTIFICADOR IGUAL NEW DICTIONARY MENOR STRING COMA INT MAYOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                               | DICTIONARY MENOR INT COMA INT MAYOR IDENTIFICADOR IGUAL NEW DICTIONARY MENOR INT COMA INT MAYOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''
    pass


# --- 7.1 TIPO DE FUNCIÓN ASIGNADA: METODO MAIN ESTRUCTURAL ---
# Definido por: Julio Cevallos
# Main quemado como token reservado (Steven Barzola) para mayor precisión
def p_metodo_main(p):
    '''metodo_main : STATIC VOID MAIN PARENTESIS_IZQ PARENTESIS_DER bloque'''
    pass


# --- 7.2 TIPO DE FUNCIÓN ASIGNADA: MÉTODOS SIN RETORNO ---
# Definido por: Steven Barzola
# Soporta:
#   void Saludar() { ... }
#   public void Ejecutar(int x, bool flag) { ... }
#   private void Limpiar() { ... }
# Nota: las alternativas VOID de p_declaracion_funcion de Isaac se omiten
# aquí ya que esta regla las cubre con soporte adicional de PUBLIC/PRIVATE
def p_metodo_void(p):
    '''metodo_void : VOID IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER bloque
                   | PUBLIC VOID IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER bloque
                   | PRIVATE VOID IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER bloque'''
    pass


# --- 7.3 TIPO DE FUNCIÓN ASIGNADA: FUNCIONES CON RETORNO ---
# Definido por: Issac Maza
# Soporta:
#   int CalcularSuma(int a, int b) { return a + b; }
#   float CalcularPromedio(float total, int cantidad) { return total / cantidad; }
#   int Duplicar(int n) => n*2;   (expresión lambda)
# Nota: alternativas VOID excluidas, cubiertas por p_metodo_void (Steven Barzola)
def p_declaracion_funcion(p):
    '''declaracion_funcion : tipo_primitivo IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER bloque
                           | tipo_primitivo IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER FLECHA_LAMBDA expresion PUNTO_COMA'''
    pass


# Sentencia return — Definido por: Issac Maza
def p_sentencia_return(p):
    '''sentencia_return : RETURN expresion PUNTO_COMA
                        | RETURN PUNTO_COMA'''
    pass


# Llamada a función como sentencia — Definido por: Issac Maza
# Ej: LimpiarPantalla(); o CalcularSuma(a, b);
def p_llamada_funcion_stmt(p):
    '''llamada_funcion_stmt : IDENTIFICADOR PARENTESIS_IZQ argumentos PARENTESIS_DER PUNTO_COMA
                            | IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''
    pass


# Llamada a función dentro de expresiones — Definido por: Issac Maza
# Ej: int x = CalcularSuma(a, b);
def p_llamada_funcion_expr(p):
    '''llamada_funcion_expr : IDENTIFICADOR PARENTESIS_IZQ argumentos PARENTESIS_DER
                            | IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER'''
    pass


# Argumentos al llamar una función — Definido por: Issac Maza
def p_argumentos(p):
    '''argumentos : argumentos COMA expresion
                  | expresion'''
    pass


# --- REGLAS DE PARÁMETROS (compartidas por metodo_void y declaracion_funcion) ---
# Estructura base: Steven Barzola (lista_parametros + empty)
# Reutilizada por: Issac Maza
def p_parametros(p):
    '''parametros : lista_parametros
                  | empty'''
    pass


def p_lista_parametros(p):
    '''lista_parametros : lista_parametros COMA parametro
                        | parametro'''
    pass


def p_parametro(p):
    '''parametro : tipo_primitivo IDENTIFICADOR'''
    pass


def p_empty(p):
    '''empty :'''
    pass


# =============================================================================
# GESTIÓN DE ERRORES SINTÁCTICOS Y SISTEMA DE LOGS
# =============================================================================
errores_sintacticos = []


def p_error(p):
    if p:
        error_msg = f"Error sintactico: Token inesperado '{p.value}' de tipo {p.type} en la linea {p.lineno}"
    else:
        error_msg = "Error sintactico: Fin de archivo inesperado. Posible falta de ';' o '}'"

    errores_sintacticos.append(error_msg)
    print(error_msg)


# Construir el analizador sintáctico (YACC)
parser = yacc.yacc()


def validar_sintaxis_algoritmo(archivo_codigo, usuario_git):
    global errores_sintacticos
    errores_sintacticos = []

    if not os.path.exists(archivo_codigo):
        print(f"Error: El archivo {archivo_codigo} no existe.")
        return

    with open(archivo_codigo, 'r', encoding='utf-8') as f:
        data = f.read()

    # Ejecutar el parser sobre el código de prueba
    parser.parse(data)

    # Formatear el reporte de logs exigido por la rúbrica
    resultado_log = f"--- LOG ANÁLISIS SINTÁCTICO ---\n"
    resultado_log += f"Archivo analizado: {archivo_codigo}\n"
    resultado_log += f"Usuario Git: {usuario_git}\n"
    resultado_log += f"Fecha y Hora: {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}\n"
    resultado_log += "-" * 50 + "\n\n"

    if errores_sintacticos:
        resultado_log += f"ESTADO: RECHAZADO ({len(errores_sintacticos)} errores encontrados)\n\n"
        resultado_log += "DETALLE DE ERRORES:\n"
        for err in errores_sintacticos:
            resultado_log += f"- {err}\n"
    else:
        resultado_log += "ESTADO: EXITOSO (0 errores sintácticos detectados).\n"

    # Generar el archivo con el formato estricto: sintactico-usuarioGit-fecha-hora.txt
    fecha_hora_formato = datetime.now().strftime("%d%m%Y-%Hh%M")
    nombre_archivo_log = f"logs/sintactico-{usuario_git}-{fecha_hora_formato}.txt"

    os.makedirs('logs', exist_ok=True)
    with open(nombre_archivo_log, 'w', encoding='utf-8') as f:
        f.write(resultado_log)

    print(f"\n Pruebas completadas. El log se ha guardado en: {nombre_archivo_log}")


# =============================================================================
# EJECUCIÓN DE PRUEBAS DE SINTAXIS
# =============================================================================
if __name__ == "__main__":
    # validar_sintaxis_algoritmo("algoritmos/algoritmo_julio.cs", "JulioCevallos")
    # validar_sintaxis_algoritmo("algoritmos/algoritmo_IssacMaza.cs", "IssacMaza")
    # validar_sintaxis_algoritmo("algoritmos/algoritmo_sintactico_merge.cs", "StevenBarzola")
    print("Para que corra el programa")