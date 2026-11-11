from __future__ import annotations

from pathlib import Path

from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(90, 90, 90)
        self.set_x(self.l_margin)
        self.cell(0, 8, "Sistema Integral de Gestion de Clientes, Servicios y Reservas - Software FJ", align="C")
        self.ln(10)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(90, 90, 90)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)


def write_title(pdf: PDF, text: str, size: int = 14):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", size)
    pdf.multi_cell(0, 8, text)
    pdf.ln(2)


def write_subtitle(pdf: PDF, text: str):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 7, text)
    pdf.ln(1)


def write_paragraph(pdf: PDF, text: str):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, text)
    pdf.ln(2)


def write_bullet(pdf: PDF, text: str):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, f"- {text}")
    pdf.ln(1)


def add_placeholder(pdf: PDF, label: str, height: int = 28):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "I", 10)
    pdf.multi_cell(0, 6, f"[Espacio para captura autentica: {label}]")
    y = pdf.get_y()
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, height)
    pdf.ln(height + 4)


def main():
    out = Path(__file__).resolve().parent / "Fase4_Sistema_SoftwareFJ_Sarlyn_Leidys_Murillo_Palacios.pdf"
    pdf = PDF(format="Letter")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(20, 20, 20)

    # Portada
    pdf.add_page()
    pdf.set_y(35)
    pdf.set_font("Helvetica", "B", 14)
    for line in [
        "Universidad Nacional Abierta y a Distancia - UNAD",
        "Escuela de Ciencias Basicas, Tecnologia e Ingenieria (ECBTI)",
        "Programa: Ingenieria de Sistemas",
        "Curso: Programacion",
        "Codigo: 213023",
        "Fase 4 - Componente practico: Practicas simuladas",
    ]:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 8, line, align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 9, "Sistema Integral de Gestion de Clientes, Servicios y Reservas - Software FJ", align="C")
    pdf.ln(16)
    pdf.set_font("Helvetica", "", 12)
    portada_info = [
        "Estudiante: SARLYN LEIDYS MURILLO PALACIOS",
        "Tutor: Wilson Hernan Perez Correa",
        "Fecha de entrega: 10 de noviembre de 2026",
    ]
    for line in portada_info:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 8, line, align="C")

    # Introduccion
    pdf.add_page()
    write_title(pdf, "Introduccion")
    write_paragraph(
        pdf,
        "La programacion orientada a objetos (POO) constituye un paradigma fundamental en el desarrollo de software, "
        "ya que facilita la organizacion del codigo mediante abstracciones que representan entidades del mundo real. "
        "A traves de conceptos como la encapsulacion, la herencia y el polimorfismo, es posible construir sistemas "
        "modulares, reutilizables y mas sencillos de mantener, favoreciendo la calidad y la escalabilidad de las soluciones tecnologicas.",
    )
    write_paragraph(
        pdf,
        "De igual manera, el manejo avanzado de excepciones es esencial para garantizar la estabilidad y la confiabilidad "
        "de las aplicaciones. La anticipacion, control y registro de errores permiten que un sistema continue su ejecucion "
        "ante situaciones imprevistas, protegiendo la integridad de los datos y mejorando la experiencia de uso. "
        "En este contexto, la implementacion de logs proporciona trazabilidad sobre las operaciones realizadas y los fallos detectados.",
    )
    write_paragraph(
        pdf,
        "El presente trabajo desarrolla el Sistema Integral de Gestion de Clientes, Servicios y Reservas para la empresa ficticia "
        "Software FJ, como parte de la Fase 4 - Componente practico: Practicas simuladas del curso Programacion (213023) de la UNAD. "
        "El sistema aplica rigurosamente los principios de la POO y el manejo avanzado de excepciones en Python, administrando la informacion "
        "operativa en memoria y utilizando archivos unicamente para el registro de eventos y errores.",
    )

    # Objetivos
    pdf.add_page()
    write_title(pdf, "Objetivos")
    write_subtitle(pdf, "Objetivo general")
    write_paragraph(
        pdf,
        "Desarrollar un Sistema Integral de Gestion de Clientes, Servicios y Reservas para la empresa ficticia Software FJ, aplicando "
        "los principios de programacion orientada a objetos y el manejo avanzado de excepciones en Python, garantizando un funcionamiento "
        "estable, modular y documentado.",
    )
    write_subtitle(pdf, "Objetivos especificos")
    write_bullet(
        pdf,
        "Disenar e implementar una arquitectura modular en Python que integre clases, herencia, encapsulacion y polimorfismo para la gestion de clientes, servicios y reservas.",
    )
    write_bullet(
        pdf,
        "Aplicar mecanismos de validacion y manejo avanzado de excepciones personalizadas, incluyendo estructuras try/except/else/finally, raise y encadenamiento de excepciones.",
    )
    write_bullet(
        pdf,
        "Verificar el correcto funcionamiento del sistema mediante la simulacion de operaciones, la ejecucion de pruebas automatizadas y el registro de eventos en un archivo de logs.",
    )

    # Desarrollo
    pdf.add_page()
    write_title(pdf, "Desarrollo")
    write_subtitle(pdf, "Arquitectura del sistema")
    write_paragraph(
        pdf,
        "El proyecto se estructuro de forma modular para favorecer la separacion de responsabilidades, la legibilidad y el mantenimiento. "
        "El paquete principal 'software_fj' contiene los modulos de entidades, clientes, servicios, reservas, excepciones, gestor y configuracion de logs. "
        "La informacion operativa se gestiona en memoria mediante objetos y estructuras de datos, mientras que el archivo 'logs/software_fj.log' se utiliza exclusivamente para la trazabilidad.",
    )

    write_subtitle(pdf, "Clases, herencia, encapsulacion y polimorfismo")
    write_paragraph(
        pdf,
        "Se implemento la clase abstracta general 'Entidad', que define el contrato comun de las entidades del sistema. La clase 'Cliente' hereda de 'Entidad' "
        "y encapsula sus datos personales mediante atributos protegidos y propiedades con validaciones estrictas. Para los servicios, se definio la clase abstracta 'Servicio' "
        "y tres clases derivadas: 'ReservaSala', 'AlquilerEquipo' y 'AsesoriaEspecializada'.",
    )
    write_paragraph(
        pdf,
        "El polimorfismo se evidencia en el calculo de costos, donde cada tipo de servicio sobrescribe el metodo 'costo_base' y utiliza reglas especificas. "
        "Asimismo, se sobrescriben metodos como 'descripcion' y 'validar'. Se emplearon parametros opcionales en metodos como 'calcular_costo', 'procesar' y 'actualizar_contacto', "
        "como forma de sobrecarga adaptada al lenguaje Python.",
    )

    write_subtitle(pdf, "Excepciones personalizadas y manejo avanzado")
    write_paragraph(
        pdf,
        "Se definieron las excepciones 'DatoInvalidoError', 'ClienteNoEncontradoError', 'ServicioNoDisponibleError', 'ReservaNoPermitidaError' y 'ParametroFaltanteError'. "
        "El sistema utiliza estructuras 'try/except', 'try/except/else' y 'try/except/finally', ademas de la instruccion 'raise' para senalar condiciones invalidas. "
        "Tambien se implemento encadenamiento de excepciones mediante 'raise ... from ...' para preservar la causa original de los errores y mejorar el diagnostico.",
    )

    write_subtitle(pdf, "Gestion de logs")
    write_paragraph(
        pdf,
        "El modulo 'logger_config.py' configura el registro de eventos utilizando la biblioteca estandar 'logging'. Los mensajes se almacenan en 'logs/software_fj.log' "
        "incluyendo fecha y hora, nivel, nombre del logger y descripcion del evento. Se registran operaciones exitosas, validaciones, cambios de estado de reservas y excepciones controladas.",
    )

    write_subtitle(pdf, "Pruebas realizadas y diez operaciones simuladas")
    write_paragraph(
        pdf,
        "Se desarrollaron pruebas automatizadas con 'unittest' para validar el comportamiento del sistema (registro y validaciones de clientes, creacion de servicios, "
        "calculo de costos, estados de reservas y generacion de logs). Adicionalmente, el archivo 'main.py' ejecuta las diez operaciones solicitadas en la guia:",
    )
    operaciones = [
        "Registro de un cliente valido.",
        "Intento de registro de un cliente con correo invalido (controlado).",
        "Registro de otro cliente valido.",
        "Creacion de un servicio de reserva de salas.",
        "Creacion de un servicio de alquiler de equipos.",
        "Creacion de un servicio de asesorias.",
        "Intento de creacion de un servicio con tarifa incorrecta (controlado).",
        "Creacion, confirmacion y procesamiento de una reserva correctamente.",
        "Intento de creacion de una reserva con un servicio inexistente (controlado).",
        "Intento de procesamiento de una reserva sin confirmarla previamente (controlado).",
    ]
    for op in operaciones:
        write_bullet(pdf, op)
    write_paragraph(
        pdf,
        "Las ejecuciones reales realizadas en el entorno de desarrollo evidenciaron que los errores controlados no interrumpen el flujo del programa y que las pruebas automatizadas "
        "se completaron satisfactoriamente (10 pruebas, estado OK).",
    )

    # Evidencias
    pdf.add_page()
    write_title(pdf, "Evidencias")
    write_paragraph(
        pdf,
        "A continuacion se presentan los espacios destinados para incluir capturas autenticas de la ejecucion y verificacion del sistema. "
        "No se incluyen capturas inventadas; los espacios deben completarse con evidencias reales obtenidas por la estudiante.",
    )
    add_placeholder(pdf, "Ejecucion del programa (python main.py)")
    add_placeholder(pdf, "Operaciones exitosas en consola")
    add_placeholder(pdf, "Operaciones fallidas controladas en consola")
    add_placeholder(pdf, "Contenido del archivo de logs (logs/software_fj.log)")
    add_placeholder(pdf, "Ejecucion de pruebas automatizadas (unittest)")
    add_placeholder(pdf, "Repositorio GitHub (captura del repositorio publicado)")

    # Enlace GitHub
    pdf.add_page()
    write_title(pdf, "Enlace de GitHub")
    write_paragraph(pdf, "Campo para el enlace real del repositorio (completar manualmente tras la publicacion):")
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 11)
    pdf.multi_cell(0, 8, "[PEGAR AQUI EL ENLACE REAL DEL REPOSITORIO GITHUB]")
    pdf.ln(4)
    write_paragraph(
        pdf,
        "Nota: En este entorno no se realizo la publicacion automatica del repositorio ni se genero un enlace. "
        "El proyecto se entrega preparado para su carga en GitHub siguiendo las instrucciones incluidas en el README.md.",
    )

    # Conclusiones
    pdf.add_page()
    write_title(pdf, "Conclusiones")
    write_bullet(
        pdf,
        "La aplicacion de los principios de programacion orientada a objetos permitio estructurar el sistema Software FJ de manera modular y coherente, facilitando la representacion de clientes, servicios y reservas mediante abstracciones claras y reutilizables.",
    )
    write_bullet(
        pdf,
        "El uso de validaciones estrictas y del manejo avanzado de excepciones, junto con el encadenamiento de errores y el registro en logs, contribuyo a la estabilidad del sistema, permitiendo controlar fallos sin interrumpir la ejecucion de las operaciones.",
    )
    write_bullet(
        pdf,
        "La verificacion mediante la simulacion de las diez operaciones y la ejecucion de pruebas automatizadas confirmo el cumplimiento de los requisitos funcionales y tecnicos del proyecto, evidenciando el correcto calculo de costos, la gestion de estados y la trazabilidad de eventos.",
    )

    # Referencias
    pdf.add_page()
    write_title(pdf, "Referencias bibliograficas")
    refs = [
        "Cuevas Alvarez, A. (2016). Python 3: curso practico (pp. 373-385). RA-MA Editorial. https://elibro-net.bibliotecavirtual.unad.edu.co/es/ereader/unad/106404",
        "Romano, F., Baka, B., & Phillips, D. (2019). Getting started with Python: Understand key data structures and use Python in object-oriented programming. Packt Publishing.",
        "Silva, F. D. (2025). Basics of using GitHub [Objeto Virtual de Informacion]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75882",
        "Van Rossum, G., & Drake Jr., F. L. (2024). El tutorial de Python. Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html",
        "Zambrano, J. P. (2025). Introduccion al uso de GitHub [Objeto Virtual de Informacion]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/75876",
    ]
    for ref in refs:
        write_paragraph(pdf, ref)

    pdf.output(str(out))
    print(out)


if __name__ == "__main__":
    main()
