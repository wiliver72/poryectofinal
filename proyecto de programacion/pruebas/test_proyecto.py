import unittest

from modelos.base import Personaje
from modelos.personajes import Guerrero, Mago, Picaro
from servicios.motor_combate import MotorCombate
from interfaz.ventana_principal import VentanaPrincipal


class PruebasProyecto(unittest.TestCase):
    def test_clases_definen_estadisticas_por_defecto(self):
        guerrero = Guerrero("Ari")
        mago = Mago("Merlin")
        picaro = Picaro("Luna")

        self.assertEqual((guerrero.hp_maximo, guerrero.atacando, guerrero.defensa), (100, 18, 7))
        self.assertEqual((mago.hp_maximo, mago.atacando, mago.defensa), (82, 16, 4))
        self.assertEqual((picaro.hp_maximo, picaro.atacando, picaro.defensa), (88, 17, 5))

    def test_encapsulamiento_limita_hp(self):
        guerrero = Guerrero("Ari", 100, 18, 7)
        guerrero.hp = 500
        self.assertEqual(guerrero.hp, 100)
        guerrero.recibir_danio(999)
        self.assertEqual(guerrero.hp, 0)

    def test_nombre_vacio_lanza_error(self):
        with self.assertRaises(ValueError):
            Guerrero("   ", 100, 18, 7)

    def test_clase_desconocida_lanza_error(self):
        with self.assertRaises(ValueError):
            VentanaPrincipal._crear_personaje("Ari", "Explorador")

    def test_polimorfismo_habilidades_distintas(self):
        objetivo = Guerrero("Objetivo", 100, 10, 2)
        personajes: list[Personaje] = [
            Guerrero("Guerra", 100, 18, 7),
            Mago("Merlin", 82, 16, 4),
            Picaro("Luna", 88, 17, 5),
        ]
        mensajes = [personaje.habilidad_especial(objetivo) for personaje in personajes]
        self.assertTrue(all(isinstance(mensaje, str) for mensaje in mensajes))
        self.assertIn("Golpe brutal", mensajes[0])
        self.assertIn("bola de fuego", mensajes[1])
        self.assertIn("golpe furtivo", mensajes[2])

    def test_accion_invalida_y_reinicio(self):
        jugador = Guerrero("Ari", 100, 18, 7)
        enemigo = Guerrero("Jefe", 100, 15, 5)
        motor = MotorCombate(jugador, enemigo)
        with self.assertRaises(ValueError):
            motor.ejecutar_accion("volar")
        nuevo = Mago("Nueva", 82, 16, 4)
        motor.reiniciar(nuevo, enemigo)
        self.assertEqual(motor.turno, 1)
        self.assertEqual(len(motor.historial), 0)

    def test_combate_finaliza_con_ganador(self):
        jugador = Guerrero("Ari", 100, 50, 20)
        enemigo = Mago("Malo", 10, 5, 0)
        motor = MotorCombate(jugador, enemigo)
        motor.ejecutar_accion("habilidad")
        self.assertTrue(motor.finalizado)
        self.assertIs(motor.ganador, jugador)


if __name__ == "__main__":
    unittest.main()
