import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime

# Importación del motor del compilador desarrollado por el grupo
import lexer
import parser


class InterfazCompilador:
    def __init__(self, root):
        self.root = root
        self.root.title("C# Compiler IDE - Panel de Control Semántico")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        # Nombre por defecto para el log (Julio Cevallos)
        self.usuario_git = "JulioCevallos"
        self.archivo_temporal = "algoritmos/workspace_gui.cs"

        self.crear_componentes()
        self.configurar_eventos()
        # Cargar una plantilla inicial en el editor
        self.cargar_plantilla_inicial()

    def crear_componentes(self):
        # -----------------------------------------------------------------
        # 1. BARRA DE HERRAMIENTAS SUPERIOR (BOTONES DE ACCIÓN)
        # -----------------------------------------------------------------
        toolbar = ttk.Frame(self.root, padding=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open = ttk.Button(toolbar, text="Abrir Archivo (.cs)", command=self.abrir_archivo)
        btn_open.pack(side=tk.LEFT, padx=5)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        btn_lex = ttk.Button(toolbar, text="Analizar Léxico", command=self.ejecutar_lexico)
        btn_lex.pack(side=tk.LEFT, padx=5)

        btn_sin = ttk.Button(toolbar, text="Analizar Sintáctico", command=self.ejecutar_sintactico)
        btn_sin.pack(side=tk.LEFT, padx=5)

        btn_sem = ttk.Button(toolbar, text="Analizar Semántico", command=self.ejecutar_semantico)
        btn_sem.pack(side=tk.LEFT, padx=5)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Botón principal destacado
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        btn_all = ttk.Button(toolbar, text="COMPILAR TODO", style="Accent.TButton", command=self.compilar_todo)
        btn_all.pack(side=tk.LEFT, padx=5)

        # -----------------------------------------------------------------
        # 2. PANEL PRINCIPAL DIVIDIDO (LADO A LADO)
        # -----------------------------------------------------------------
        panel_dividido = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        panel_dividido.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- LADO IZQUIERDO: SECCIÓN DE ESCRITURA DE CÓDIGO ---
        frame_izquierdo = ttk.LabelFrame(panel_dividido, text=" Editor de Código C# ", padding=5)
        panel_dividido.add(frame_izquierdo, weight=1)

        # Contenedor para scrollbars y números de línea
        contenedor_editor = ttk.Frame(frame_izquierdo)
        contenedor_editor.pack(fill=tk.BOTH, expand=True)

        # Lienzo para números de línea
        self.line_canvas = tk.Canvas(contenedor_editor, width=35, bg="#f0f0f0", bd=0, highlightthickness=0)
        self.line_canvas.pack(side=tk.LEFT, fill=tk.Y)

        # Scrollbar vertical del editor
        scroll_y = ttk.Scrollbar(contenedor_editor)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Editor de Texto Principal
        self.txt_editor = tk.Text(
            contenedor_editor,
            wrap=tk.NONE,
            yscrollcommand=scroll_y.set,
            font=("Consolas", 11),
            undo=True,
            bg="#ffffff",
            fg="#000000",
            insertbackground="black"
        )
        self.txt_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.txt_editor.yview)

        # Scrollbar horizontal del editor
        scroll_x = ttk.Scrollbar(frame_izquierdo, orient=tk.HORIZONTAL, command=self.txt_editor.xview)
        self.txt_editor.config(xscrollcommand=scroll_x.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # --- LADO DERECHO: CENTRO DE DIAGNÓSTICO (LOGS) ---
        frame_derecho = ttk.LabelFrame(panel_dividido, text=" Diagnóstico y Reportes del Sistema ", padding=5)
        panel_dividido.add(frame_derecho, weight=1)

        # Notebook (Control de Pestañas)
        self.notebook = ttk.Notebook(frame_derecho)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Estilo para las consolas oscuras
        config_consola = {
            "bg": "#1e1e1e",
            "fg": "#d4d4d4",
            "insertbackground": "white",
            "font": ("Consolas", 10),
            "wrap": tk.WORD
        }

        # Pestaña 1: Log Léxico
        self.tab_lexico = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_lexico, text="Log Léxico ")
        self.txt_log_lexico = tk.Text(self.tab_lexico, **config_consola)
        self.txt_log_lexico.pack(fill=tk.BOTH, expand=True)

        # Pestaña 2: Log Sintáctico
        self.tab_sintactico = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sintactico, text="Log Sintáctico ")
        self.txt_log_sintactico = tk.Text(self.tab_sintactico, **config_consola)
        self.txt_log_sintactico.pack(fill=tk.BOTH, expand=True)

        # Pestaña 3: Log Semántico
        self.tab_semantico = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_semantico, text="Log Semántico ")
        self.txt_log_semantico = tk.Text(self.tab_semantico, **config_consola)
        self.txt_log_semantico.pack(fill=tk.BOTH, expand=True)

    def configurar_eventos(self):
        # Sincronizar el scrollbar y eventos de teclado con el rediseño de números de línea
        self.txt_editor.bind("<KeyRelease>", self.actualizar_lineas)
        self.txt_editor.bind("<Configure>", self.actualizar_lineas)
        self.txt_editor.bind("<MouseWheel>", self.actualizar_lineas)
        self.txt_editor.bind("<<Modified>>", self.actualizar_lineas)

    def actualizar_lineas(self, event=None):
        self.line_canvas.delete("all")
        i = self.txt_editor.index("@0,0")
        while True:
            dline = self.txt_editor.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            num_linea = str(i).split(".")[0]
            self.line_canvas.create_text(32, y, anchor="ne", text=num_linea, fill="#757575", font=("Consolas", 10))
            i = self.txt_editor.index(f"{i}+1line")
        self.txt_editor.edit_modified(False)

    def obtener_codigo(self):
        """Única fuente de verdad para el texto a analizar."""
        return self.txt_editor.get("1.0", tk.END).strip()

    def guardar_codigo_temporal(self):
        """Guarda el texto actual del editor en un archivo físico para que los analizadores lo lean."""
        os.makedirs("algoritmos", exist_ok=True)
        codigo = self.obtener_codigo()
        with open(self.archivo_temporal, "w", encoding="utf-8") as f:
            f.write(codigo)

    def cargar_plantilla_inicial(self):
        plantilla = (
            "using System;\n\n"
            "int control = 12;\n"
            "float umbral = 24.5;\n"
            "string tag = \"Procesando\";\n\n"
            "while (control < umbral) {\n"
            "    control = control + 2;\n"
            "}"
        )
        self.txt_editor.insert("1.0", plantilla)
        self.actualizar_lineas()

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos C#", "*.cs"), ("Archivos de texto", "*.txt")])
        if ruta:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            self.txt_editor.delete("1.0", tk.END)
            self.txt_editor.insert("1.0", contenido)
            self.actualizar_lineas()
            messagebox.showinfo("Éxito", f"Archivo cargado correctamente:\n{os.path.basename(ruta)}")

    def _correr_lexico(self, codigo):
        """Corre el lexer una sola vez sobre 'codigo' y arma el texto del panel."""
        lexer.errores_lexicos = []
        # FIX: Resetear numero de lineas
        lexer.lexer.lineno = 1
        lexer.lexer.input(codigo)

        resultado = "TOKENS RECONOCIDOS:\n"
        while True:
            tok = lexer.lexer.token()
            if not tok:
                break
            resultado += f"Token: {tok.type:15} | Valor: '{tok.value}'; Línea: {tok.lineno}\n"
        resultado += "\nERRORES LÉXICOS:\n"
        if lexer.errores_lexicos:
            for err in lexer.errores_lexicos:
                resultado += f"❌ {err}\n"
        else:
            resultado += "Ninguno. Sintaxis léxica correcta.\n"

        return resultado

    def _formatear_panel_sintactico(self, errores_sintacticos):
        if errores_sintacticos:
            resultado = f"ESTADO: RECHAZADO ({len(errores_sintacticos)} errores encontrados)\n\n"
            for err in errores_sintacticos:
                resultado += f"❌ {err}\n"
        else:
            resultado = "ESTADO: EXITOSO (0 errores sintácticos detectados).\n\n"
        return resultado

    def _formatear_panel_semantico(self, errores_semanticos, errores_sintacticos):
        resultado = ""
        if errores_sintacticos:
            # Si hubo errores sintácticos, parte del árbol se construyó por
            # recuperación de errores (ver p_sentencia_error)
            # Avisar que el resultado semántico puede no ser confiable
            resultado += (
                "ADVERTENCIA: se detectaron errores sintácticos. Los resultados\n"
                "semánticos pueden no ser confiables, ya que parte del\n"
                "código se procesó mediante recuperación de errores.\n\n"
            )
        if errores_semanticos:
            resultado += f"ESTADO: RECHAZADO ({len(errores_semanticos)} infracciones de tipo/contexto)\n\n"
            for err in errores_semanticos:
                resultado += f"❌ {err}\n"
        else:
            resultado += "ESTADO: EXITOSO (0 errores semánticos detectados).\n\n"
        return resultado

    def _correr_sintactico_y_semantico(self, codigo):
        """Corre el parser UNA sola vez (sintáctico + semántico se resuelven
        juntos, ya que este compilador es de una sola pasada) y devuelve el
        texto ya formateado para ambos paneles."""
        parser.errores_sintacticos = []
        parser.errores_semanticos = []
        parser.tabla_simbolos.limpiar()

        # FIX: Rsetear numero de lineas
        lexer.lexer.lineno = 1
        parser.parser.parse(codigo)

        resultado_sin = self._formatear_panel_sintactico(parser.errores_sintacticos)
        resultado_sem = self._formatear_panel_semantico(parser.errores_semanticos, parser.errores_sintacticos)
        return resultado_sin, resultado_sem

    # -----------------------------------------------------------------
    # EJECUCIÓN DE LOGS INDEPENDIENTES EN LA INTERFAZ (botones sueltos)
    # -----------------------------------------------------------------

    def ejecutar_lexico(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        resultado = self._correr_lexico(codigo)

        self.txt_log_lexico.delete("1.0", tk.END)
        self.txt_log_lexico.insert("1.0", resultado)
        self.notebook.select(self.tab_lexico)  # Enfocar pestaña

    def ejecutar_sintactico(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        resultado_sin, resultado_sem = self._correr_sintactico_y_semantico(codigo)

        self.txt_log_sintactico.delete("1.0", tk.END)
        self.txt_log_sintactico.insert("1.0", resultado_sin)
        self.txt_log_semantico.delete("1.0", tk.END)
        self.txt_log_semantico.insert("1.0", resultado_sem)
        self.notebook.select(self.tab_sintactico)  # Enfocar pestaña

    def ejecutar_semantico(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        resultado_sin, resultado_sem = self._correr_sintactico_y_semantico(codigo)

        self.txt_log_sintactico.delete("1.0", tk.END)
        self.txt_log_sintactico.insert("1.0", resultado_sin)
        self.txt_log_semantico.delete("1.0", tk.END)
        self.txt_log_semantico.insert("1.0", resultado_sem)
        self.notebook.select(self.tab_semantico)  # Enfocar pestaña

    # -----------------------------------------------------------------
    # PIPELINE COMPLETO: GUARDA LOS ARCHIVOS DE TEXTO EXIGIDOS
    # -----------------------------------------------------------------
    def compilar_todo(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        # 1. Generar los logs físicos reglamentarios en /logs/
        resultado_lexico = lexer.validar_algoritmo(self.archivo_temporal, self.usuario_git)
        parser.compilar_archivo(self.archivo_temporal, self.usuario_git)

        # 2. Mostrar en los paneles EXACTAMENTE lo que se acaba de calcular,
        #    sin volver a correr el lexer ni el parser.
        self.txt_log_lexico.delete("1.0", tk.END)
        self.txt_log_lexico.insert("1.0", resultado_lexico)

        resultado_sin = self._formatear_panel_sintactico(parser.errores_sintacticos)
        self.txt_log_sintactico.delete("1.0", tk.END)
        self.txt_log_sintactico.insert("1.0", resultado_sin)

        resultado_sem = self._formatear_panel_semantico(parser.errores_semanticos, parser.errores_sintacticos)
        self.txt_log_semantico.delete("1.0", tk.END)
        self.txt_log_semantico.insert("1.0", resultado_sem)

        messagebox.showinfo(
            "Compilación Completada",
            f"Análisis finalizado para las 3 fases.\n\n"
            f"Los logs físicos reglamentarios han sido guardados en la carpeta /logs/"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCompilador(root)
    root.mainloop()