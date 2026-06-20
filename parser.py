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
    '''programa : lista_sentencias'''
    p[0] = p[1]

def p_lista_sentencias(p):
    '''lista_sentencias : sentencia lista_sentencias
                       | sentencia'''
    pass

def p_sentencia(p):
    '''sentencia : declaracion
                 | asignacion
                 | impresion
                 | bucle_while
                 | declaracion_arreglo
                 | metodo_main
                 | bucle_for
                 | declaracion_diccionario
                 | declaracion_funcion
                 | sentencia_return
                 | llamada_funcion_stmt'''
    pass

# Placeholder para que el parser no falle mientras Steven e Issac agregan sus partes
def p_estructura_control_companeros(p):
    '''estructura_control_companeros : IF PARENTESIS_IZQ expresion PARENTESIS_DER bloque
                                    | FOR PARENTESIS_IZQ asignacion expresion PUNTO_COMA asignacion PARENTESIS_DER bloque'''
    pass


# =============================================================================
# === REGLAS SINTÁCTICAS: JULIO CEVALLOS ===
# =============================================================================

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
# Definido por: Julio Cevallos (¡Soporta declaraciones simples y múltiples en una línea!)
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

# Tu regla de asignación se queda exactamente igual como la tenías:
def p_asignacion(p):
    '''asignacion : IDENTIFICADOR IGUAL expresion PUNTO_COMA'''
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

# Definido por: Julio Cevallos (Permite usar Console.ReadLine() dentro de asignaciones)
def p_lectura_teclado(p):
    '''lectura_teclado : CONSOLE PUNTO READLINE PARENTESIS_IZQ PARENTESIS_DER'''
    pass


# --- 5. ESTRUCTURA DE CONTROL ASIGNADA: BUCLE WHILE ---
# Definido por: Julio Cevallos
def p_bucle_while(p):
    '''bucle_while : WHILE PARENTESIS_IZQ expresion PARENTESIS_DER bloque'''
    pass

# Definido por: Julio Cevallos (Define las Reglas de Alcance / Scope del bloque)
def p_bloque(p):
    '''bloque : LLAVE_IZQ lista_sentencias LLAVE_DER
              | LLAVE_IZQ LLAVE_DER'''
    pass


# --- 6. ESTRUCTURA DE DATOS ASIGNADA: ARREGLOS TRADICIONALES ---
# Definido por: Julio Cevallos (Soporta: int[] vec; o int[] vec = new int[5];)
def p_declaracion_arreglo(p):
    '''declaracion_arreglo : tipo_primitivo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR PUNTO_COMA
                           | tipo_primitivo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR IGUAL NEW tipo_primitivo CORCHETE_IZQ ENTERO CORCHETE_DER PUNTO_COMA'''
    pass


# --- 7. TIPO DE FUNCIÓN ASIGNADA: MÉTODO MAIN ESTRUCTURAL ---
# Definido por: Julio Cevallos (Reconoce la estructura 'static void Main()')
# Nota: 'static' y 'Main' se tratan como IDENTIFICADORES para evitar saturar el léxico.
def p_metodo_main(p):
    '''metodo_main : STATIC VOID IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER bloque'''
    pass

# =============================================================================
# === FIN DEL BLOQUE DE JULIO CEVALLOS ===
# =============================================================================

# =============================================================================
# === INICIO PARTE: ISSAC MAZA ===
# Reglas: bucle for, Dictionary<K,V>, funciones con return
# =============================================================================
 
# --- 1. ESTRUCTURA DE CONTROL: BUCLE FOR ---
# Definido por: Issac-Maza
# Soporta: for (int i = 0; i < 5; i = i + 1) { ... }
def p_bucle_for(p):
    '''bucle_for : FOR PARENTESIS_IZQ tipo_primitivo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA IDENTIFICADOR IGUAL expresion PARENTESIS_DER bloque'''
    pass
 
# --- 2. ESTRUCTURA DE DATOS: DICCIONARIO ---
# Definido por: Issac-Maza
# Soporta: Dictionary<string, int> edades = new Dictionary<string, int>();
def p_declaracion_diccionario(p):
    '''declaracion_diccionario : DICTIONARY MENOR STRING COMA INT MAYOR IDENTIFICADOR IGUAL NEW DICTIONARY MENOR STRING COMA INT MAYOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                               | DICTIONARY MENOR INT COMA INT MAYOR IDENTIFICADOR IGUAL NEW DICTIONARY MENOR INT COMA INT MAYOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                               | DICTIONARY MENOR STRING COMA INT MAYOR IDENTIFICADOR PUNTO_COMA
                               | DICTIONARY MENOR INT COMA INT MAYOR IDENTIFICADOR PUNTO_COMA'''
    pass
 
# --- 3. TIPO DE FUNCIÓN: FUNCIONES CON RETURN ---
# Definido por: Issac-Maza
# Soporta:
#   int CalcularSuma(int a, int b) { return a + b; }
#   float CalcularPromedio(float total, int cantidad) { return total / cantidad; }
#   void MostrarResultado() { return; }
#   int Duplicar(int n) => n*2;   (lambda)
def p_declaracion_funcion(p):
    '''declaracion_funcion : tipo_primitivo IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER bloque
                           | tipo_primitivo IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER bloque
                           | VOID IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER bloque
                           | VOID IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER bloque
                           | tipo_primitivo IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER FLECHA_LAMBDA expresion PUNTO_COMA'''
    pass
 
# Parámetros de una función: (int a, int b) o (float total, int cantidad)
# Definido por: Issac-Maza
def p_parametros(p):
    '''parametros : parametros COMA parametro
                  | parametro'''
    pass
 
def p_parametro(p):
    '''parametro : tipo_primitivo IDENTIFICADOR'''
    pass
 
# Sentencia return dentro de funciones
# Definido por: Issac-Maza
def p_sentencia_return(p):
    '''sentencia_return : RETURN expresion PUNTO_COMA
                        | RETURN PUNTO_COMA'''
    pass
 
# Llamada a función como sentencia: CalcularSuma(suma, i);
# Definido por: Issac-Maza
def p_llamada_funcion_stmt(p):
    '''llamada_funcion_stmt : IDENTIFICADOR PARENTESIS_IZQ argumentos PARENTESIS_DER PUNTO_COMA
                            | IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''
    pass
 
# Llamada a función dentro de expresiones: CalcularSuma(suma, i)
# Definido por: Issac-Maza
def p_llamada_funcion_expr(p):
    '''llamada_funcion_expr : IDENTIFICADOR PARENTESIS_IZQ argumentos PARENTESIS_DER
                            | IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER'''
    pass
 
# Argumentos al llamar una función
# Definido por: Issac-Maza
def p_argumentos(p):
    '''argumentos : argumentos COMA expresion
                  | expresion'''
    pass
 
# =============================================================================
# === FIN PARTE: ISSAC MAZA ===
# =============================================================================

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

# Recuperación de errores — Permite continuar después de un error hasta el siguiente ';'
def p_sentencia_error(p):
    '''sentencia : error PUNTO_COMA
                | error LLAVE_DER'''
    pass

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
    # Cambia "algoritmo_julio.cs" por el archivo C# que quieras testear.
    validar_sintaxis_algoritmo("algoritmo_IssacMaza.cs", "IssacMaza")