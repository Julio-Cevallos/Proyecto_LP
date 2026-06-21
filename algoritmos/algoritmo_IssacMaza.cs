/* =============================================================
   Algoritmo de prueba — Issac Alexander Maza Punine
   Cubre: Bucle for, estructuras de datos complejas
          (arreglos, listas, diccionarios) y declaracion
          de funciones con validacion de retornos.
   ============================================================= */

//  1. Declaracion de funciones con retorno tipado 

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

//  2. Variables globales 

int suma = 0;
float promedio = 0.0;

// 3. Arreglo unidimensional 

int[] notas = new int[5];

//  4. Bucle for valido: variable de control entera 

for (int i = 0; i < 5; i = i + 1) {
    suma = CalcularSuma(suma, i);
}

// 5. Lista dinamica 

List<int> numeros = new List<int>();

//  6. Diccionario clave-valor 

Dictionary<string, int> edades = new Dictionary<string, int>();

//  7. Impresion de resultados 

Console.Write("Suma total: " + suma);
Console.Write("Promedio: " + promedio);

//  8. ERRORES SEMANTICOS INTENCIONALES 

// Error 1: retorno de tipo incorrecto (declara int, retorna string)
int FuncionConErrorDeRetorno(int x) {
    return "texto_invalido";
}

// Error 2: bucle for con variable de control de tipo string
for (string s = "inicio"; s != "fin"; s = s + "x") {
    suma = suma + 1;
}

// Error 3: estructura de datos con tipo no reconocido
Stack<int> pila = new Stack<int>();

//  9. ERRORES LEXICOS INTENCIONALES 

int $precio = 100;

float @tasa = 0.5;

string #nombre = "Issac";