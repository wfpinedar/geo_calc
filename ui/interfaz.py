import flet as ft
from logica_negocio.coordenada import Coordenada
from logica_negocio.punto_geografico import PuntoGeografico
from logica_negocio.calculadora_geografica import CalculadoraGeografica
from persistencia.gestor_historial import GestorHistorial

def main(page: ft.Page):
    # Definir elementos de la interfaz
    page.title = "Calculadora Geográfica"
    gestor_historial = GestorHistorial()

    historial_list_view = ft.ListView(
        expand=False,
        spacing=10,
        padding=10,
        auto_scroll=True 
    )
    # Tabla para mostrar el historial
    historial_table = ft.DataTable(
        
        columns=[
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Distancia (km)")),
            ft.DataColumn(ft.Text("Rumbo")),
            ft.DataColumn(ft.Text("Azimut (°)")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )


    def actualizar_historial():
        registros = gestor_historial.obtener_registros()
        historial_table.rows.clear()
        for registro in registros:
            id_registro = registro.id
            fecha = registro.fecha
            distancia = registro.distancia
            rumbo = registro.rumbo
            azimut = registro.azimut

            historial_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(fecha)),
                        ft.DataCell(ft.Text(f"{distancia:.2f}")),
                        ft.DataCell(ft.Text(rumbo)),
                        ft.DataCell(ft.Text(f"{azimut:.2f}")),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        on_click=lambda e, id=id_registro: editar_registro(id)
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        on_click=lambda e, id=id_registro: eliminar_registro(id)
                                    ),
                                ]
                            )
                        )
                    ]
                )
            )
            historial_list_view.controls.append(historial_table)
        page.update()

    # Evento al presionar el botón de calcular
    def calcular_evento(e):
        try:
            # Coordenadas del Punto 1
            lat1 = Coordenada(
                grados=float(input_lat1_grados.value),
                minutos=float(input_lat1_minutos.value),
                segundos=float(input_lat1_segundos.value),
                direccion=input_lat1_direccion.value  # 'N' o 'S'
            )
            lon1 = Coordenada(
                grados=float(input_lon1_grados.value),
                minutos=float(input_lon1_minutos.value),
                segundos=float(input_lon1_segundos.value),
                direccion=input_lon1_direccion.value  # 'E' o 'W'
            )
            punto1 = PuntoGeografico(latitud=lat1, longitud=lon1)

            # Coordenadas del Punto 2
            lat2 = Coordenada(
                grados=float(input_lat2_grados.value),
                minutos=float(input_lat2_minutos.value),
                segundos=float(input_lat2_segundos.value),
                direccion=input_lat2_direccion.value  # 'N' o 'S'
            )
            lon2 = Coordenada(
                grados=float(input_lon2_grados.value),
                minutos=float(input_lon2_minutos.value),
                segundos=float(input_lon2_segundos.value),
                direccion=input_lon2_direccion.value  # 'E' o 'W'
            )
            punto2 = PuntoGeografico(latitud=lat2, longitud=lon2)

            # Crear instancia de la calculadora
            calculadora = CalculadoraGeografica()

            # Calcular distancia, rumbo y azimut
            distancia = calculadora.calcular_distancia(punto1, punto2)
            rumbo = calculadora.calcular_rumbo(punto1, punto2)
            azimut = calculadora.calcular_azimut(punto1, punto2)
            
            gestor_historial.guardar_registro(punto1, punto2, distancia, rumbo, azimut)
            
            # Mostrar resultados al usuario
            label_resultados.value = f"Distancia: {distancia:.2f} km\n" \
                                     f"Rumbo: {rumbo}\n" \
                                     f"Azimut: {azimut:.2f}°"

            # Actualizar la tabla de historial
            actualizar_historial()
        except Exception as ex:
            label_resultados.value = f"Error: {str(ex)}"
            
        page.update()
    
    # Evento para editar y eliminar registros del historial
    def editar_registro(id_registro):
        print(f"Se esta editando el registro {id_registro}")
        registro = gestor_historial.obtener_un_registro(id_registro)
        def handle_close(e):
            page.close(edit_dialog)
        edit_dialog = ft.AlertDialog(
            title=ft.Text("Editar Registro"),
            content=ft.Text(f"Solo MONESVOL puede editar este registro, te faltan permisos. Pero en su infinita bondad te lo dejara ver. Fecha: {registro.fecha}, Distancia: {registro.distancia}, Rumbo: {registro.rumbo}, Azimut: {registro.azimut}"),
            
            actions=[
                ft.TextButton("Cancelar", on_click=handle_close),
                ft.TextButton("No editar", on_click=handle_close)
            ]
        )
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()

    def eliminar_registro(id_registro):
        
        def confirmar_eliminacion(e):
            gestor_historial.eliminar_registro(id_registro)
            actualizar_historial()
            page.close(confirm_dialog)
        def handle_close(e):
            page.close(confirm_dialog)
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Estás seguro de que deseas eliminar este registro?"),
            actions=[
                ft.TextButton("Cancelar", on_click=handle_close),
                ft.TextButton("Eliminar", on_click=confirmar_eliminacion)
            ]
        )
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    # Campos de entrada para el Punto 1
    input_lat1_grados = ft.TextField(label="Grados", width=100)
    input_lat1_minutos = ft.TextField(label="Minutos", width=100)
    input_lat1_segundos = ft.TextField(label="Segundos", width=100)
    input_lat1_direccion = ft.Dropdown(
        label="Dirección",
        options=[
            ft.dropdown.Option("N"),
            ft.dropdown.Option("S")
        ],
        width=100
    )

    input_lon1_grados = ft.TextField(label="Grados", width=100)
    input_lon1_minutos = ft.TextField(label="Minutos", width=100)
    input_lon1_segundos = ft.TextField(label="Segundos", width=100)
    input_lon1_direccion = ft.Dropdown(
        label="Dirección",
        options=[
            ft.dropdown.Option("E"),
            ft.dropdown.Option("W")
        ],
        width=100
    )

    # Campos de entrada para el Punto 2
    input_lat2_grados = ft.TextField(label="Grados", width=100)
    input_lat2_minutos = ft.TextField(label="Minutos", width=100)
    input_lat2_segundos = ft.TextField(label="Segundos", width=100)
    input_lat2_direccion = ft.Dropdown(
        label="Dirección",
        options=[
            ft.dropdown.Option("N"),
            ft.dropdown.Option("S")
        ],
        width=100
    )

    input_lon2_grados = ft.TextField(label="Grados", width=100)
    input_lon2_minutos = ft.TextField(label="Minutos", width=100)
    input_lon2_segundos = ft.TextField(label="Segundos", width=100)
    input_lon2_direccion = ft.Dropdown(
        label="Dirección",
        options=[
            ft.dropdown.Option("E"),
            ft.dropdown.Option("W")
        ],
        width=100
    )
    #Etiquetas entrada
    label_lat1 = ft.Text(value="Latitud 1")
    label_lon1 = ft.Text(value="Longitud 1")
    label_lat2 = ft.Text(value="Latitud 2")
    label_lon2 = ft.Text(value="Longitud 2")

    # Botón de calcular
    btn_calcular = ft.ElevatedButton(text="Calcular", on_click=calcular_evento)

    # Etiqueta para mostrar los resultados
    label_resultados = ft.Text(value="", size=20)

    # Columna para los campos de entrada y el resultado
    input_column = ft.Column(
        [
            ft.Text("Punto 1", size=20),
            ft.Row([ft.Column([label_lat1, input_lat1_grados, input_lat1_minutos, input_lat1_segundos, input_lat1_direccion]),
                    ft.Column([label_lon1, input_lon1_grados, input_lon1_minutos, input_lon1_segundos, input_lon1_direccion])]),
            ft.Text("Punto 2", size=20),
            ft.Row([ft.Column([label_lat2, input_lat2_grados, input_lat2_minutos, input_lat2_segundos, input_lat2_direccion]),
                    ft.Column([label_lon2, input_lon2_grados, input_lon2_minutos, input_lon2_segundos, input_lon2_direccion])]),
            btn_calcular,
            label_resultados
        ],
        scroll="adaptive", 
        expand=True
    )

    # Columna para el historial
    historial_column = ft.Column(
        [
            ft.Text("Historial de Cálculos", size=20),
            historial_table
        ],
        scroll="adaptive",  # Habilitar desplazamiento si el contenido se desborda
        expand=True
    )
    

    # Organizar los controles en una fila para mostrarlos lado a lado
    page.add(
        ft.Row(
            [input_column, historial_column],
            expand=True,
            scroll="auto"
        )
    )

    # Inicializar la tabla de historial
    actualizar_historial()

if __name__ == "__main__":
    ft.app(target=main)
