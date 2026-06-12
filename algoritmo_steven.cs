// Comentario simple

/* Comentario
   multilinea */

int x = 10;
float y = 3.14;
bool activo = true;
string nombre = "Julio";
char letra = 'A';

int[] numeros = {1, 2, 3, 4, 5};
int primero = numeros[0];

if (x >= 5 && activo != false) {
    x = x + 1;
}

while (x < 20 || activo) {
    x = x * 2;
}

for (int i = 0; i < 10; i = i + 1) {
    y = y % 2;
}

void miFuncion() {
    return;
}

List<int> lista = new List<int>();
Dictionary<string, int> mapa = new Dictionary<string, int>();

// ===== SECCIÓN DE ERRORES LEXICOS INTENCIONALES =====

// Caracteres especiales no definidos
int $ = 5;
float @precio;
string # = "x";
int ^x = 3;

// Símbolo de pregunta no definido
bool activo? = true;

// Pipe simple (no es ||)
bool resultado = true | false;

// Ampersand simple (no es &&)
bool otro = true & false;

// Tilde no definida
int teléfono = 0985533;
