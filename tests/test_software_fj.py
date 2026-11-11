"""Pruebas automatizadas para el sistema Software FJ."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from software_fj.excepciones import (
    ClienteNoEncontradoError,
    DatoInvalidoError,
    ReservaNoPermitidaError,
    ServicioNoDisponibleError,
)
from software_fj.gestor import GestorSoftwareFJ
from software_fj.servicios import AsesoriaEspecializada, ReservaSala


class TestSoftwareFJ(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.log_path = Path(self.tmp.name) / "test.log"
        self.gestor = GestorSoftwareFJ(ruta_log=self.log_path)

    def tearDown(self) -> None:
        # Cierra handlers para liberar el archivo de log en Windows.
        for handler in list(self.gestor.logger.handlers):
            handler.close()
            self.gestor.logger.removeHandler(handler)
        self.tmp.cleanup()

    def test_registro_cliente_valido(self):
        cliente = self.gestor.registrar_cliente("C1", "Ana Maria", "ana@example.com", "3001234567")
        self.assertEqual(cliente.nombre, "Ana Maria")
        self.assertEqual(len(self.gestor.listar_clientes()), 1)

    def test_cliente_correo_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            self.gestor.registrar_cliente("C2", "Ana", "correo-malo", "3001234567")

    def test_cliente_duplicado_por_correo(self):
        self.gestor.registrar_cliente("C1", "Ana Maria", "ana@example.com", "3001234567")
        with self.assertRaises(DatoInvalidoError):
            self.gestor.registrar_cliente("C2", "Ana Perez", "ana@example.com", "3009999999")

    def test_crear_servicio_tarifa_incorrecta(self):
        with self.assertRaises(DatoInvalidoError):
            self.gestor.crear_servicio_reserva_sala("S1", "Sala A", -5, capacidad=10)

    def test_calculo_costo_polimorfismo_y_descuento_impuesto(self):
        sala = ReservaSala("S10", "Sala Test", 100.0, capacidad=10)
        # costo base 100*2*1=200, descuento 10% -> 180, impuesto 19% -> 214.2
        total = sala.calcular_costo(horas=2, unidades=1, descuento=0.10, aplicar_impuesto=True)
        self.assertAlmostEqual(total, 214.2, places=2)

        asesoria = AsesoriaEspecializada("S11", "Asesoria", 100.0, nivel="avanzado")
        # base 100*1*1*1.35=135, sin descuento, sin impuesto
        total_asesoria = asesoria.calcular_costo(horas=1, unidades=1, descuento=0.0, aplicar_impuesto=False)
        self.assertAlmostEqual(total_asesoria, 135.0, places=2)

    def test_reserva_exitosa_confirmar_y_procesar(self):
        self.gestor.registrar_cliente("C1", "Ana Maria", "ana@example.com", "3001234567")
        self.gestor.crear_servicio_asesoria("S1", "Asesoría", 100.0, nivel="general")
        reserva = self.gestor.crear_reserva("R1", "C1", "S1", horas=1)
        self.assertEqual(reserva.estado, "CREADA")
        self.gestor.confirmar_reserva("R1")
        self.assertEqual(self.gestor.consultar_reserva("R1").estado, "CONFIRMADA")
        costo = self.gestor.procesar_reserva("R1", descuento=0.0, aplicar_impuesto=False)
        self.assertAlmostEqual(costo, 115.0, places=2)  # general factor 1.15
        self.assertEqual(self.gestor.consultar_reserva("R1").estado, "PROCESADA")

    def test_reserva_servicio_inexistente(self):
        self.gestor.registrar_cliente("C1", "Ana Maria", "ana@example.com", "3001234567")
        with self.assertRaises(ServicioNoDisponibleError):
            self.gestor.crear_reserva("R1", "C1", "S999", horas=1)

    def test_procesar_reserva_sin_confirmar(self):
        self.gestor.registrar_cliente("C1", "Ana Maria", "ana@example.com", "3001234567")
        self.gestor.crear_servicio_reserva_sala("S1", "Sala", 100.0, capacidad=5)
        self.gestor.crear_reserva("R1", "C1", "S1", horas=1)
        with self.assertRaises(ReservaNoPermitidaError):
            self.gestor.procesar_reserva("R1")

    def test_cliente_no_encontrado(self):
        with self.assertRaises(ClienteNoEncontradoError):
            self.gestor.consultar_cliente("NOEXISTE")

    def test_log_se_genera(self):
        self.gestor.registrar_cliente("C1", "Ana Maria", "ana@example.com", "3001234567")
        self.assertTrue(self.log_path.exists())
        contenido = self.log_path.read_text(encoding="utf-8")
        self.assertIn("Cliente registrado", contenido)


if __name__ == "__main__":
    unittest.main()
