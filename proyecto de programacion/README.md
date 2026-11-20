# Arena RPG por Turnos

## 1. Nombre del proyecto

**Arena RPG por Turnos** es un juego de escritorio en Python. El jugador elige un combatiente y se enfrenta por turnos al Maestro Sombrío.

## 2. Descripción del problema

El proyecto ofrece una aplicación pequeña e interactiva para practicar programación orientada a objetos. Las reglas de combate hacen visibles conceptos como encapsulamiento, herencia, abstracción y polimorfismo, mientras que la interfaz permite observar sus efectos.

## 3. Objetivos

- Aplicar POO en una aplicación funcional.
- Separar los modelos del dominio, las reglas de combate y la interfaz.
- Permitir iniciar y jugar un combate con acciones distintas.
- Validar entradas y comunicar errores sin cerrar la aplicación.
- Verificar las reglas principales con pruebas automatizadas.

## 4. Funcionalidades

- Elegir nombre y clase: Guerrero, Mago o Pícaro.
- Rechazar nombres vacíos o demasiado largos y clases desconocidas.
- Atacar con un movimiento básico o una habilidad propia de la clase.
- Defenderse para reducir el siguiente daño recibido.
- Recuperar vida con la acción de curación.
- Permitir que el enemigo responda automáticamente en cada turno.
- Consultar las barras de vida, el turno actual y el registro del combate.
- Iniciar una partida nueva, que reinicia el estado y el registro.
- Mostrar el resultado y desactivar acciones al finalizar el combate.

## 5. Tecnologías utilizadas

- **Python 3.10 o superior:** lenguaje de implementación. Se requiere por el uso de anotaciones de tipos modernas.
- **Tkinter y ttk:** interfaz gráfica de escritorio incluida con Python. Se eligió para evitar dependencias externas y facilitar la instalación.
- **unittest:** pruebas automatizadas de la biblioteca estándar de Python.
- **Markdown:** documentación del proyecto.

No se utilizan bibliotecas externas. `requirements.txt` se conserva para facilitar la instalación y futuras ampliaciones.

## 6. Instalación

Se necesita Python 3.10 o superior. Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows PowerShell, activa el entorno con:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En algunas distribuciones de Linux, Tkinter se instala por separado mediante el paquete del sistema `python3-tk`.

## 7. Ejecución

Desde la carpeta raíz, con el entorno virtual activado:

```bash
python main.py
```

Para ejecutar las pruebas:

```bash
python -m unittest discover -s pruebas -v
```

## 8. Manual de usuario

1. Al abrir la aplicación aparece una partida nueva.
2. Escribe el nombre del combatiente y selecciona una clase. Si el nombre está vacío, supera el límite permitido o la clase no es válida, la aplicación muestra una advertencia.
3. Pulsa **Iniciar nueva partida** para aplicar la selección y reiniciar el registro.
4. Elige **Ataque básico**, **Habilidad especial**, **Defender** o **Curar**. Después de cada acción válida, el enemigo realiza su turno si el combate no ha terminado.
5. Consulta el estado de ambos combatientes y los mensajes en el registro.
6. Al terminar el combate, la aplicación muestra el resultado y desactiva las acciones. Pulsa **Iniciar nueva partida** para volver a jugar.

### Capturas de pantalla

Guarda las capturas reales de la aplicación en `docs/imagenes/` con estos nombres antes de entregar:

- `[CAPTURA: inicio.png]` — ventana al iniciar.
- `[CAPTURA: seleccion.png]` — nombre y clase elegidos.
- `[CAPTURA: combate.png]` — combate en curso y registro de acciones.
- `[CAPTURA: resultado.png]` — estado final de la partida.

## 9. Estructura del proyecto

```text
proyecto-de-programacion/
├── main.py
├── modelos/
│   ├── __init__.py
│   ├── base.py
│   └── personajes.py
├── servicios/
│   ├── __init__.py
│   └── motor_combate.py
├── interfaz/
│   ├── __init__.py
│   └── ventana_principal.py
├── recursos/
├── pruebas/
│   └── test_proyecto.py
├── docs/
│   ├── INFORME_TECNICO.md
│   └── imagenes/
├── .gitignore
├── requirements.txt
└── README.md
```

- `main.py` inicia la aplicación.
- `modelos/` contiene la clase abstracta y los personajes concretos.
- `servicios/motor_combate.py` aplica las reglas, coordina los turnos y mantiene el historial.
- `interfaz/ventana_principal.py` construye la ventana y conecta los controles con el motor.
- `pruebas/test_proyecto.py` verifica reglas del dominio y del combate.
- `docs/` contiene el informe técnico y las capturas.

## 10. Autor o autores

- **Autor:** [Nombre del estudiante]
- **Institución:** [Nombre de la institución]
- **Curso:** [Nombre del curso]
- **Docente:** [Nombre del docente]
