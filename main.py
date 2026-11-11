"""Punto de entrada del Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ.

Ejecuta y demuestra al menos 10 operaciones solicitadas en la Fase 4.
"""

from __future__ import annotations

from software_fj.excepciones import (
    ClienteNoEncontradoError,
    DatoInvalidoError,
    ParametroFaltanteError,
    ReservaNoPermitidaError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)
from software_fj.gestor import GestorSoftwareFJ


def imprimir_titulo(texto: str) -> None:
    print("\n" + "=" * 80)
    print(texto)
    print("=" * 80)


def ejecutar_operacion(nombre: str, funcion) -> None:
    """Ejecuta una operación mostrando manejo de excepciones y continuidad del programa."""
    imprimir_titulo(nombre)
    try:
        resultado = funcion()
    except SoftwareFJError as error:
        print(f"[ERROR CONTROLADO] {type(error).__name__}: {error}")
        # Se registra el error controlado en el log del gestor a través de operaciones previas/finally;
        # aquí se evidencia que el programa continúa.
    except Exception as error:
        # Ejemplo de encapsulamiento/encadenamiento defensivo ante errores inesperados
        print(f"[ERROR INESPERADO] {type(error).__name__}: {error}")
        raise RuntimeError("Fallo inesperado en la simulación.") from error
    else:
        print(f"[ÉXITO] {resultado}")
    finally:
        print("[FIN DE OPERACIÓN] La ejecución continúa con la siguiente operación.")


def main() -> None:
    gestor = GestorSoftwareFJ()

    operaciones = []

    # 1. Registrar un cliente válido.
    operaciones.append(
        (
            "1. Registrar un cliente válido",
            lambda: gestor.registrar_cliente(
                "C001", "Sarlyn Murillo", "sarlyn.murillo@example.com", "3001234567"
            ).descripcion(),
        )
    )

    # 2. Intentar registrar un cliente con correo inválido.
    operaciones.append(
        (
            "2. Intentar registrar un cliente con correo inválido",
            lambda: gestor.registrar_cliente(
                "C002", "Cliente Invalido", "correo-invalido", "3009876543"
            ).descripcion(),
        )
    )

    # 3. Registrar otro cliente válido.
    operaciones.append(
        (
            "3. Registrar otro cliente válido",
            lambda: gestor.registrar_cliente(
                "C003", "Carlos Perez", "carlos.perez@example.com", "3015557788"
            ).descripcion(),
        )
    )

    # 4. Crear un servicio de reserva de salas.
    operaciones.append(
        (
            "4. Crear un servicio de reserva de salas",
            lambda: gestor.crear_servicio_reserva_sala(
                "S001", "Sala de Innovación", 50000.0, capacidad=12
            ).descripcion(),
        )
    )

    # 5. Crear un servicio de alquiler de equipos.
    operaciones.append(
        (
            "5. Crear un servicio de alquiler de equipos",
            lambda: gestor.crear_servicio_alquiler_equipo(
                "S002", "Alquiler de Portátil", 20000.0, tipo_equipo="Portátil"
            ).descripcion(),
        )
    )

    # 6. Crear un servicio de asesorías.
    operaciones.append(
        (
            "6. Crear un servicio de asesorías",
            lambda: gestor.crear_servicio_asesoria(
                "S003", "Asesoría en Programación", 80000.0, nivel="avanzado"
            ).descripcion(),
        )
    )

    # 7. Intentar crear un servicio con tarifa incorrecta.
    operaciones.append(
        (
            "7. Intentar crear un servicio con tarifa incorrecta",
            lambda: gestor.crear_servicio_reserva_sala(
                "S004", "Sala Errónea", -10000.0, capacidad=8
            ).descripcion(),
        )
    )

    # 8. Crear, confirmar y procesar una reserva correctamente.
    def operacion_reserva_exitosa() -> str:
        reserva = gestor.crear_reserva("R001", "C001", "S003", horas=2, unidades=1)
        gestor.confirmar_reserva("R001")
        costo = gestor.procesar_reserva("R001", descuento=0.10, aplicar_impuesto=True)
        return f"{reserva.descripcion()} | Costo procesado: {costo:.2f}"

    operaciones.append(("8. Crear, confirmar y procesar una reserva correctamente", operacion_reserva_exitosa))

    # 9. Intentar crear una reserva con un servicio inexistente.
    operaciones.append(
        (
            "9. Intentar crear una reserva con un servicio inexistente",
            lambda: gestor.crear_reserva("R002", "C003", "S999", horas=1).descripcion(),
        )
    )

    # 10. Intentar procesar una reserva sin confirmarla previamente.
    def operacion_reserva_sin_confirmar() -> str:
        gestor.crear_reserva("R003", "C003", "S001", horas=3, unidades=1)
        costo = gestor.procesar_reserva("R003")
        return f"Costo: {costo:.2f}"

    operaciones.append(
        ("10. Intentar procesar una reserva sin confirmarla previamente", operacion_reserva_sin_confirmar)
    )

    for nombre, funcion in operaciones:
        ejecutar_operacion(nombre, funcion)

    imprimir_titulo("RESUMEN FINAL")
    print(f"Clientes registrados: {len(gestor.listar_clientes())}")
    print(f"Servicios registrados: {len(gestor.listar_servicios())}")
    print(f"Reservas registradas: {len(gestor.listar_reservas())}")
    print("Estados de reservas:")
    for reserva in gestor.listar_reservas():
        print(f" - {reserva.descripcion()}")
    print("\nSimulación finalizada. Revise el archivo logs/software_fj.log para el registro de eventos.")


if __name__ == "__main__":
    main()
