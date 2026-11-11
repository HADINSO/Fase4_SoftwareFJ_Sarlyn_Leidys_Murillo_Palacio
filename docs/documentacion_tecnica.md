# Documentación técnica – Sistema Integral de Gestión de Clientes, Servicios y Reservas (Software FJ)

## 1. Información general
- **Proyecto:** Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ
- **Estudiante:** SARLYN LEIDYS MURILLO PALACIOS
- **Curso:** Programación (213023) – UNAD
- **Fase:** 4 – Componente práctico: Prácticas simuladas
- **Lenguaje:** Python (sin bases de datos; persistencia operativa en memoria)

## 2. Arquitectura y separación de responsabilidades
El sistema se organiza en módulos con responsabilidades claras:

- `software_fj/entidades.py`: define la clase abstracta `Entidad`, base común para entidades del sistema.
- `software_fj/clientes.py`: implementa `Cliente` con encapsulación, validaciones estrictas y actualización de contacto.
- `software_fj/servicios.py`: define la clase abstracta `Servicio` y las clases derivadas `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`.
- `software_fj/reservas.py`: implementa `Reserva`, estados, validaciones y operaciones (confirmar, cancelar, procesar, calcular costo).
- `software_fj/excepciones.py`: define excepciones personalizadas del dominio.
- `software_fj/logger_config.py`: configura el logger (archivo + consola) usando `logging`.
- `software_fj/gestor.py`: orquesta la lógica de negocio en memoria (clientes, servicios, reservas), aplica reglas y registra eventos/errores.
- `main.py`: punto de entrada que ejecuta la simulación de las 10 operaciones obligatorias.
- `tests/test_software_fj.py`: pruebas automatizadas con `unittest`.

## 3. Diseño orientado a objetos
### 3.1 Abstracción
- `Entidad` (ABC) define la interfaz común (`descripcion`, `validar`) para entidades del sistema.
- `Servicio` (ABC) define el contrato para servicios, incluyendo `costo_base` abstracto y el cálculo total con políticas de impuesto/descuento.

### 3.2 Encapsulación
- `Cliente` encapsula datos personales (`_nombre`, `_correo`, `_telefono`) y expone acceso/control mediante propiedades y validaciones.
- `Reserva` y `Servicio` encapsulan su estado interno y reglas de negocio.

### 3.3 Herencia
- `Cliente` hereda de `Entidad`.
- `Servicio` hereda de `Entidad` y es base de `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`.

### 3.4 Polimorfismo y métodos sobrescritos
- `descripcion()` y `validar()` se implementan/sobrescriben según el tipo concreto.
- `costo_base()` se implementa de forma polimórfica en cada servicio:
  - **ReservaSala:** considera horas, unidades y recargo por capacidad.
  - **AlquilerEquipo:** costo por hora y unidad.
  - **AsesoriaEspecializada:** aplica factor según nivel (`basico`, `general`, `avanzado`).

### 3.5 Sobrecarga adaptada a Python (parámetros opcionales)
- `Cliente.actualizar_contacto(correo=None, telefono=None)`
- `Servicio.calcular_costo(horas=1.0, unidades=1, descuento=0.0, aplicar_impuesto=True)`
- `Reserva.calcular_costo(...)`, `Reserva.procesar(...)` y métodos de creación en `GestorSoftwareFJ` con parámetros opcionales.

## 4. Excepciones personalizadas y manejo avanzado
### 4.1 Excepciones definidas (`software_fj/excepciones.py`)
- `SoftwareFJError` (base)
- `DatoInvalidoError`
- `ClienteNoEncontradoError`
- `ServicioNoDisponibleError`
- `ReservaNoPermitidaError`
- `ParametroFaltanteError`

### 4.2 Uso de estructuras de manejo
- `try/except`: captura de errores de dominio y validación (p. ej. en `main.py` y `gestor.py`).
- `try/except/else`: usado en operaciones del gestor para ejecutar acciones de éxito (almacenamiento y logging) solo cuando no hay errores.
- `try/except/finally`: usado para registrar finalización de operaciones y garantizar continuidad/limpieza.
- `raise`: lanzamiento explícito de excepciones ante datos inválidos, estados no permitidos o parámetros faltantes.
- `raise ... from ...`: encadenamiento de excepciones para preservar la causa original (p. ej. validación de cliente/servicio al crear reservas o registros).

## 5. Sistema de logs
- Archivo: `logs/software_fj.log`
- Configuración: `software_fj/logger_config.py` usando `logging`.
- Registra: fecha y hora, nivel, nombre del logger y mensaje.
- Eventos registrados: inicialización, clientes registrados, servicios creados, reservas creadas/confirmadas/canceladas/procesadas, errores de validación y excepciones controladas en operaciones.

## 6. Validaciones implementadas
- **Clientes:** identificador obligatorio, nombre (mínimo 3 caracteres y solo letras/espacios), correo con formato válido, teléfono numérico (7-15 dígitos), prevención de duplicados por ID y correo.
- **Servicios:** identificador y nombre válidos, tarifa base > 0, impuesto en rango [0,1], disponibilidad, validaciones específicas por tipo (capacidad, tipo de equipo, nivel de asesoría).
- **Reservas:** identificador obligatorio, cliente y servicio existentes/asociados, horas y unidades > 0, control de estados para confirmar/cancelar/procesar.

## 7. Simulación de operaciones (main.py)
El programa ejecuta y demuestra las 10 operaciones requeridas:
1. Registrar un cliente válido.
2. Intentar registrar un cliente con correo inválido (error controlado).
3. Registrar otro cliente válido.
4. Crear servicio de reserva de salas.
5. Crear servicio de alquiler de equipos.
6. Crear servicio de asesorías.
7. Intentar crear un servicio con tarifa incorrecta (error controlado).
8. Crear, confirmar y procesar una reserva correctamente.
9. Intentar crear una reserva con un servicio inexistente (error controlado).
10. Intentar procesar una reserva sin confirmarla previamente (error controlado).

Cada operación se muestra en consola y se registran eventos en el log. Las fallas controladas no detienen la ejecución del programa.

## 8. Pruebas automatizadas y resultados reales
- **Framework:** `unittest`
- **Archivo:** `tests/test_software_fj.py`
- **Cobertura funcional verificada:** registro/validación de clientes, duplicados, errores de tarifa, cálculo polimórfico con impuestos/descuentos, flujo de reserva (crear-confirmar-procesar), reserva con servicio inexistente, procesamiento sin confirmación, consulta de cliente inexistente y generación de log.

**Resultado real de ejecución:**
- `python main.py`: ejecución exitosa de la simulación con 4 errores controlados y continuidad hasta el resumen final.
- `python -m unittest discover -s tests -v`: `Ran 10 tests ... OK`.

Las evidencias textuales se encuentran en:
- `docs/evidencia_ejecucion_main.txt`
- `docs/evidencia_pruebas_unittest.txt`

## 9. Ejecución desde la carpeta raíz
```bash
cd SoftwareFJ_Fase4
python main.py
python -m unittest discover -s tests -v
```

## 10. Consideraciones de entrega
- El sistema no utiliza bases de datos.
- El log se usa para trazabilidad de operaciones y errores.
- El campo de enlace GitHub en el PDF debe completarse manualmente con el enlace real cuando el repositorio sea publicado (no se inventa URL).
