# Informe técnico — Arena RPG por Turnos

## 1. Análisis del problema

El proyecto está dirigido a estudiantes que necesitan integrar conceptos de programación orientada a objetos en una aplicación ejecutable. El combate por turnos hace observables los cambios de estado de los personajes y permite comparar comportamientos distintos mediante una interfaz gráfica.

La aplicación permite elegir el nombre y la clase del jugador, ejecutar cuatro acciones, responder a un enemigo controlado por reglas, consultar el historial y comenzar otra partida. El alcance se limita a un combate local: no incluye conexión en red, guardado permanente, selección de equipo ni contenido descargable.

## 2. Diseño inicial

El diseño separa las responsabilidades por capas:

- `Personaje` define el estado y el contrato común de un combatiente.
- `Guerrero`, `Mago` y `Picaro` proporcionan estadísticas iniciales y comportamientos especializados.
- `MotorCombate` aplica las reglas, administra los turnos, decide la respuesta del enemigo y conserva el historial.
- `VentanaPrincipal` presenta la aplicación y conecta las acciones del usuario con el motor mediante callbacks.

La GUI no calcula el daño ni decide el resultado: delega esas reglas al dominio y al servicio de combate.

## 3. Arquitectura

`main.py` crea `VentanaPrincipal` e inicia el bucle de eventos de Tkinter. La interfaz importa las clases concretas y `MotorCombate`; este servicio recibe las instancias de los combatientes y coordina sus métodos. Los modelos no dependen de widgets ni de Tkinter.

La organización permite probar los modelos y el motor con `unittest` sin iniciar la interfaz. El estado de la partida y el registro se mantienen en memoria.

## 4. Funcionalidades y reglas del juego

La aplicación inicia una partida con el combatiente elegido y el Maestro Sombrío. En cada turno, el jugador puede atacar, usar la habilidad de su clase, defenderse o curarse. Si el combate continúa, el motor selecciona una respuesta del enemigo según su vida. La partida termina cuando uno de los combatientes llega a cero HP; el motor expone el ganador y la interfaz comunica el resultado.

Al comenzar una partida nueva se crean combatientes nuevos, se reinician los turnos y se limpia el registro visual. El nombre y la clase se validan al crear el personaje; las acciones no válidas o posteriores al final del combate producen errores que la interfaz muestra al usuario.

## 5. Aplicación de POO

La clase abstracta establece el contrato para los comportamientos que cada personaje debe implementar:

```python
class Personaje(ABC):
    @abstractmethod
    def atacar_basico(self, objetivo: "Personaje") -> str:
        ...

    @abstractmethod
    def habilidad_especial(self, objetivo: "Personaje") -> str:
        ...
```

Las clases concretas inicializan su configuración heredada mediante `super()` y redefinen los ataques:

```python
class Guerrero(Personaje):
    def __init__(self, nombre: str, hp_maximo: int = 100,
                 ataque: int = 18, defensa: int = 7) -> None:
        super().__init__(nombre, hp_maximo, ataque, defensa)

    def habilidad_especial(self, objetivo: Personaje) -> str:
        ...
```

| Concepto | Clase o método | Archivo | Explicación |
| :--- | :--- | :--- | :--- |
| Clases y objetos | `Personaje`, `Guerrero`, `Mago`, `Picaro` | `modelos/base.py`, `modelos/personajes.py` | Cada combatiente se instancia como objeto con estado y operaciones propios. |
| Encapsulamiento | `nombre`, `hp`, `hp_maximo`, `recibir_danio` | `modelos/base.py` | Las propiedades validan nombres y límites de vida; los métodos concentran el daño, la defensa y la curación. |
| Herencia | `Guerrero`, `Mago`, `Picaro` | `modelos/personajes.py` | Las clases reutilizan `Personaje`, invocan su constructor con `super()` y especializan estadísticas y ataques. |
| Polimorfismo | `atacar_basico`, `habilidad_especial` | `modelos/personajes.py`, `servicios/motor_combate.py` | El motor invoca las operaciones del tipo base; la implementación concreta determina el efecto y el mensaje. |
| Abstracción | `Personaje(ABC)` | `modelos/base.py` | `ABC` y `@abstractmethod` impiden crear un combatiente incompleto y fijan las operaciones requeridas. |
| Relaciones | `MotorCombate`, `Personaje` y objetivo del ataque | `servicios/motor_combate.py`, `modelos/personajes.py` | El motor se asocia con los combatientes que recibe; el historial es una lista creada y administrada por el motor. Un ataque recibe otro `Personaje` como objetivo. |

La relación del motor con los combatientes es una agregación: las instancias se crean fuera del motor y se entregan a su constructor. El motor mantiene la propiedad de su lista interna de historial, que constituye una composición. Los personajes colaboran al dirigir un ataque a otro personaje.

## 6. Construcción de la interfaz

Se utiliza **Tkinter/ttk**, incluida en Python, para evitar dependencias externas y ofrecer una interfaz de escritorio. Los estilos de ttk y los colores de Tkinter organizan la ventana en una sección de configuración, tarjetas de combatientes, controles de acción y registro desplazable.

Los controles permiten introducir el nombre, seleccionar una clase, iniciar una partida y elegir ataque básico, habilidad especial, defensa o curación. Los botones llaman a métodos de `VentanaPrincipal`; estos invocan `MotorCombate`, actualizan las barras de vida y agregan los mensajes al registro. Las entradas inválidas y las acciones no permitidas se comunican mediante cuadros de diálogo. Al finalizar el combate, las acciones quedan deshabilitadas.

Para completar la evidencia visual de la entrega, guarda estas capturas reales en `docs/imagenes/`:

- `[CAPTURA: inicio.png]` — ventana al iniciar.
- `[CAPTURA: seleccion.png]` — nombre y clase elegidos.
- `[CAPTURA: combate.png]` — combate en curso y registro de acciones.
- `[CAPTURA: resultado.png]` — estado final de la partida.

## 7. Proceso de desarrollo

1. **Formulación de la idea:** se escogió un combate RPG local por turnos.
2. **Identificación de funcionalidades:** se definieron selección de personaje, acciones, respuesta del enemigo, historial y reinicio.
3. **Diseño de clases:** se separaron el contrato `Personaje`, las especializaciones y el motor.
4. **Construcción de la lógica:** se implementaron validaciones, daño, defensa, curación, turnos y condición de finalización.
5. **Desarrollo de la interfaz:** se construyó la ventana con Tkinter/ttk, tarjetas de estado y controles.
6. **Integración:** los callbacks conectan los controles con el motor, manteniendo las reglas fuera de los widgets.
7. **Pruebas y correcciones:** se verificaron los límites de vida, las clases, el polimorfismo, las acciones inválidas y el flujo de partida.

## 8. Pruebas

Las pruebas se ejecutan con `python -m unittest discover -s pruebas -v`.

| Prueba | Acción realizada | Resultado esperado | Resultado obtenido |
| :--- | :--- | :--- | :--- |
| Estadísticas por clase | Crear las tres clases con sus valores iniciales predeterminados. | Cada clase queda inicializada con sus estadísticas correspondientes. | Correcto. |
| Encapsulamiento de vida | Asignar vida sobre el máximo y aplicar daño excesivo. | La vida no supera el máximo y no baja de cero. | Correcto. |
| Validación de nombre | Crear un personaje con nombre vacío. | Se genera `ValueError`. | Correcto. |
| Validación de clase | Intentar crear un personaje con una clase desconocida. | Se genera `ValueError`. | Correcto. |
| Polimorfismo | Ejecutar las habilidades de Guerrero, Mago y Pícaro. | Cada clase responde con su comportamiento especializado. | Correcto. |
| Acción inválida y reinicio | Enviar una acción desconocida y reiniciar el motor. | La acción inválida se rechaza; el reinicio restaura turno e historial. | Correcto. |
| Finalización del combate | Derrotar al enemigo con una habilidad. | La partida finaliza y se identifica al ganador. | Correcto. |

## 9. Problemas y soluciones

Durante la revisión para esta entrega se identificaron y resolvieron estos problemas:

- **Las estadísticas iniciales estaban asignadas desde la interfaz.** Esto acoplaba la presentación con datos propios de cada clase. Se trasladaron como valores predeterminados a los constructores de los personajes, que inicializan la clase base mediante `super()`.
- **El registro visual conservaba mensajes de la partida anterior.** La interfaz creaba un motor nuevo, pero no limpiaba el widget de texto. Ahora borra el registro antes de mostrar la nueva partida.
- **El comando de instalación del README apuntaba a una carpeta que no existe en todas las instalaciones.** Se reemplazó por instrucciones para activar el entorno desde la carpeta raíz del proyecto.

## 10. Conclusiones

El proyecto integra clases abstractas y concretas, validación de estado, herencia, polimorfismo y colaboración entre objetos en un juego pequeño y ejecutable. La separación entre modelos, servicio e interfaz permite probar la lógica sin abrir la ventana y mantener la GUI enfocada en la interacción.

La aplicación no guarda partidas al cerrar y dispone de un único rival con reglas sencillas. Como posibles extensiones se podrían añadir más enemigos, niveles de dificultad o persistencia opcional, manteniendo el alcance controlado.
