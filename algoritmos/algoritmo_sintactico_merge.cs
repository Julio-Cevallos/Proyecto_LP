using System;

// =====================================================
// PRUEBAS GENERALES (Steven Barzola - cambios globales)
// =====================================================

// --- using y bloque vacio ---
static void Main()
{
    // --- Tipos primitivos y declaracion multiple (Julio) ---
    int x = 10, y = 20, z;
    float precio = 3.14;
    bool activo = true;
    string nombre = "Steven";
    char letra = 'A';

    // --- var (Steven) ---
    var mensaje = "Proyecto LP";
    var total = 99;

    // --- Asignacion simple ---
    x = x + 1;
    total = total * 2;

    // --- Expresiones booleanas complejas (Julio/Steven) ---
    bool resultado = !activo && (x > 0 || total == 99);

    // --- Console I/O (Julio) ---
    Console.WriteLine("Inicio del programa");
    Console.Write(total);
    string entrada = Console.ReadLine();

    // =====================================================
    // ESTRUCTURA DE CONTROL: IF / ELSE IF / ELSE (Steven)
    // =====================================================

    if (x > 10)
    {
        Console.WriteLine("x es mayor que 10");
    }
    else if (x == 10)
    {
        Console.WriteLine("x es exactamente 10");
    }
    else
    {
        Console.WriteLine("x es menor que 10");
    }

    // --- Bloque vacio (Steven) ---
    if (activo)
    {
    }

    // --- IF anidado ---
    if (x > 0)
    {
        if (total > 50)
        {
            Console.WriteLine("x positivo y total alto");
        }
    }

    // =====================================================
    // ESTRUCTURA DE DATOS: LISTA (Steven)
    // =====================================================

    List<int> numeros;
    List<string> nombres = new List<string>();
    List<float> precios = new List<float>();
    List<bool> flags;

    // =====================================================
    // METODOS SIN RETORNO (Steven)
    // =====================================================
}

void Saludar()
{
    Console.WriteLine("Hola!");
}

void Imprimir(string texto)
{
    Console.WriteLine(texto);
}

public void Ejecutar(int cantidad, bool activo)
{
    Console.WriteLine(cantidad);
}

private void Limpiar()
{
}

// =====================================================
// ESTRUCTURA DE CONTROL: FOR (Isaac)
// =====================================================

void PruebaFor()
{
    int suma = 0;
    for (int i = 0; i < 10; i = i + 1)
    {
        suma = suma + i;
    }
    Console.WriteLine(suma);
}

// =====================================================
// ESTRUCTURA DE DATOS: DICCIONARIO (Isaac)
// =====================================================

void PruebaDiccionario()
{
    Dictionary<string, int> edades;
    Dictionary<int, int> conteo = new Dictionary<int, int>();
    Dictionary<string, int> notas = new Dictionary<string, int>();
}

// =====================================================
// FUNCIONES CON RETORNO Y LAMBDA (Isaac)
// =====================================================

int CalcularSuma(int a, int b)
{
    return a + b;
}

float CalcularPromedio(float total, int cantidad)
{
    return total / cantidad;
}

int Duplicar(int n) => n * 2;

// =====================================================
// LLAMADAS A FUNCION (Isaac)
// =====================================================

void PruebaLlamadas()
{
    Saludar();
    Imprimir("hola");
    int resultado = CalcularSuma(5, 3);
    Console.WriteLine(resultado);
}

// =====================================================
// ARREGLOS (Julio)
// =====================================================

void PruebaArreglos()
{
    int[] notas;
    float[] precios = new float[5];
}

// =====================================================
// WHILE (Julio)
// =====================================================

void PruebaWhile()
{
    int contador = 0;
    while (contador < 10)
    {
        contador = contador + 1;
    }
}

// =====================================================
// ERRORES A PROPOSITO
// =====================================================

// ERROR 1: falta punto y coma
void ErrorUno()
{
    int x = 5
    Console.WriteLine(x);
}

// ERROR 2: if sin condicion
void ErrorDos()
{
    if ()
    {
        Console.WriteLine("mal");
    }
}

// ERROR 3: llave de cierre faltante
void ErrorTres()
{
    int y = 10;