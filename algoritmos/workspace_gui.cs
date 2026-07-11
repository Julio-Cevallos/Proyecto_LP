using System;

namespace AnalizadorDemo {

    public class Calculadora {

        private int resultado;

        public static void Sumar(int a, int b) {
            resultado = a + b;
            return resultado;
        }

        private bool EsPositivo(float num) {
            if (num > 0) {
                return true;
            } else {
                return false;
            }
        }
    }
}