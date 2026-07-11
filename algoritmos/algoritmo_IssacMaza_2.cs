/* =============================================================
   Algoritmo de prueba final — Issac Alexander Maza Punine
   Analizador: Lexico, Sintactico y Semantico
   ============================================================= */

// ============================================================
// SECCION 1: DECLARACION DE FUNCIONES CON RETORNO TIPADO
// Cubre: Tipo de funcion asignado a Issac Maza
// ============================================================

// Funcion valida: retorna int
int CalcularSuma(int a, int b) {
    return a + b;
}

// Funcion valida: retorna float
float CalcularPromedio(float total, int cantidad) {
    return total / cantidad;
}

// Funcion void sin retorno de valor
void MostrarResultado() {
    return;
}

// Funcion lambda valida: retorna int
int Duplicar(int n) => n * 2;

// ============================================================
// SECCION 2: VARIABLES GLOBALES Y TIPOS PRIMITIVOS
// Cubre: tipos base del lexico
// ============================================================

int suma = 0;
float promedio = 0.0;
bool activo = true;
string mensaje = "Resultado";
char letra = 'A';

// ============================================================
// SECCION 3: ARREGLO UNIDIMENSIONAL
// Cubre: estructura de datos de Julio (arreglos)
// ============================================================

int[] notas = new int[5];

// ============================================================
// SECCION 4: BUCLE FOR VALIDO
// Cubre: estructura de control asignada a Issac Maza
// Condicion bool, variable de control entera
// ============================================================

for (int i = 0; i < 5; i = i + 1) {
    suma = CalcularSuma(suma, i);
}

// ============================================================
// SECCION 5: LISTA DINAMICA
// Cubre: estructura de datos de Steven (listas)
// ============================================================

List<int> numeros = new List<int>();

// ============================================================
// SECCION 6: DICCIONARIO CLAVE-VALOR
// Cubre: estructura de datos asignada a Issac Maza
// ============================================================

Dictionary<string, int> edades = new Dictionary<string, int>();

// ============================================================
// SECCION 7: IMPRESION DE RESULTADOS
// Cubre: I/O del lexico y sintactico
// ============================================================

Console.Write("Suma total: " + suma);
Console.Write("Promedio: " + promedio);

// ============================================================
// SECCION 8: ERRORES SEMANTICOS INTENCIONALES
// Cada error activa una regla semantica de Issac Maza
// ============================================================

// Error Semantico 1 [Regla 3b - Retorno incorrecto]:
// La funcion declara retornar int pero el return devuelve string
int FuncionConErrorDeRetorno(int x) {
    return "texto_invalido";
}

// Error Semantico 2 [Regla 1 - Condicion del for debe ser bool]:
// La condicion usa suma + 1 que es de tipo int, no bool
for (int j = 0; suma + 1; j = j + 1) {
    suma = suma + 1;
}

// Error Semantico 3 [Regla 2 - Redeclaracion de diccionario]:
// edades ya fue declarado en la seccion 6, no se puede redeclarar
Dictionary<string, int> edades = new Dictionary<string, int>();

// ============================================================
// SECCION 9: ERRORES LEXICOS INTENCIONALES
// Caracteres no definidos en Mini-C#
// ============================================================

int $precio = 100;
float @tasa = 0.5;
string #nombre = "Issac";