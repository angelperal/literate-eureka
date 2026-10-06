from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar
)

from views import ClienteController
from views import EstudianteController


class MenuClientes:
    """VISTA: muestra, pide y presenta. No decide reglas del negocio."""

    TITULO = "SISTEMA DE GESTIÓN DE CLIENTES"
    ANCHO = 85

    def __init__(self, controlador=ClienteController):
        self.__controlador = controlador
        self.__activo = True

        self.__opciones = {
            "1": ("Crear cliente", self.crear),
            "2": ("Ver todos", self.listar),
            "3": ("Buscar", self.buscar),
            "4": ("Ver por id", self.ver_por_id),
            "5": ("Actualizar", self.actualizar),
            "6": ("Eliminar", self.eliminar),
            "7": ("Estadísticas", self.estadisticas),
            "0": ("Salir", self.salir),
        }

    # ==========================================================
    # MÉTODOS ESTÁTICOS
    # ==========================================================

    @staticmethod
    def pausa():
        input("\nPresione Enter para continuar...")

    @staticmethod
    def pedir_entero(etiqueta):
        """Devuelve un entero o None si el usuario escribe algo inválido."""
        try:
            return int(input(etiqueta))
        except ValueError:
            return None

    @staticmethod
    def mostrar_resultado(exito, mensaje):
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    # ==========================================================
    # MÉTODOS DE CLIENTES
    # ==========================================================

    def mostrar_tabla(self, clientes):
        print(
            f"{'ID':<5}"
            f"{'NOMBRE':<25}"
            f"{'EMAIL':<28}"
            f"{'CIUDAD':<15}"
            f"{'TELÉFONO':<12}"
        )

        print("-" * self.ANCHO)

        for cliente in clientes:
            print(
                f"{cliente.id:<5}"
                f"{cliente.nombre_completo:<25}"
                f"{cliente.email:<28}"
                f"{cliente.ciudad:<15}"
                f"{cliente.telefono:<12}"
            )

        print("-" * self.ANCHO)

        imprimir_info(
            f"Total: {len(clientes)} cliente(s)"
        )

    def crear(self):
        imprimir_titulo("CREAR NUEVO CLIENTE")

        datos = {}

        for campo in self.__controlador.MODELO.CAMPOS:
            datos[campo] = input(
                f"{campo.capitalize()}: "
            )

        exito, mensaje = self.__controlador.crear(datos)

        self.mostrar_resultado(
            exito,
            mensaje
        )

        self.pausa()

    def listar(self):
        imprimir_titulo("LISTA DE CLIENTES")

        clientes = self.__controlador.listar()

        if not clientes:
            imprimir_info(
                "Todavía no hay clientes. "
                "Use la opción 1 para crear el primero."
            )
        else:
            self.mostrar_tabla(clientes)

        self.pausa()

    def buscar(self):
        imprimir_titulo("BUSCAR CLIENTE")

        termino = input(
            "Nombre, email, teléfono o ciudad: "
        )

        encontrados = self.__controlador.buscar(
            termino
        )

        if not encontrados:
            imprimir_info(
                f"Ningún cliente coincide con '{termino}'."
            )
        else:
            self.mostrar_tabla(encontrados)

        self.pausa()

    def ver_por_id(self):
        imprimir_titulo("VER CLIENTE POR ID")

        id_cliente = self.pedir_entero(
            "Id del cliente: "
        )

        if id_cliente is None:
            imprimir_error(
                "El id debe ser un número entero"
            )
            return self.pausa()

        cliente = self.__controlador.obtener(
            id_cliente
        )

        if cliente is None:
            imprimir_error(
                f"No existe un cliente con id {id_cliente}"
            )
        else:
            for clave, valor in cliente.a_diccionario().items():
                print(
                    f"  {clave.capitalize():<12}: {valor}"
                )

            imprimir_info(
                f"Dominio del email: "
                f"{cliente.dominio_email}"
            )

        self.pausa()

    def actualizar(self):
        imprimir_titulo("ACTUALIZAR CLIENTE")

        id_cliente = self.pedir_entero(
            "Id del cliente: "
        )

        if id_cliente is None:
            imprimir_error(
                "El id debe ser un número entero"
            )
            return self.pausa()

        cliente = self.__controlador.obtener(
            id_cliente
        )

        if cliente is None:
            imprimir_error(
                f"No existe un cliente con id {id_cliente}"
            )
            return self.pausa()

        imprimir_info(
            f"Editando a {cliente.nombre_completo}"
        )

        print(
            "Deje en blanco el campo que no quiera cambiar.\n"
        )

        cambios = {}

        for campo in self.__controlador.MODELO.CAMPOS:

            actual = getattr(
                cliente,
                campo
            )

            nuevo = input(
                f"{campo.capitalize()} [{actual}]: "
            ).strip()

            if nuevo:
                cambios[campo] = nuevo

        self.mostrar_resultado(
            *self.__controlador.actualizar(
                id_cliente,
                cambios
            )
        )

        self.pausa()

    def eliminar(self):
        imprimir_titulo("ELIMINAR CLIENTE")

        id_cliente = self.pedir_entero(
            "Id del cliente: "
        )

        if id_cliente is None:
            imprimir_error(
                "El id debe ser un número entero"
            )
            return self.pausa()

        cliente = self.__controlador.obtener(
            id_cliente
        )

        if cliente is None:
            imprimir_error(
                f"No existe un cliente con id {id_cliente}"
            )
            return self.pausa()

        imprimir_info(
            f"Se eliminará: {cliente}"
        )

        if confirmar(
            "¿Confirma la eliminación?"
        ):
            self.mostrar_resultado(
                *self.__controlador.eliminar(
                    id_cliente
                )
            )
        else:
            imprimir_info(
                "Operación cancelada"
            )

        self.pausa()

    def estadisticas(self):
        imprimir_titulo(
            "ESTADÍSTICAS"
        )

        datos = self.__controlador.estadisticas()

        print(
            f"  Clientes registrados : "
            f"{datos['total']}"
        )

        print(
            f"  Ciudades distintas   : "
            f"{len(datos['ciudades'])} -> "
            f"{', '.join(datos['ciudades'])}"
        )

        print(
            f"  Dominios de email    : "
            f"{', '.join(datos['dominios'])}"
        )

        print(
            f"  Sin teléfono         : "
            f"{len(datos['sin_telefono'])}"
        )

        self.pausa()

    def salir(self):
        self.__activo = False

        imprimir_info(
            "¡Hasta luego! 👋"
        )

    # ==========================================================
    # MENÚ
    # ==========================================================

    def mostrar_menu(self):
        imprimir_titulo(
            self.TITULO
        )

        for tecla, (texto, _metodo) in self.__opciones.items():
            print(
                f"  {tecla}. {texto}"
            )

        print()

    def ejecutar(self):
        """Bucle principal del menú."""

        while self.__activo:

            self.mostrar_menu()

            tecla = input(
                "Seleccione una opción: "
            ).strip()

            if tecla not in self.__opciones:

                imprimir_error(
                    "Opción no válida"
                )

                self.pausa()
                continue

            _texto, metodo = self.__opciones[tecla]

            metodo()


# ==============================================================
# MENÚ DE ESTUDIANTES
# ==============================================================

class MenuEstudiantes(MenuClientes):

    TITULO = "SISTEMA DE GESTIÓN DE ESTUDIANTES"

    def __init__(self):

        super().__init__(
            controlador=EstudianteController
        )

        # Cambiamos las opciones heredadas de clientes
        # por las opciones de estudiantes.

        self._MenuClientes__opciones["1"] = (
            "Crear estudiante",
            self.crear
        )

        self._MenuClientes__opciones["2"] = (
            "Ver todos los estudiantes",
            self.listar
        )

        self._MenuClientes__opciones["3"] = (
            "Buscar estudiante",
            self.buscar
        )

        self._MenuClientes__opciones["4"] = (
            "Ver estudiante por ID",
            self.ver_por_id
        )

        self._MenuClientes__opciones["5"] = (
            "Actualizar estudiante",
            self.actualizar
        )

        self._MenuClientes__opciones["6"] = (
            "Eliminar estudiante",
            self.eliminar
        )

        self._MenuClientes__opciones["7"] = (
            "Estadísticas",
            self.estadisticas
        )

        self._MenuClientes__opciones["8"] = (
            "Agregar nota",
            self.agregar_nota
        )

        self._MenuClientes__opciones["9"] = (
            "Ver estado y promedio",
            self.ver_estado
        )

        self._MenuClientes__opciones["10"] = (
            "Materias en común",
            self.materias_en_comun
        )

    # ==========================================================
    # TABLA DE ESTUDIANTES
    # ==========================================================

    def mostrar_tabla(self, estudiantes):

        print(
            f"{'ID':<5}"
            f"{'NOMBRE':<25}"
            f"{'EMAIL':<30}"
            f"{'CARNET':<15}"
        )

        print("-" * self.ANCHO)

        for estudiante in estudiantes:

            print(
                f"{estudiante.id:<5}"
                f"{estudiante.nombre_completo:<25}"
                f"{estudiante.email:<30}"
                f"{estudiante.carnet:<15}"
            )

        print("-" * self.ANCHO)

        imprimir_info(
            f"Total: {len(estudiantes)} estudiante(s)"
        )

    # ==========================================================
    # CREAR ESTUDIANTE
    # ==========================================================

    def crear(self):

        imprimir_titulo(
            "CREAR NUEVO ESTUDIANTE"
        )

        datos = {}

        for campo in self._MenuClientes__controlador.MODELO.CAMPOS:

            datos[campo] = input(
                f"{campo.capitalize()}: "
            )

        exito, mensaje = (
            self._MenuClientes__controlador.crear(
                datos
            )
        )

        self.mostrar_resultado(
            exito,
            mensaje
        )

        self.pausa()

    # ==========================================================
    # LISTAR ESTUDIANTES
    # ==========================================================

    def listar(self):

        imprimir_titulo(
            "LISTA DE ESTUDIANTES"
        )

        estudiantes = (
            self._MenuClientes__controlador.listar()
        )

        if not estudiantes:

            imprimir_info(
                "Todavía no hay estudiantes. "
                "Use la opción 1 para crear el primero."
            )

        else:

            self.mostrar_tabla(
                estudiantes
            )

        self.pausa()

    # ==========================================================
    # BUSCAR ESTUDIANTE
    # ==========================================================

    def buscar(self):

        imprimir_titulo(
            "BUSCAR ESTUDIANTE"
        )

        termino = input(
            "Nombre, apellido, email o carnet: "
        )

        encontrados = (
            self._MenuClientes__controlador.buscar(
                termino
            )
        )

        if not encontrados:

            imprimir_info(
                f"Ningún estudiante coincide con "
                f"'{termino}'."
            )

        else:

            self.mostrar_tabla(
                encontrados
            )

        self.pausa()

    # ==========================================================
    # VER ESTUDIANTE POR ID
    # ==========================================================

    def ver_por_id(self):

        imprimir_titulo(
            "VER ESTUDIANTE POR ID"
        )

        id_estudiante = self.pedir_entero(
            "Id del estudiante: "
        )

        if id_estudiante is None:

            imprimir_error(
                "El id debe ser un número entero"
            )

            return self.pausa()

        estudiante = (
            self._MenuClientes__controlador.obtener(
                id_estudiante
            )
        )

        if estudiante is None:

            imprimir_error(
                f"No existe un estudiante "
                f"con id {id_estudiante}"
            )

        else:

            for clave, valor in estudiante.a_diccionario().items():

                print(
                    f"  {clave.capitalize():<12}: {valor}"
                )

            print()

            imprimir_info(
                f"Promedio: "
                f"{estudiante.promedio:.2f}"
            )

            imprimir_info(
                f"Estado: "
                f"{estudiante.estado}"
            )

        self.pausa()

    # ==========================================================
    # ACTUALIZAR ESTUDIANTE
    # ==========================================================

    def actualizar(self):

        imprimir_titulo(
            "ACTUALIZAR ESTUDIANTE"
        )

        id_estudiante = self.pedir_entero(
            "Id del estudiante: "
        )

        if id_estudiante is None:

            imprimir_error(
                "El id debe ser un número entero"
            )

            return self.pausa()

        estudiante = (
            self._MenuClientes__controlador.obtener(
                id_estudiante
            )
        )

        if estudiante is None:

            imprimir_error(
                f"No existe un estudiante "
                f"con id {id_estudiante}"
            )

            return self.pausa()

        imprimir_info(
            f"Editando a "
            f"{estudiante.nombre_completo}"
        )

        print(
            "Deje en blanco el campo "
            "que no quiera cambiar.\n"
        )

        cambios = {}

        for campo in (
            self._MenuClientes__controlador.MODELO.CAMPOS
        ):

            actual = getattr(
                estudiante,
                campo
            )

            nuevo = input(
                f"{campo.capitalize()} "
                f"[{actual}]: "
            ).strip()

            if nuevo:

                cambios[campo] = nuevo

        self.mostrar_resultado(
            *self._MenuClientes__controlador.actualizar(
                id_estudiante,
                cambios
            )
        )

        self.pausa()

    # ==========================================================
    # ELIMINAR ESTUDIANTE
    # ==========================================================

    def eliminar(self):

        imprimir_titulo(
            "ELIMINAR ESTUDIANTE"
        )

        id_estudiante = self.pedir_entero(
            "Id del estudiante: "
        )

        if id_estudiante is None:

            imprimir_error(
                "El id debe ser un número entero"
            )

            return self.pausa()

        estudiante = (
            self._MenuClientes__controlador.obtener(
                id_estudiante
            )
        )

        if estudiante is None:

            imprimir_error(
                f"No existe un estudiante "
                f"con id {id_estudiante}"
            )

            return self.pausa()

        imprimir_info(
            f"Se eliminará: {estudiante}"
        )

        if confirmar(
            "¿Confirma la eliminación?"
        ):

            self.mostrar_resultado(
                *self._MenuClientes__controlador.eliminar(
                    id_estudiante
                )
            )

        else:

            imprimir_info(
                "Operación cancelada"
            )

        self.pausa()

    # ==========================================================
    # ESTADÍSTICAS
    # ==========================================================

    def estadisticas(self):

        imprimir_titulo(
            "ESTADÍSTICAS DE ESTUDIANTES"
        )

        datos = (
            self._MenuClientes__controlador.estadisticas()
        )

        print(
            f"  Estudiantes registrados : "
            f"{datos['total']}"
        )

        print(
            f"  Dominios de email      : "
            f"{', '.join(datos['dominios'])}"
        )

        print(
            f"  Sin teléfono            : "
            f"{len(datos['sin_telefono'])}"
        )

        self.pausa()

    # ==========================================================
    # AGREGAR NOTA
    # ==========================================================

    def agregar_nota(self):

        imprimir_titulo(
            "AGREGAR NOTA A ESTUDIANTE"
        )

        id_est = self.pedir_entero(
            "ID del estudiante: "
        )

        if id_est is None:

            imprimir_error(
                "El ID debe ser un número entero"
            )

            return self.pausa()

        materia = input(
            "Materia: "
        ).strip()

        try:

            nota = float(
                input(
                    "Nota (0-20): "
                )
            )

            exito, mensaje = (
                self._MenuClientes__controlador.agregar_nota(
                    id_est,
                    materia,
                    nota
                )
            )

            self.mostrar_resultado(
                exito,
                mensaje
            )

        except ValueError as error:

            imprimir_error(
                str(error)
            )

        self.pausa()

    # ==========================================================
    # VER ESTADO Y PROMEDIO
    # ==========================================================

    def ver_estado(self):

        imprimir_titulo(
            "ESTADO Y PROMEDIO"
        )

        id_est = self.pedir_entero(
            "ID del estudiante: "
        )

        if id_est is None:

            imprimir_error(
                "El ID debe ser un número entero"
            )

            return self.pausa()

        estudiante = (
            self._MenuClientes__controlador.obtener(
                id_est
            )
        )

        if estudiante:

            imprimir_info(
                f"Estudiante: "
                f"{estudiante.nombre_completo}"
            )

            print(
                f"  Promedio: "
                f"{estudiante.promedio:.2f}"
            )

            print(
                f"  Estado  : "
                f"{estudiante.estado}"
            )

        else:

            imprimir_error(
                f"No existe un estudiante "
                f"con ID {id_est}"
            )

        self.pausa()

    # ==========================================================
    # MATERIAS EN COMÚN
    # ==========================================================

    def materias_en_comun(self):

        imprimir_titulo(
            "MATERIAS EN COMÚN"
        )

        id_a = self.pedir_entero(
            "ID Primer estudiante: "
        )

        id_b = self.pedir_entero(
            "ID Segundo estudiante: "
        )

        if id_a is None or id_b is None:

            imprimir_error(
                "Los dos IDs deben ser números enteros"
            )

            return self.pausa()

        comunes, mensaje = (
            self._MenuClientes__controlador.materias_en_comun(
                id_a,
                id_b
            )
        )

        if comunes is not None:

            imprimir_info(
                f"{mensaje}: "
                f"{', '.join(comunes) if comunes else 'Ninguna'}"
            )

        else:

            imprimir_error(
                mensaje
            )

        self.pausa()


# ==============================================================
# EJECUCIÓN DEL PROGRAMA
# ==============================================================

if __name__ == "__main__":

    try:

        MenuEstudiantes().ejecutar()

    except KeyboardInterrupt:

        print(
            "\nPrograma interrumpido por el usuario."
        )