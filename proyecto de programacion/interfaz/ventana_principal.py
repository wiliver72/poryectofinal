import tkinter as tk
from tkinter import messagebox, ttk

from modelos.base import Personaje
from modelos.personajes import Guerrero, Mago, Picaro
from servicios.motor_combate import MotorCombate


class VentanaPrincipal(tk.Tk):
    """Ventana principal basada en Tkinter y callbacks de eventos."""

    COLORES = {
        "fondo": "#10151D",
        "panel": "#171F2A",
        "tarjeta": "#202B38",
        "entrada": "#111923",
        "borde": "#2B3949",
        "texto": "#F2F4F7",
        "secundario": "#A7B1BE",
        "dorado": "#D8AD68",
        "dorado_hover": "#E5BC7D",
        "verde": "#51B88A",
        "rojo": "#D96C72",
    }

    def __init__(self) -> None:
        super().__init__()
        self.title("Arena RPG | Combate por turnos")
        self.geometry("1080x760")
        self.minsize(940, 680)
        self.configure(background=self.COLORES["fondo"], padx=24, pady=20)

        self.motor: MotorCombate | None = None
        self.botones_accion: list[ttk.Button] = []
        self._configurar_estilos()
        self._construir_interfaz()
        self._iniciar_partida()

    def _configurar_estilos(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=self.COLORES["fondo"])
        style.configure("Panel.TFrame", background=self.COLORES["panel"])
        style.configure("TLabel", background=self.COLORES["fondo"], foreground=self.COLORES["texto"])
        style.configure(
            "Title.TLabel",
            font=("TkDefaultFont", 22, "bold"),
            foreground=self.COLORES["texto"],
        )
        style.configure(
            "Subtitle.TLabel",
            font=("TkDefaultFont", 10),
            foreground=self.COLORES["secundario"],
        )
        style.configure(
            "Eyebrow.TLabel",
            font=("TkDefaultFont", 9, "bold"),
            foreground=self.COLORES["dorado"],
        )
        style.configure(
            "Panel.Eyebrow.TLabel",
            background=self.COLORES["panel"],
            font=("TkDefaultFont", 9, "bold"),
            foreground=self.COLORES["dorado"],
        )
        style.configure(
            "Section.TLabel",
            font=("TkDefaultFont", 13, "bold"),
            foreground=self.COLORES["texto"],
        )
        style.configure(
            "Panel.Section.TLabel",
            background=self.COLORES["panel"],
            font=("TkDefaultFont", 13, "bold"),
            foreground=self.COLORES["texto"],
        )
        style.configure(
            "Card.Section.TLabel",
            background=self.COLORES["tarjeta"],
            font=("TkDefaultFont", 13, "bold"),
            foreground=self.COLORES["texto"],
        )
        style.configure(
            "Field.TLabel",
            font=("TkDefaultFont", 10, "bold"),
            foreground=self.COLORES["secundario"],
        )
        style.configure(
            "Panel.Field.TLabel",
            background=self.COLORES["panel"],
            font=("TkDefaultFont", 10, "bold"),
            foreground=self.COLORES["secundario"],
        )
        style.configure(
            "Card.Field.TLabel",
            background=self.COLORES["tarjeta"],
            font=("TkDefaultFont", 10, "bold"),
            foreground=self.COLORES["secundario"],
        )
        style.configure(
            "Panel.Subtitle.TLabel",
            background=self.COLORES["panel"],
            font=("TkDefaultFont", 10),
            foreground=self.COLORES["secundario"],
        )
        style.configure(
            "Card.Subtitle.TLabel",
            background=self.COLORES["tarjeta"],
            font=("TkDefaultFont", 10),
            foreground=self.COLORES["secundario"],
        )
        style.configure(
            "TEntry",
            fieldbackground=self.COLORES["entrada"],
            foreground=self.COLORES["texto"],
            insertcolor=self.COLORES["texto"],
            bordercolor=self.COLORES["borde"],
            padding=9,
        )
        style.configure(
            "TCombobox",
            fieldbackground=self.COLORES["entrada"],
            background=self.COLORES["entrada"],
            foreground=self.COLORES["texto"],
            arrowcolor=self.COLORES["dorado"],
            bordercolor=self.COLORES["borde"],
            padding=8,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.COLORES["entrada"])],
            foreground=[("readonly", self.COLORES["texto"])],
            selectbackground=[("readonly", self.COLORES["entrada"])],
            selectforeground=[("readonly", self.COLORES["texto"])],
        )
        style.configure(
            "Accent.TButton",
            background=self.COLORES["dorado"],
            foreground="#171717",
            font=("TkDefaultFont", 10, "bold"),
            padding=(12, 10),
            borderwidth=0,
        )
        style.map(
            "Accent.TButton",
            background=[
                ("disabled", self.COLORES["borde"]),
                ("active", self.COLORES["dorado_hover"]),
                ("!disabled", self.COLORES["dorado"]),
            ],
            foreground=[("disabled", self.COLORES["secundario"]), ("!disabled", "#171717")],
        )
        style.configure(
            "Action.TButton",
            background=self.COLORES["tarjeta"],
            foreground=self.COLORES["texto"],
            font=("TkDefaultFont", 10, "bold"),
            padding=(9, 12),
            borderwidth=1,
            relief="flat",
        )
        style.map(
            "Action.TButton",
            background=[("disabled", self.COLORES["panel"]), ("active", self.COLORES["borde"])],
            foreground=[("disabled", self.COLORES["secundario"])],
        )
        style.configure(
            "Player.Horizontal.TProgressbar",
            troughcolor=self.COLORES["entrada"],
            background=self.COLORES["verde"],
            bordercolor=self.COLORES["entrada"],
            lightcolor=self.COLORES["verde"],
            darkcolor=self.COLORES["verde"],
            thickness=10,
        )
        style.configure(
            "Enemy.Horizontal.TProgressbar",
            troughcolor=self.COLORES["entrada"],
            background=self.COLORES["rojo"],
            bordercolor=self.COLORES["entrada"],
            lightcolor=self.COLORES["rojo"],
            darkcolor=self.COLORES["rojo"],
            thickness=10,
        )
        style.configure(
            "Vertical.TScrollbar",
            background=self.COLORES["tarjeta"],
            troughcolor=self.COLORES["panel"],
            bordercolor=self.COLORES["panel"],
            arrowcolor=self.COLORES["secundario"],
        )
        self.option_add("*TCombobox*Listbox.background", self.COLORES["entrada"])
        self.option_add("*TCombobox*Listbox.foreground", self.COLORES["texto"])
        self.option_add("*TCombobox*Listbox.selectBackground", self.COLORES["borde"])

    def _construir_interfaz(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        encabezado = ttk.Frame(self)
        encabezado.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        encabezado.columnconfigure(0, weight=1)

        titulo = ttk.Frame(encabezado)
        titulo.grid(row=0, column=0, sticky="w")
        ttk.Label(titulo, text="ARENA  /  RPG", style="Eyebrow.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 4)
        )
        ttk.Label(titulo, text="Combate por turnos", style="Title.TLabel").grid(
            row=1, column=0, sticky="w"
        )
        ttk.Label(
            titulo,
            text="Elige tu estrategia. Sobrevive a la arena.",
            style="Subtitle.TLabel",
        ).grid(row=2, column=0, sticky="w", pady=(4, 0))

        self.label_turno = tk.Label(
            encabezado,
            text="TURNO 01",
            bg=self.COLORES["panel"],
            fg=self.COLORES["dorado"],
            font=("TkDefaultFont", 10, "bold"),
            padx=16,
            pady=10,
        )
        self.label_turno.grid(row=0, column=1, sticky="e", padx=(16, 0))

        contenido = ttk.Frame(self)
        contenido.grid(row=1, column=0, sticky="nsew")
        contenido.columnconfigure(1, weight=1)
        contenido.rowconfigure(0, weight=1)

        self._construir_configuracion(contenido)
        self._construir_combate(contenido)
        self._construir_historial()

    def _construir_configuracion(self, parent: ttk.Frame) -> None:
        panel = tk.Frame(
            parent,
            bg=self.COLORES["panel"],
            highlightbackground=self.COLORES["borde"],
            highlightthickness=1,
            padx=20,
            pady=20,
            width=280,
        )
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        panel.grid_propagate(False)
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="PREPARACIÓN", style="Panel.Eyebrow.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(panel, text="Tu combatiente", style="Panel.Section.TLabel").grid(
            row=1, column=0, sticky="w", pady=(5, 18)
        )

        ttk.Label(panel, text="NOMBRE", style="Panel.Field.TLabel").grid(
            row=2, column=0, sticky="w", pady=(0, 7)
        )
        self.entry_nombre = ttk.Entry(panel)
        self.entry_nombre.insert(0, "Héroe")
        self.entry_nombre.grid(row=3, column=0, sticky="ew", pady=(0, 16))

        ttk.Label(panel, text="CLASE", style="Panel.Field.TLabel").grid(
            row=4, column=0, sticky="w", pady=(0, 7)
        )
        self.combo_clase = ttk.Combobox(
            panel,
            values=["Guerrero", "Mago", "Pícaro"],
            state="readonly",
        )
        self.combo_clase.set("Guerrero")
        self.combo_clase.grid(row=5, column=0, sticky="ew")

        ttk.Separator(panel).grid(row=6, column=0, sticky="ew", pady=20)
        ttk.Label(panel, text="RIVAL", style="Panel.Eyebrow.TLabel").grid(
            row=7, column=0, sticky="w"
        )
        ttk.Label(panel, text="Maestro Sombrío", style="Panel.Section.TLabel").grid(
            row=8, column=0, sticky="w", pady=(5, 2)
        )
        ttk.Label(panel, text="Guerrero  ·  Nivel 1", style="Panel.Subtitle.TLabel").grid(
            row=9, column=0, sticky="w"
        )

        ttk.Button(
            panel,
            text="Iniciar nueva partida",
            style="Accent.TButton",
            command=self._iniciar_partida,
        ).grid(row=10, column=0, sticky="ew", pady=(24, 0))
        ttk.Label(
            panel,
            text="Al iniciar, la partida y el registro se reinician.",
            style="Panel.Subtitle.TLabel",
            wraplength=230,
            justify="left",
        ).grid(row=11, column=0, sticky="w", pady=(12, 0))

    def _construir_combate(self, parent: ttk.Frame) -> None:
        zona = ttk.Frame(parent)
        zona.grid(row=0, column=1, sticky="nsew")
        zona.columnconfigure((0, 1), weight=1, uniform="combatientes")

        ttk.Label(zona, text="ENFRENTAMIENTO", style="Eyebrow.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        ttk.Label(zona, text="Estado del combate", style="Section.TLabel").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(5, 4)
        )
        ttk.Label(
            zona,
            text="Controla tu salud y decide cuándo atacar, defenderte o recuperarte.",
            style="Subtitle.TLabel",
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 16))

        (
            self.avatar_jugador,
            self.nombre_jugador,
            self.clase_jugador,
            self.hp_jugador,
            self.vida_jugador,
        ) = self._crear_tarjeta_combatiente(
            zona, 3, 0, "JUGADOR", self.COLORES["verde"], "Player"
        )
        (
            self.avatar_enemigo,
            self.nombre_enemigo,
            self.clase_enemigo,
            self.hp_enemigo,
            self.vida_enemigo,
        ) = self._crear_tarjeta_combatiente(
            zona, 3, 1, "OPONENTE", self.COLORES["rojo"], "Enemy"
        )

        ttk.Label(zona, text="TUS ACCIONES", style="Eyebrow.TLabel").grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(22, 10)
        )
        acciones = ttk.Frame(zona)
        acciones.grid(row=5, column=0, columnspan=2, sticky="ew")
        for columna in range(4):
            acciones.columnconfigure(columna, weight=1, uniform="acciones")

        opciones = [
            ("Ataque básico", "ataque"),
            ("Habilidad especial", "habilidad"),
            ("Defender", "defender"),
            ("Curar", "curar"),
        ]
        for columna, (texto, accion) in enumerate(opciones):
            boton = ttk.Button(
                acciones,
                text=texto,
                style="Action.TButton",
                command=lambda opcion=accion: self._ejecutar(opcion),
            )
            boton.grid(row=0, column=columna, sticky="ew", padx=(0 if columna == 0 else 5, 0))
            self.botones_accion.append(boton)

    def _crear_tarjeta_combatiente(
        self,
        parent: ttk.Frame,
        fila: int,
        columna: int,
        etiqueta: str,
        color: str,
        estilo_vida: str,
    ) -> tuple[tk.Label, ttk.Label, ttk.Label, ttk.Label, ttk.Progressbar]:
        tarjeta = tk.Frame(
            parent,
            bg=self.COLORES["tarjeta"],
            highlightbackground=self.COLORES["borde"],
            highlightthickness=1,
            padx=16,
            pady=15,
        )
        tarjeta.grid(
            row=fila,
            column=columna,
            sticky="nsew",
            padx=(0 if columna == 0 else 7, 7 if columna == 0 else 0),
        )
        tarjeta.columnconfigure(1, weight=1)

        tk.Label(
            tarjeta,
            text=etiqueta,
            bg=self.COLORES["tarjeta"],
            fg=color,
            font=("TkDefaultFont", 9, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 13))

        retrato = tk.Label(
            tarjeta,
            text="?",
            bg=self.COLORES["panel"],
            fg=color,
            font=("TkDefaultFont", 20, "bold"),
            width=3,
            height=2,
        )
        retrato.grid(row=1, column=0, rowspan=2, sticky="nw", padx=(0, 12))

        nombre = ttk.Label(tarjeta, text="", style="Card.Section.TLabel")
        nombre.grid(row=1, column=1, sticky="sw")
        clase = ttk.Label(tarjeta, text="", style="Card.Subtitle.TLabel")
        clase.grid(row=2, column=1, sticky="nw", pady=(3, 0))

        hp = ttk.Label(tarjeta, text="", style="Card.Field.TLabel")
        hp.grid(row=3, column=0, columnspan=2, sticky="w", pady=(17, 7))
        vida = ttk.Progressbar(
            tarjeta,
            maximum=100,
            style=f"{estilo_vida}.Horizontal.TProgressbar",
        )
        vida.grid(row=4, column=0, columnspan=2, sticky="ew")
        return retrato, nombre, clase, hp, vida

    def _construir_historial(self) -> None:
        registro = tk.Frame(
            self,
            bg=self.COLORES["panel"],
            highlightbackground=self.COLORES["borde"],
            highlightthickness=1,
            padx=16,
            pady=12,
        )
        registro.grid(row=2, column=0, sticky="nsew", pady=(18, 0))
        registro.columnconfigure(0, weight=1)
        registro.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(registro, text="REGISTRO", style="Eyebrow.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )
        self.texto_historial = tk.Text(
            registro,
            height=7,
            state="disabled",
            wrap="word",
            background=self.COLORES["panel"],
            foreground=self.COLORES["texto"],
            insertbackground=self.COLORES["texto"],
            selectbackground=self.COLORES["borde"],
            relief="flat",
            borderwidth=0,
            font=("TkFixedFont", 10),
            padx=4,
            pady=2,
        )
        self.texto_historial.grid(row=1, column=0, sticky="nsew")
        self.texto_historial.tag_configure(
            "sistema", foreground=self.COLORES["dorado"], font=("TkFixedFont", 10, "bold")
        )
        scrollbar = ttk.Scrollbar(
            registro,
            orient="vertical",
            command=self.texto_historial.yview,
            style="Vertical.TScrollbar",
        )
        scrollbar.grid(row=1, column=1, sticky="ns", padx=(8, 0))
        self.texto_historial.configure(yscrollcommand=scrollbar.set)

    @staticmethod
    def _crear_personaje(nombre: str, clase: str) -> Personaje:
        if clase == "Guerrero":
            return Guerrero(nombre)
        if clase == "Mago":
            return Mago(nombre)
        if clase == "Pícaro":
            return Picaro(nombre)
        raise ValueError("Selecciona una clase válida.")

    def _iniciar_partida(self) -> None:
        nombre = self.entry_nombre.get().strip() if hasattr(self, "entry_nombre") else "Héroe"
        clase = self.combo_clase.get() if hasattr(self, "combo_clase") else "Guerrero"
        try:
            jugador = self._crear_personaje(nombre, clase)
            enemigo = Guerrero("Maestro Sombrío", ataque=15, defensa=5)
            self.motor = MotorCombate(jugador, enemigo)
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
            self.entry_nombre.focus_set()
            return
        self._limpiar_historial()
        self._actualizar_interfaz()
        self._escribir_historial("Nueva partida iniciada.")

    def _ejecutar(self, accion: str) -> None:
        if self.motor is None:
            return
        try:
            cantidad_antes = len(self.motor.historial)
            mensaje = self.motor.ejecutar_accion(accion)
            self._actualizar_interfaz()
            self._escribir_historial(mensaje)
            for entrada in self.motor.historial[cantidad_antes:]:
                if entrada != f"Turno {self.motor.turno - 1}: {mensaje}":
                    self._escribir_historial(entrada)
            if self.motor.finalizado:
                ganador = self.motor.ganador
                texto = f"¡Victoria de {ganador.nombre}!" if ganador else "Empate"
                messagebox.showinfo("Resultado del combate", texto)
        except (RuntimeError, ValueError) as error:
            messagebox.showerror("No se pudo ejecutar la acción", str(error))

    def _actualizar_interfaz(self) -> None:
        if self.motor is None:
            return
        jugador = self.motor.jugador
        enemigo = self.motor.enemigo
        self.avatar_jugador.configure(text=jugador.nombre[:1].upper())
        self.nombre_jugador.configure(text=jugador.nombre)
        self.clase_jugador.configure(text=self._nombre_clase(jugador))
        self.hp_jugador.configure(text=f"{jugador.hp} / {jugador.hp_maximo} HP")
        self.vida_jugador.configure(maximum=jugador.hp_maximo, value=jugador.hp)

        self.avatar_enemigo.configure(text=enemigo.nombre[:1].upper())
        self.nombre_enemigo.configure(text=enemigo.nombre)
        self.clase_enemigo.configure(text=self._nombre_clase(enemigo))
        self.hp_enemigo.configure(text=f"{enemigo.hp} / {enemigo.hp_maximo} HP")
        self.vida_enemigo.configure(maximum=enemigo.hp_maximo, value=enemigo.hp)

        self.label_turno.configure(
            text="COMBATE FINALIZADO" if self.motor.finalizado else f"TURNO {self.motor.turno:02d}"
        )
        estado = "disabled" if self.motor.finalizado else "normal"
        for boton in self.botones_accion:
            boton.configure(state=estado)

    @staticmethod
    def _nombre_clase(personaje: Personaje) -> str:
        return {
            Guerrero: "Guerrero",
            Mago: "Mago",
            Picaro: "Pícaro",
        }.get(type(personaje), type(personaje).__name__)

    def _limpiar_historial(self) -> None:
        self.texto_historial.configure(state="normal")
        self.texto_historial.delete("1.0", "end")
        self.texto_historial.configure(state="disabled")

    def _escribir_historial(self, mensaje: str) -> None:
        self.texto_historial.configure(state="normal")
        etiqueta = "sistema" if mensaje == "Nueva partida iniciada." else None
        self.texto_historial.insert("end", mensaje + "\n", etiqueta)
        self.texto_historial.see("end")
        self.texto_historial.configure(state="disabled")
