from typing import List
from modelos.base import Personaje


class MotorCombate:
    """Controla turnos, acciones e historial de una partida."""

    ACCIONES_VALIDAS = {"ataque", "habilidad", "defender", "curar"}

    def __init__(self, jugador: Personaje, enemigo: Personaje):
        self._jugador = jugador
        self._enemigo = enemigo
        self._turno = 1
        self._historial: List[str] = []
        self._finalizado = False

    @property
    def jugador(self) -> Personaje:
        return self._jugador

    @property
    def enemigo(self) -> Personaje:
        return self._enemigo

    @property
    def turno(self) -> int:
        return self._turno

    @property
    def finalizado(self) -> bool:
        return self._finalizado

    @property
    def historial(self) -> tuple[str, ...]:
        return tuple(self._historial)

    @property
    def ganador(self) -> Personaje | None:
        if self.jugador.esta_vivo and not self.enemigo.esta_vivo:
            return self.jugador
        if self.enemigo.esta_vivo and not self.jugador.esta_vivo:
            return self.enemigo
        return None

    def ejecutar_accion(self, accion: str) -> str:
        if self._finalizado:
            raise RuntimeError("La partida ya terminó.")
        if accion not in self.ACCIONES_VALIDAS:
            raise ValueError("Acción de combate desconocida.")

        if accion == "ataque":
            mensaje = self.jugador.atacar_basico(self.enemigo)
        elif accion == "habilidad":
            mensaje = self.jugador.habilidad_especial(self.enemigo)
        elif accion == "defender":
            mensaje = self.jugador.defender()
        else:
            curado = self.jugador.curar(12)
            mensaje = f"{self.jugador.nombre} se cura {curado} HP."

        self._registrar(f"Turno {self._turno}: {mensaje}")
        self._comprobar_final()
        if not self._finalizado:
            self._accion_enemigo()
            self._comprobar_final()
        self._turno += 1
        return mensaje

    def reiniciar(self, jugador: Personaje, enemigo: Personaje) -> None:
        self._jugador = jugador
        self._enemigo = enemigo
        self._turno = 1
        self._historial.clear()
        self._finalizado = False

    def _accion_enemigo(self) -> None:
        if self.enemigo.hp <= self.enemigo.hp_maximo // 3:
            curado = self.enemigo.curar(10)
            mensaje = f"{self.enemigo.nombre} se cura {curado} HP."
        elif self.enemigo.hp < self.enemigo.hp_maximo // 2:
            mensaje = self.enemigo.habilidad_especial(self.jugador)
        else:
            mensaje = self.enemigo.atacar_basico(self.jugador)
        self._registrar(f"Turno {self._turno}: {mensaje}")

    def _comprobar_final(self) -> None:
        if not self.jugador.esta_vivo or not self.enemigo.esta_vivo:
            self._finalizado = True

    def _registrar(self, mensaje: str) -> None:
        self._historial.append(mensaje)
