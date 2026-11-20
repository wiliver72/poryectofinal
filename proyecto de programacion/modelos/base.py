from abc import ABC, abstractmethod


class Personaje(ABC):
    """Entidad abstracta compartida por todos los combatientes."""

    def __init__(self, nombre: str, hp_maximo: int, ataque: int, defensa: int):
        self.nombre = nombre
        self.hp_maximo = hp_maximo
        self._hp = hp_maximo
        self._ataque = ataque
        self._defensa = defensa
        self._defendiendose = False

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError("El nombre no puede estar vacío.")
        if len(valor) > 18:
            raise ValueError("El nombre debe tener como máximo 18 caracteres.")
        self._nombre = valor

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise ValueError("La vida debe ser un número entero.")
        self._hp = max(0, min(valor, self._hp_maximo))

    @property
    def hp_maximo(self) -> int:
        return self._hp_maximo

    @hp_maximo.setter
    def hp_maximo(self, valor: int) -> None:
        if not isinstance(valor, int) or valor < 1:
            raise ValueError("La vida máxima debe ser un entero positivo.")
        self._hp_maximo = valor

    @property
    def esta_vivo(self) -> bool:
        return self._hp > 0

    @property
    def defensa(self) -> int:
        return self._defensa

    @property
    def atacando(self) -> int:
        return self._ataque

    def recibir_danio(self, cantidad: int) -> int:
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo.")
        reduccion = self._defensa // 2 if not self._defendiendose else self._defensa
        danio_real = max(1, cantidad - reduccion)
        hp_anterior = self._hp
        self.hp -= danio_real
        self._defendiendose = False
        return hp_anterior - self._hp

    def defender(self) -> str:
        self._defendiendose = True
        return f"{self.nombre} adopta una postura defensiva."

    def curar(self, cantidad: int) -> int:
        if cantidad < 0:
            raise ValueError("La curación no puede ser negativa.")
        hp_anterior = self._hp
        self.hp += cantidad
        return self._hp - hp_anterior

    @abstractmethod
    def atacar_basico(self, objetivo: "Personaje") -> str:
        """Ejecuta el ataque básico."""

    @abstractmethod
    def habilidad_especial(self, objetivo: "Personaje") -> str:
        """Ejecuta una habilidad propia de la clase."""
