using System;

// =========================================================
// ARCHIVO DE PRUEBA - ANÁLISIS SEMÁNTICO
// Desarrollador: Steven Barzola
// Cubre: declaraciones, var, if, while, listas, métodos void,
//        operaciones, conversión implícita y errores intencionales
// =========================================================

// --- BLOQUE 1: DECLARACIONES PRIMITIVAS Y REDECLARACIÓN ---
// [OK] Declaraciones válidas
int edad = 25;
float precio = 3.14;
string nombre = "Steven";
bool activo = true;
char inicial = 'S';

// [ERROR] Redeclaración de variable ya existente
int edad = 30;

// [OK] Coerción implícita válida: int -> float
float resultado = 10;

// [ERROR] Conversión implícita inválida: string -> int
int codigo = "hola";

// [ERROR] Conversión implícita inválida: bool -> float
float porcentaje = true;


// --- BLOQUE 2: VAR - INFERENCIA DE TIPO ---
// [OK] var infiere correctamente el tipo
var contador = 100;
var mensaje = "Bienvenido";
var bandera = false;

// [ERROR] Redeclaración con var de variable ya existente
var edad = 99;

// [OK] var con expresión aritmética
var total = 5 + 3;


// --- BLOQUE 3: ASIGNACIONES Y VARIABLES NO DECLARADAS ---
// [OK] Reasignación válida
edad = 26;
precio = 9.99;

// [ERROR] Asignación a variable no declarada
sueldo = 1500;

// [ERROR] Reasignación con tipo incompatible
activo = 42;

// [OK] Reasignación con coerción válida int -> float
precio = 5;


// --- BLOQUE 4: OPERACIONES ARITMÉTICAS ---
// [OK] Operaciones válidas entre numéricos
int suma = 10 + 5;
float division = 10 / 2;

// [ERROR] Operación aritmética inválida: string * int
var invalido = "texto" * 5;

// [ERROR] Operación aritmética inválida: bool - int
var otro = true - 1;

// [OK] Concatenación de strings con +
string saludo = "Hola " + "mundo";


// --- BLOQUE 5: OPERACIONES RELACIONALES Y LÓGICAS ---
// [OK] Comparaciones válidas
bool esMayor = edad > 18;
bool sonIguales = precio == 9.99;

// [ERROR] Comparación inválida entre tipos incompatibles
bool comparacion = nombre > 10;

// [OK] Operadores lógicos entre bool
bool resultado2 = activo && esMayor;

// [ERROR] Operador lógico con tipo no bool
bool logicaMal = edad && activo;

// [OK] Negación de bool
bool negado = !activo;

// [ERROR] Negación aplicada a int
bool negadoMal = !edad;


// --- BLOQUE 6: ESTRUCTURA IF ---
// [OK] Condición booleana válida
if (activo) {
    int x = 1;
}

// [OK] if/else válido
if (edad > 18) {
    string estado = "mayor";
} else {
    string estado = "menor"; //Nuestro caso da error porque se consideran variables globales
}

// [ERROR] Condición de if con tipo int (no bool)
if (edad) {
    int y = 2;
}

// [ERROR] Condición de if con tipo string
if (nombre) {
    int z = 3;
}

// [OK] else if encadenado válido
if (edad < 18) {
    string rango = "joven";
} else if (edad < 65) {
    string rango = "adulto"; //Nuestro caso da error porque se consideran variables globales
} else {
    string rango = "mayor"; //Nuestro caso da error porque se consideran variables globales
}


// --- BLOQUE 7: BUCLE WHILE ---
// [OK] Condición bool válida
int i = 0;
while (i > 0) {
    i = i + 1;
}

// [ERROR] Condición while con tipo int
while (contador) {
    contador = contador + 1;
}

// [OK] Condición while con expresión relacional
while (edad < 100) {
    edad = edad + 1;
}


// --- BLOQUE 8: LISTAS ---
// [OK] Declaración simple de lista
List<int> numeros;

// [OK] Declaración con inicialización consistente
List<string> nombres = new List<string>();

// [ERROR] Conflicto de tipos en lista: List<int> inicializada con List<float>
List<int> enteros = new List<float>();

// [ERROR] Redeclaración de lista ya existente
List<string> nombres = new List<string>();


// --- BLOQUE 9: ARREGLOS ---
// [OK] Arreglo simple
int[] edades;

// [OK] Arreglo con instanciación consistente
float[] precios = new float[10];

// [ERROR] Conflicto de tipos en arreglo
int[] valores = new float[5];

// [ERROR] Redeclaración de arreglo
int[] edades;


// --- BLOQUE 10: MÉTODOS VOID ---
// [OK] Método void simple
void Saludar() {
    string msg = "Hola";
    Console.WriteLine(msg);
}

// [OK] Método void con parámetros y modificador de acceso
public void Mostrar(int valor, bool flag) {
    Console.WriteLine(valor); //Da error porque mientras se hace esto, no se ha implementado semantica a que reconozca parametros localmente (solo globales)
}

// [ERROR] Redeclaración de método void ya existente
void Saludar() { //Ademas de este error
    string msg = "Adios"; //Nuestro caso, esto tambien da error porque se consideran variables globales
}

// [OK] Método void privado
private void Limpiar() {}


// --- BLOQUE 11: IMPRESIÓN ---
// [OK] Console.WriteLine con expresión válida
Console.WriteLine(nombre);
Console.WriteLine(edad + 1);

// [OK] Console.Write con string
Console.Write("Valor: ");