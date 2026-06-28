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
# INFRAESTRUCTURA DE ANÁLISIS SEMÁNTICO
# Desarrollado por: Julio Cevallos
# =============================================================================

class TablaSimbolos:
    def __init__(self):
        self.variables = {}  # { nombre: {'tipo': tipo, 'categoria': str} }

    # categoria puede ser: 'variable', 'arreglo', 'lista', 'diccionario' o 'metodo'
    def insertar(self, nombre, tipo, categoria='variable'):
        self.variables[nombre] = {'tipo': tipo, 'categoria': categoria}

    def existe(self, nombre):
        return nombre in self.variables

    def obtener_tipo(self, nombre):
        if self.existe(nombre):
            return self.variables[nombre]['tipo']
        return None

    def obtener_categoria(self, nombre):
        if self.existe(nombre):
            return self.variables[nombre]['categoria']
        return None

    def limpiar(self):
        self.variables.clear()

# Inicialización de componentes globales del Semántico
tabla_simbolos = TablaSimbolos()
errores_semanticos = []
tipo_retorno_actual = None  #Compartido: Steven lo pone en None (void), Issac lo pone en 'int', 'float', etc.

def registrar_error_semantico(mensaje, linea):
    error_formateado = f"Error Semántico (Línea {linea}): {mensaje}"
    if error_formateado not in errores_semanticos:
        errores_semanticos.append(error_formateado)



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
    p[0] = p[1].lower() # Propaga 'int', 'float', 'char', etc.

# --- 2. DECLARACIÓN Y ASIGNACIÓN ---
# Definido por: Julio Cevallos (Soporta declaraciones simples y múltiples en una línea)
def p_declaracion(p):
    '''declaracion : tipo_primitivo lista_declaraciones PUNTO_COMA'''
    tipo_base= p[1] #'int', 'float', 'char', etc.
    # Procesamos cada variable declarada en la línea
    for elem in p[2]:
        modo, nombre_var, tipo_exp, linea= elem
        if tabla_simbolos.existe(nombre_var):
            registrar_error_semantico(f"Redeclaración de la variable '{nombre_var}'.", linea)
        else:
            if modo == "asignado" and tipo_exp != "error":
                if tipo_base != tipo_exp:
                    # Coerción implícita permitida de int a float en C# - BugFix por Steven Barzola
                    if tipo_base == "float" and tipo_exp == "int":
                        pass
                    else:
                        registrar_error_semantico(f"No se puede asignar el tipo '{tipo_exp}' a una variable de tipo '{tipo_base}'.", linea)
            # Guardamos la variable en la tabla con su tipo base correcto
            tabla_simbolos.insertar(nombre_var, tipo_base)

def p_lista_declaraciones(p):
    '''lista_declaraciones : lista_declaraciones COMA elemento_declaracion
                           | elemento_declaracion'''
    if len(p) == 4:
        p[0]= p[1] + [p[3]]
    else:
        p[0]= [p[1]]

def p_elemento_declaracion(p):
    '''elemento_declaracion : IDENTIFICADOR IGUAL expresion
                           | IDENTIFICADOR'''
    if len(p) == 4:
        p[0]= ("asignado", p[1], p[3], p.lineno(1))
    else:
        p[0]= ("solo", p[1], None, p.lineno(1)) #BugFix para que reconozca sin inicializar (en teoria)

# Definido por: Julio Cevallos
def p_asignacion(p):
    '''asignacion : IDENTIFICADOR IGUAL expresion PUNTO_COMA'''
    nombre_var= p[1]
    tipo_exp= p[3]
    linea= p.lineno(1)

    if not tabla_simbolos.existe(nombre_var):
        registrar_error_semantico(f"Asignación a variable no declarada '{nombre_var}'.", linea)
    else:
        tipo_var= tabla_simbolos.obtener_tipo(nombre_var)
        if tipo_exp != "error" and tipo_var != tipo_exp:
            if tipo_var == "float" and tipo_exp == "int":
                pass
            else:
                registrar_error_semantico(f"No se puede asignar el tipo '{tipo_exp}' a la variable '{nombre_var}' de tipo '{tipo_var}'.", linea)

# Definido por: Steven Barzola — Declaración implícita con var (ej: var x = 5;)
# Regla Semántica por Steven Barzola
def p_declaracion_var(p):
    '''declaracion_var : VAR IDENTIFICADOR IGUAL expresion PUNTO_COMA'''
    nombre_var = p[2]
    tipo_inferido = p[4]
    linea = p.lineno(2)

    if tabla_simbolos.existe(nombre_var):
        registrar_error_semantico(f"Redeclaración de la variable '{nombre_var}'.", linea)
    else:
        if tipo_inferido == "error":
            registrar_error_semantico(f"No se puede inferir el tipo de '{nombre_var}' porque la expresión contiene errores.", linea)
        else:
            tabla_simbolos.insertar(nombre_var, tipo_inferido)


# --- 3. REGLAS GENERALES: ENTRADA / SALIDA (I/O) ---
# Definido por: Julio Cevallos
def p_impresion(p):
    '''impresion : CONSOLE PUNTO WRITE PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA
                 | CONSOLE PUNTO WRITELINE PARENTESIS_IZQ expresion PARENTESIS_DER PUNTO_COMA'''
    if p[5] == "error":
        registrar_error_semantico("La expresión en la función de impresión contiene errores semánticos.", p.lineno(3))


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
    op= p.slice[2].type #Para luego separar los tipos de operaciones (no es lo mismo operar un + que un <)
    t1= p[1]
    t2= p[3]
    linea= p.lineno(2)
    
    if t1 == "error" and t2 == "error":
        p[0] = "error"
        return
    
    # Operaciones Aritmeticas
    if op in ["MAS", "MENOS", "MULT", "DIV", "MOD"]:
        if t1 == "string" and op == "MAS": # Concatenacion de cadenas (Solo si el de la izquierda es string)
            p[0]= "string"
        elif t1 in ["int", "float"] and t2 in ["int", "float"]:
            p[0]= "float" if ("float" in [t1, t2]) else "int"
        else:
            registrar_error_semantico(f"Operación aritmética no válida entre los tipos '{t1}' y '{t2}'.", linea)
            p[0]= "error"
    
    # Operaciones Relacionales (Condicionales)
    elif op in ["IGUAL_IGUAL", "DIFERENTE", "MENOR", "MENOR_IGUAL", "MAYOR", "MAYOR_IGUAL"]:
        if(t1 in ["int", "float"] and t2 in ["int", "float"]) or (t1 == t2): #Solo comparacion del mismo tipo (excepcion int y float)
            p[0] = "bool"
        else:
            registrar_error_semantico(f"Comparación lógica inválida entre tipos '{t1}' y '{t2}'.", linea)
            p[0] = "error"
    
    # Operadores Logicos (Conectar Condicionales)
    elif op in ["AND", "OR"]:
        if t1 == "bool" and t2 == "bool":
            p[0] = "bool"
        else:
            registrar_error_semantico(f"Los operadores lógicos requieren tipos 'bool' (se recibió '{t1}' y '{t2}').", linea)
            p[0] = "error"

# Definido por: Julio Cevallos
def p_expresion_not(p):
    '''expresion : NOT expresion'''
    if p[2] != "error" and p[2] != "bool":
        registrar_error_semantico(f"El operador de negación '!' no se puede aplicar al tipo '{p[2]}'. Requiere un 'bool'.", p.lineno(1))
        p[0]= "error"
    else:
        p[0]= "bool"

# Definido por: Julio Cevallos
def p_expresion_agrupacion(p):
    '''expresion : PARENTESIS_IZQ expresion PARENTESIS_DER'''
    p[0] = p[2]

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
    tipo_token= p.slice[1].type

    if tipo_token == "ENTERO":
        p[0]= "int"
    elif tipo_token == 'FLOTANTE':
        p[0] = 'float'
    elif tipo_token == 'CADENA':
        p[0] = 'string'
    elif tipo_token == 'CARACTER':
        p[0] = 'char'
    elif tipo_token in ['TRUE', 'FALSE']:
        p[0] = 'bool'
    elif tipo_token == 'IDENTIFICADOR':
        nombre_var = p[1]
        if not tabla_simbolos.existe(nombre_var):
            registrar_error_semantico(f"Uso de variable no declarada '{nombre_var}'.", p.lineno(1))
            p[0] = 'error'
        else:
            p[0] = tabla_simbolos.obtener_tipo(nombre_var)
    elif tipo_token in ['lectura_teclado', 'llamada_funcion_expr']:
        p[0] = p[1] if p[1] else 'string' # (DEJAR ASI O MODIFICAR) Por llamada_funcion_expr se pone que retorna STRING aunque no sea cierto


# Definido por: Julio Cevallos
def p_lectura_teclado(p):
    '''lectura_teclado : CONSOLE PUNTO READLINE PARENTESIS_IZQ PARENTESIS_DER'''
    p[0] = "string" # Console.ReadLine() siempre retorna string en C#


# --- 5.1 ESTRUCTURA DE CONTROL ASIGNADA: BUCLE WHILE ---
# Definido por: Julio Cevallos
def p_bucle_while(p):
    '''bucle_while : WHILE PARENTESIS_IZQ expresion PARENTESIS_DER bloque'''
    tipo_condicion = p[3]
    linea = p.lineno(1)
    if tipo_condicion != 'error' and tipo_condicion != 'bool':
        registrar_error_semantico(f"La condición de la instrucción 'while' requiere un tipo 'bool' (Se recibió un tipo '{tipo_condicion}').", linea)


# Definido por: Julio Cevallos
# Modificado por: Steven Barzola — agregada alternativa de bloque vacío {}
def p_bloque(p):
    '''bloque : LLAVE_IZQ lista_sentencias LLAVE_DER
              | LLAVE_IZQ LLAVE_DER'''
    pass


# --- 5.2 ESTRUCTURA DE CONTROL ASIGNADA: IF/ELSE ---
# Definido por: Steven Barzola (Reglas sintácticas y semanticas)
# Soporta: if, if/else, y else if encadenado
def p_estructura_if(p):
    '''estructura_if : IF PARENTESIS_IZQ expresion PARENTESIS_DER bloque
                     | IF PARENTESIS_IZQ expresion PARENTESIS_DER bloque ELSE bloque
                     | IF PARENTESIS_IZQ expresion PARENTESIS_DER bloque ELSE estructura_if'''
    tipo_condicion = p[3]
    linea = p.lineno(1)

    if tipo_condicion != "error" and tipo_condicion != "bool":
        registrar_error_semantico(f"La condición de la instrucción 'if' requiere un tipo 'bool' (Se recibió un tipo '{tipo_condicion}').", linea)


# --- 5.3 ESTRUCTURA DE CONTROL ASIGNADA: BUCLE FOR ---
# Definido por: Issac Maza
# Soporta: for (int i = 0; i < 5; i = i + 1) { ... }
#
# REGLA SEMÁNTICA 1 — Issac Maza:
#   La expresión condicional del 'for' debe evaluar estrictamente a tipo 'bool'.
#   Adicionalmente, la variable de control se registra en la tabla de símbolos
#   para que pueda ser usada dentro del bloque sin errores de "variable no declarada".

def p_bucle_for(p):
    '''bucle_for : FOR PARENTESIS_IZQ tipo_primitivo IDENTIFICADOR IGUAL expresion PUNTO_COMA expresion PUNTO_COMA IDENTIFICADOR IGUAL expresion PARENTESIS_DER bloque'''
    tipo_var_control = p[3]       # 'int', 'string', etc.
    nombre_var_control = p[4]     # 'i', 's', etc.
    tipo_condicion = p[8]         # resultado de la expresión condicional (ej: bool)
    linea = p.lineno(1)
 
    # Regla semántica 1a: la condición debe ser bool
    if tipo_condicion != 'error' and tipo_condicion != 'bool':
        registrar_error_semantico(
            f"La condición del bucle 'for' debe ser de tipo 'bool' "
            f"(se recibió '{tipo_condicion}').",
            linea
        )
    # Registrar variable de control para que sea visible dentro del bloque
    # No se marca error si ya existe (puede haber varios for anidados con 'i')
    tabla_simbolos.insertar(nombre_var_control, tipo_var_control, categoria='variable')


# --- 6.1 ESTRUCTURA DE DATOS ASIGNADA: ARREGLOS TRADICIONALES ---
# Definido por: Julio Cevallos (Soporta: int[] vec; o int[] vec = new int[5];)
def p_declaracion_arreglo(p):
    '''declaracion_arreglo : tipo_primitivo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR PUNTO_COMA
                           | tipo_primitivo CORCHETE_IZQ CORCHETE_DER IDENTIFICADOR IGUAL NEW tipo_primitivo CORCHETE_IZQ ENTERO CORCHETE_DER PUNTO_COMA'''
    tipo_izq = p[1]
    nombre_arr = p[4]
    linea = p.lineno(4)

    if len(p) == 12:  # Caso de inicialización con instanciación (new)
        tipo_der = p[7]
        if tipo_izq != tipo_der:
            registrar_error_semantico(f"Conflicto de tipos en arreglo. No se puede instanciar un arreglo de tipo '{tipo_izq}[]' con un constructor de '{tipo_der}[]'.", linea)

    if tabla_simbolos.existe(nombre_arr):
        registrar_error_semantico(f"El identificador de arreglo '{nombre_arr}' ya existe en el ámbito actual.", linea)
    else:
        tabla_simbolos.insertar(nombre_arr, tipo_izq, categoria='arreglo')


# --- 6.2 ESTRUCTURA DE DATOS ASIGNADA: LISTAS ---
# Definido por: Steven Barzola (Reglas sintacticas y semanticas)
# Soporta:
#   List<int> numeros;
#   List<string> nombres = new List<string>();
# No soporta anidados: List<List<int>>
def p_declaracion_lista(p):
    '''declaracion_lista : LIST MENOR tipo_primitivo MAYOR IDENTIFICADOR PUNTO_COMA
                         | LIST MENOR tipo_primitivo MAYOR IDENTIFICADOR IGUAL NEW LIST MENOR tipo_primitivo MAYOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''
    tipo_izq = p[3]
    nombre_lista = p[5]
    linea = p.lineno(5)

    if len(p) == 15:
        tipo_der = p[10]
        if tipo_izq != tipo_der:
            registrar_error_semantico(f"Conflicto de tipos en lista. No se puede instanciar 'List<{tipo_izq}>' con un constructor 'List<{tipo_der}>'.", linea)

    if tabla_simbolos.existe(nombre_lista):
        registrar_error_semantico(f"El identificador de lista '{nombre_lista}' ya existe en el ámbito actual.", linea)
    else:
        tabla_simbolos.insertar(nombre_lista, tipo_izq, categoria='lista')


# --- 6.3 ESTRUCTURA DE DATOS ASIGNADA: DICCIONARIOS ---
# Definido por: Issac Maza
# Soporta:
#   Dictionary<string, int> edades;
#   Dictionary<string, int> edades = new Dictionary<string, int>();
#   Dictionary<int, int> contadores = new Dictionary<int, int>();
#
# REGLA SEMÁNTICA 2 — Issac Maza:
#   Validar que el identificador del diccionario no esté ya declarado
#   en el ámbito actual (no redeclaración). Adicionalmente, cuando se
#   instancia con 'new', los tipos de la declaración y el constructor
#   deben coincidir exactamente.
def p_declaracion_diccionario(p):
    '''declaracion_diccionario : DICTIONARY MENOR STRING COMA INT MAYOR IDENTIFICADOR PUNTO_COMA
                               | DICTIONARY MENOR INT COMA INT MAYOR IDENTIFICADOR PUNTO_COMA
                               | DICTIONARY MENOR STRING COMA INT MAYOR IDENTIFICADOR IGUAL NEW DICTIONARY MENOR STRING COMA INT MAYOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA
                               | DICTIONARY MENOR INT COMA INT MAYOR IDENTIFICADOR IGUAL NEW DICTIONARY MENOR INT COMA INT MAYOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''
 
    # Extraer tipo clave y nombre según variante (con o sin inicialización)
    tipo_clave_izq = p[3].lower()   # 'string' o 'int'
    nombre_dict = p[7]
    linea = p.lineno(7)
 
    # Variante con instanciación: Dictionary<K,V> nombre = new Dictionary<K,V>();
    if len(p) == 19:
        tipo_clave_der = p[12].lower()
        if tipo_clave_izq != tipo_clave_der:
            registrar_error_semantico(
                f"Conflicto de tipos en diccionario '{nombre_dict}'. "
                f"No se puede instanciar 'Dictionary<{tipo_clave_izq}, int>' "
                f"con un constructor 'Dictionary<{tipo_clave_der}, int>'.",
                linea
            )
 
    # Regla semántica 2: no redeclaración
    if tabla_simbolos.existe(nombre_dict):
        registrar_error_semantico(
            f"El identificador de diccionario '{nombre_dict}' "
            f"ya existe en el ámbito actual.",
            linea
        )
    else:
        tabla_simbolos.insertar(nombre_dict, tipo_clave_izq, categoria='diccionario')


# --- 7.1 TIPO DE FUNCIÓN ASIGNADA: METODO MAIN ESTRUCTURAL ---
# Definido por: Julio Cevallos
# Main quemado como token reservado (Steven Barzola) para mayor precisión
def p_metodo_main(p):
    '''metodo_main : STATIC VOID MAIN PARENTESIS_IZQ PARENTESIS_DER bloque'''
    pass


# --- 7.2 TIPO DE FUNCIÓN ASIGNADA: METODOS SIN RETORNO ---
# Definido por: Steven Barzola (Reglas sintacticas y semanticas)
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
    global tipo_retorno_actual

    nombre_metodo = p[2] if len(p) == 7 else p[3]
    linea = p.lineno(2) if len(p) == 7 else p.lineno(3)

    tipo_retorno_actual = None  # Caso sin retorno

    if tabla_simbolos.existe(nombre_metodo):
        registrar_error_semantico(f"El identificador de metodo '{nombre_metodo}' ya existe en el ámbito actual.", linea)
    else:
        tabla_simbolos.insertar(nombre_metodo, 'void', categoria='metodo')

    tipo_retorno_actual = None  # Limpiar al salir


# --- 7.3 TIPO DE FUNCIÓN ASIGNADA: FUNCIONES CON RETORNO ---
# Definido por: Issac Maza
# Soporta:
#   int CalcularSuma(int a, int b) { return a + b; }
#   float CalcularPromedio(float total, int cantidad) { return total / cantidad; }
#   int Duplicar(int n) => n*2;   (expresión lambda)
# Nota: alternativas VOID excluidas, cubiertas por p_metodo_void (Steven Barzola)
# Regla Semántica 3a — Issac Maza:
#   Registrar la función en la tabla de símbolos con su tipo de retorno.
#   Marcar tipo_retorno_actual para que p_sentencia_return lo valide.
#   Para funciones lambda (=>), validar directamente el tipo de la expresión.
def p_declaracion_funcion(p):
    '''declaracion_funcion : tipo_primitivo IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER bloque
                           | tipo_primitivo IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER FLECHA_LAMBDA expresion PUNTO_COMA'''
    global tipo_retorno_actual

    tipo_retorno = p[1]
    nombre_func = p[2]
    linea = p.lineno(2)

    # Registrar la función en la tabla de símbolos
    if tabla_simbolos.existe(nombre_func):
        registrar_error_semantico(
            f"El identificador de función '{nombre_func}' "
            f"ya existe en el ámbito actual.",
            linea
        )
    else:
        tabla_simbolos.insertar(nombre_func, tipo_retorno, categoria='metodo')

    # Caso lambda: int Duplicar(int n) => n*2;
    if len(p) == 9:
        tipo_expr_lambda = p[7]
        if tipo_expr_lambda != 'error' and tipo_expr_lambda != tipo_retorno:
            if not (tipo_retorno == 'float' and tipo_expr_lambda == 'int'):
                registrar_error_semantico(
                    f"La expresión lambda de '{nombre_func}' retorna '{tipo_expr_lambda}' "
                    f"pero la función declara retornar '{tipo_retorno}'.",
                    linea
                )
        # Lambda no tiene bloque, limpiar después de validar
        tipo_retorno_actual = None
    else:
        # Función con bloque: marcar tipo esperado ANTES de procesar el bloque
        # NOTA: En LALR el bloque ya fue procesado cuando llegamos aquí,
        # por eso tipo_retorno_actual se setea para la SIGUIENTE función.
        # La limitación real es que PLY procesa bottom-up.
        # La solución parcial: al menos registramos para detectar returns sueltos.
        tipo_retorno_actual = None  # Limpiar al salir del bloque


# Regla Semantica 3b Sentencia return — Definido por: Issac Maza
#   Validar que el tipo del valor retornado por 'return' coincida con el tipo
#   declarado en la firma de la función actualmente en procesamiento.
#   En funciones void (tipo_retorno_actual == None), 'return expr;' es un error.
def p_sentencia_return(p):
    '''sentencia_return : RETURN expresion PUNTO_COMA
                        | RETURN PUNTO_COMA'''
    global tipo_retorno_actual
    linea = p.lineno(1)
 
    # Caso: return con valor (RETURN expresion PUNTO_COMA)
    if len(p) == 4:
        tipo_retornado = p[2]
 
        if tipo_retorno_actual is None:
            # Estamos en un void o fuera de función: no se esperaba valor
            registrar_error_semantico(
                "Sentencia 'return' con valor en un método que no retorna ningun tipo (void) o fuera de una función.",
                linea
            )
        elif tipo_retornado != 'error' and tipo_retornado != tipo_retorno_actual:
            # Coerción implícita int → float permitida
            if not (tipo_retorno_actual == 'float' and tipo_retornado == 'int'):
                registrar_error_semantico(
                    f"Tipo de retorno incorrecto: la función declara retornar "
                    f"'{tipo_retorno_actual}' pero se encontró '{tipo_retornado}'.",
                    linea
                )


# Llamada a función como sentencia — Definido por: Issac Maza
# Ej: LimpiarPantalla(); o CalcularSuma(a, b);
#Modificado por Issac Maza
def p_llamada_funcion_stmt(p):
    '''llamada_funcion_stmt : IDENTIFICADOR PARENTESIS_IZQ argumentos PARENTESIS_DER PUNTO_COMA
                            | IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER PUNTO_COMA'''
    nombre_func = p[1]
    linea = p.lineno(1)
    if not tabla_simbolos.existe(nombre_func):
        registrar_error_semantico(
            f"Llamada a función no declarada '{nombre_func}'.", linea
        )


# Llamada a función dentro de expresiones — Definido por: Issac Maza
# Ej: int x = CalcularSuma(a, b);
#Modificado por Issac Maza
def p_llamada_funcion_expr(p):
    '''llamada_funcion_expr : IDENTIFICADOR PARENTESIS_IZQ argumentos PARENTESIS_DER
                            | IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER'''
    nombre_func = p[1]
    linea = p.lineno(1)
    if tabla_simbolos.existe(nombre_func):
        p[0] = tabla_simbolos.obtener_tipo(nombre_func)
    else:
        registrar_error_semantico(
            f"Llamada a función no declarada '{nombre_func}'.", linea
        )
        p[0] = 'error'


# Argumentos al llamar una función — Definido por: Issac Maza
def p_argumentos(p):
    '''argumentos : argumentos COMA expresion
                  | expresion'''
    pass


# --- REGLAS DE PARÁMETROS (compartidas por metodo_void y declaracion_funcion) ---
# Estructura base: Steven Barzola (lista_parametros + empty)
# Reutilizada por: Issac Maza
#tiene pass, correcto. La semántica está en p_parametro.
def p_parametros(p):
    '''parametros : lista_parametros
                  | empty'''
    pass

#tiene pass, correcto. La semántica está en p_parametro.
def p_lista_parametros(p):
    '''lista_parametros : lista_parametros COMA parametro
                        | parametro'''
    pass


def p_parametro(p):
    '''parametro : tipo_primitivo IDENTIFICADOR'''
    # Registrar parametro como variable para que sea visible dentro del bloque
    # Definido por: Issac Maza
    tabla_simbolos.insertar(p[2], p[1], categoria='variable')


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


def generar_log_sintactico(archivo_codigo, usuario_git):
    global errores_sintacticos
    errores_sintacticos = []

    #if not os.path.exists(archivo_codigo):
    #    print(f"Error: El archivo {archivo_codigo} no existe.")
    #    return
    #with open(archivo_codigo, 'r', encoding='utf-8') as f:
    #    data = f.read()
    # Ejecutar el parser sobre el código de prueba
    #parser.parse(data)

    # Formatear el reporte de logs
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
    
    print(f"\n Pruebas sintacticas completadas. El log se ha guardado en: {nombre_archivo_log}")


# =============================================================================
# Función para escribir el archivo de LOG SEMÁNTICO
# =============================================================================
def generar_log_semantico(archivo_codigo, usuario_git):
    contenido_log = f"--- LOG ANÁLISIS SEMÁNTICO ---\n"
    contenido_log += f"Archivo de código probado: {archivo_codigo}\n"
    contenido_log += f"Desarrollador Responsable: {usuario_git}\n"
    contenido_log += f"Fecha y Hora: {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}\n"
    contenido_log += "=" * 60 + "\n\n"

    if errores_semanticos:
        contenido_log += f"ESTADO DEL ANÁLISIS: RECHAZADO ({len(errores_semanticos)} errores semánticos detectados)\n\n"
        contenido_log += "DETALLE DE INFRACCIONES DE REGLAS DE NEGOCIO:\n"
        for error in errores_semanticos:
            contenido_log += f"- {error}\n"
    else:
        contenido_log += "ESTADO: EXITOSO (0 errores semántico detectados).\n"

    fecha_hora_formato = datetime.now().strftime("%d%m%Y-%Hh%M")
    nombre_archivo_log = f"logs/semantico-{usuario_git}-{fecha_hora_formato}.txt"

    os.makedirs('logs', exist_ok=True)
    with open(nombre_archivo_log, 'w', encoding='utf-8') as f:
        f.write(contenido_log)
    print(f"\n Pruebas semánticas completadas. El log se ha guardado en: {nombre_archivo_log}")


# =============================================================================
# Función para escribir el archivo de LOG SEMÁNTICO
# =============================================================================
def compilar_archivo(archivo_codigo, usuario_git):
    global errores_sintacticos, errores_semanticos
    
    # 1. Limpiar estados anteriores antes de una nueva prueba
    errores_sintacticos = []
    errores_semanticos = []
    tabla_simbolos.limpiar()
    
    if not os.path.exists(archivo_codigo):
        print(f"Error: El archivo {archivo_codigo} no existe.")
        return

    with open(archivo_codigo, 'r', encoding='utf-8') as f:
        data = f.read()

    # 2. Ejecutar la compilación (Esto corre Sintáctico y Semántico al mismo tiempo)
    parser.parse(data)

    # 3. Generar reportes por separado
    generar_log_sintactico(archivo_codigo, usuario_git) #Que siga funcionando bien
    
    # Al parecer en los compiladores, si la sintaxis está totalmente rota,
    # el árbol semántico no es confiable. Sin embargo, se puede generar el log igualmente.
    # TENERLO EN CUENTA para la interfaz gráfica...
    generar_log_semantico(archivo_codigo, usuario_git)


# =============================================================================
# EJECUCIÓN DE PRUEBAS
# =============================================================================
if __name__ == "__main__":
    #compilar_archivo("algoritmos/algoritmo_julio.cs", "JulioCevallos")
    compilar_archivo("algoritmos/algoritmo_semantico_IssacMaza.cs", "IssacMaza")
    #compilar_archivo("algoritmos/algoritmo2_semantico_sintactico_steven.cs", "StevenBarzola")
    print("Para que corra el programa")