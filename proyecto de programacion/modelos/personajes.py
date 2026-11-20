from .base import Personaje


class Guerrero(Personaje):
    def __init__(
        self, nombre: str, hp_maximo: int = 100, ataque: int = 18, defensa: int = 7
    ) -> None:
        super().__init__(nombre, hp_maximo, ataque, defensa)

    def atacar_basico(self, objetivo: Personaje) -> str:
        danio = objetivo.recibir_danio(self.atacando)
        return f"{self.nombre} corta con su espada a {objetivo.nombre} ({danio} HP)."

    def habilidad_especial(self, objetivo: Personaje) -> str:
        danio = objetivo.recibir_danio(self.atacando + 8)
        return f"{self.nombre} usa Golpe brutal contra {objetivo.nombre} ({danio} HP)."


class Mago(Personaje):
    def __init__(
        self, nombre: str, hp_maximo: int = 82, ataque: int = 16, defensa: int = 4
    ) -> None:
        super().__init__(nombre, hp_maximo, ataque, defensa)

    def atacar_basico(self, objetivo: Personaje) -> str:
        danio = objetivo.recibir_danio(self.atacando - 2)
        return f"{self.nombre} lanza una descarga arcana a {objetivo.nombre} ({danio} HP)."

    def habilidad_especial(self, objetivo: Personaje) -> str:
        danio = objetivo.recibir_danio(self.atacando + 12)
        curacion = self.curar(4)
        return f"{self.nombre} invoca bola de fuego: {danio} daño y se cura {curacion} HP."


class Picaro(Personaje):
    def __init__(
        self, nombre: str, hp_maximo: int = 88, ataque: int = 17, defensa: int = 5
    ) -> None:
        super().__init__(nombre, hp_maximo, ataque, defensa)

    def atacar_basico(self, objetivo: Personaje) -> str:
        danio = objetivo.recibir_danio(self.atacando)
        return f"{self.nombre} apuñala a {objetivo.nombre} ({danio} HP)."

    def habilidad_especial(self, objetivo: Personaje) -> str:
        danio = objetivo.recibir_danio(self.atacando + 5)
        curacion = self.curar(7)
        return f"{self.nombre} usa golpe furtivo: {danio} daño y se cura {curacion} HP."
