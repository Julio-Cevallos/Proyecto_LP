/* =========================================================
   Archivo de Pruebas Sintácticas: Julio Cevallos
   ========================================================= */

static void Main() {
    // 1. Prueba de Declaración y Tipos de Datos Primitivos
    int edad = 20;
    float pesoInicial = 75.5;
    string nombreUsuario = "Julio_Cevallos";
    bool estadoActivo = true;
    bool estadoInactivo = false;

    // PRUEBA FALTANTE: Operador lógico NOT (!)
    bool estadoNegado = !estadoActivo;

    // 2. Prueba de Declaración Múltiple en una línea (¡Implementado con comas!)
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

    // 5. Prueba de Estructura de Datos (Arreglos)
    int[] vec = new int[5];
    int[] vecVacio; // PRUEBA FALTANTE: Declaración simple de arreglo

    // 6. Prueba de Estructura de Control (Bucle While)
    while (a > 2) {
        a = a + 1;
    }

    // 7. Prueba Global: Impresión (Write/WriteLine) y Solicitud de Datos
    Console.Write("Ingrese un nuevo valor: ");
    string entrada = Console.ReadLine();
    
    // PRUEBA FALTANTE: Uso de WriteLine
    Console.WriteLine("Análisis completado con éxito.");
}