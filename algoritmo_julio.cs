/* =========================================================
   Este bloque ignora intencionalmente caracteres ilegales 
   para validar la robustez de las expresiones regulares:
   @, #, $, %, ^, &, ~, ?, ¡, ¿, !, É, á, í, ó, ú
   ========================================================= */

// 1. Prueba de Declaración y Tipos de Datos Primitivos
int edad = 20;
float pesoInicial = 75.5;
string nombreUsuario = "Julio_Cevallos";
bool estadoActivo = true;
bool estadoInactivo = false;

// 2. Prueba de Declaración Múltiple en una línea
float a = 1.5, b = 4.2, c = 3.14;

// 3. Prueba de Operadores Aritméticos y Agrupación con Paréntesis
int suma = (10 + 5) - 2;
float multiplicacion = (a * b) + c;
float division = pesoInicial / 2.0;
int modulo = 15 % 4;

// 4. Prueba de Operadores Relacionales
bool esMayor = a > b;
bool esMenorIgual = c <= 5.0;
bool esIgual = edad == 20;
bool esDiferente = (suma != 10);
bool esMayorIgual = (pesoInicial >= 70.0);

// 5. Prueba Global: Impresión y Solicitud de Datos
// Utiliza el punto (.) y los paréntesis para métodos del sistema
Console.Write("Ingrese un nuevo valor: ");
string entrada = Console.ReadLine();