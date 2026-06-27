using System;

// =========================================================
// ARCHIVO DE PRUEBA - ANÁLISIS SEMÁNTICO (SIN ERRORES)
// Desarrollador: Steven Barzola
// =========================================================

// --- BLOQUE 1: DECLARACIONES PRIMITIVAS ---
int edad = 25;
float precio = 3.14;
string nombre = "Steven";
bool activo = true;
char inicial = 'S';

// Coerción implícita válida: int -> float
float resultado = 10;

// Declaración sin inicialización
int contador;


// --- BLOQUE 2: VAR - INFERENCIA DE TIPO ---
var puntos = 100;
var etiqueta = "Bienvenido";
var bandera = false;
var promedio = 8 + 2;


// --- BLOQUE 3: ASIGNACIONES ---
edad = 26;
precio = 9.99;

// Coerción válida int -> float en reasignación
precio = 5;

// Operaciones válidas asignadas
int suma = 10 + 5;
float division = 10 / 2;
string saludo = "Hola " + "mundo";


// --- BLOQUE 4: OPERACIONES RELACIONALES Y LÓGICAS ---
bool esMayor = edad > 18;
bool esIgual = precio == 9.99;
bool combinado = activo && esMayor;
bool negado = !activo;
bool rango = esMayor || bandera;


// --- BLOQUE 5: ESTRUCTURA IF ---
// Variables con nombres únicos por scope plano
if (activo) {
    int valorIf = 1;
}

if (edad > 18) {
    string estadoIf = "mayor";
} else {
    string estadoElse = "menor";
}

if (edad < 18) {
    string rangoJoven = "joven";
} else if (edad < 65) {
    string rangoAdulto = "adulto";
} else {
    string rangoMayor = "mayor";
}


// --- BLOQUE 6: BUCLE WHILE ---
int indice = 0;
while (indice > 0) {
    int iteracion = indice + 1;
}

while (edad < 100) {
    int edadTemp = edad + 1;
}


// --- BLOQUE 7: LISTAS ---
List<int> numeros;
List<string> nombres = new List<string>();
List<bool> flags = new List<bool>();


// --- BLOQUE 8: ARREGLOS ---
int[] edades;
float[] precios = new float[10];
string[] etiquetas = new string[5];


// --- BLOQUE 9: MÉTODOS VOID ---
void Saludar() {
    string msgSaludo = "Hola";
    Console.WriteLine(msgSaludo);
}

public void Mostrar(int valor, bool flag) {
    int valor = 1; //Por ahora no se ha implementado que reconoza el parametro (variables globales)
    Console.WriteLine(valor);
}

private void Limpiar() {}


// --- BLOQUE 10: IMPRESIÓN ---
Console.WriteLine(nombre);
Console.WriteLine(edad + 1);
Console.Write("Precio: ");
Console.WriteLine(precio);