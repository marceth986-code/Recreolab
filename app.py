import tkinter as tk
import customtkinter as ctk
import modelo
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

COLOR_FONDO = "#000000"
COLOR_PANEL = "#111111"

COLORES_CATEGORIAS = {
    "Bebidas": "#1E88E5",
    "Snacks": "#FB8C00",
    "Golosinas": "#D81B60",
    "Todas": "#1F6AA5",
}


class Aplicacion(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("RecreoLab - Kiosco Escolar")
        self.geometry("950x800")
        self.minsize(850, 700)

        self.configure(
            fg_color=COLOR_FONDO
        )

        self.logo_kiosco = ctk.CTkImage(
            light_image=Image.open("kiosco.png"),
            dark_image=Image.open("kiosco.png"),
            size=(200, 200)
        )

        self.logo_bebida = ctk.CTkImage(
            light_image=Image.open("bebida.logo.png"),
            dark_image=Image.open("bebida.logo.png"),
            size=(45, 45)
        )

        self.logo_snack = ctk.CTkImage(
            light_image=Image.open("snack.png"),
            dark_image=Image.open("snack.png"),
            size=(45, 45)
        )

        self.logo_golosina = ctk.CTkImage(
            light_image=Image.open("golosinas.png"),
            dark_image=Image.open("golosinas.png"),
            size=(45, 45)
        )

        self.productos = modelo.catalogo_inicial()
        self.carrito = []
        self.ventas = []

        self.grid_rowconfigure(
            1,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.frame_logo = ctk.CTkFrame(
            self,
            fg_color=COLOR_PANEL,
            corner_radius=18,
            border_width=2,
            border_color="#333333",
            height=210
        )

        self.frame_logo.grid(
            row=0,
            column=0,
            padx=15,
            pady=(10, 5),
            sticky="ew"
        )

        self.frame_logo.grid_columnconfigure(
            0,
            weight=1
        )

        self.frame_logo.grid_rowconfigure(
            0,
            weight=1
        )

        self.lbl_logo = ctk.CTkLabel(
            self.frame_logo,
            image=self.logo_kiosco,
            text=""
        )

        self.lbl_logo.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            sticky="nsew"
        )

        self.tabview = ctk.CTkTabview(
            self,
            fg_color=COLOR_PANEL,
            segmented_button_fg_color="#181818",
            segmented_button_selected_color="#1F6AA5",
            segmented_button_selected_hover_color="#15527D"
        )

        self.tabview.grid(
            row=1,
            column=0,
            padx=15,
            pady=(5, 15),
            sticky="nsew"
        )

        self.tab_kiosco = self.tabview.add(
            "🏪 Kiosco"
        )

        self.tab_presupuesto = self.tabview.add(
            "💡 Sugerir Pares"
        )

        self.setup_kiosco()
        self.setup_presupuesto()
        self.refrescar_kiosco()

    def setup_kiosco(self):

        self.tab_kiosco.configure(
            fg_color=COLOR_PANEL
        )

        self.tab_kiosco.grid_columnconfigure(
            0,
            weight=3
        )

        self.tab_kiosco.grid_columnconfigure(
            1,
            weight=2
        )

        self.tab_kiosco.grid_rowconfigure(
            1,
            weight=1
        )

        frame_filtros = ctk.CTkFrame(
            self.tab_kiosco,
            fg_color="#181818"
        )

        frame_filtros.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=10,
            pady=(5, 10),
            sticky="ew"
        )

        self.entry_busqueda = ctk.CTkEntry(
            frame_filtros,
            placeholder_text="🔍 Buscar producto...",
            fg_color="#000000"
        )

        self.entry_busqueda.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        self.entry_busqueda.bind(
            "<KeyRelease>",
            lambda event: self.refrescar_kiosco()
        )

        self.combo_categoria = ctk.CTkOptionMenu(
            frame_filtros,
            values=[
                "Todas",
                "Bebidas",
                "Snacks",
                "Golosinas"
            ],
            command=lambda cat: self.refrescar_kiosco()
        )

        self.combo_categoria.pack(
            side="right",
            padx=10,
            pady=10
        )

        self.frame_catalogo = ctk.CTkScrollableFrame(
            self.tab_kiosco,
            label_text="Catálogo de Productos",
            fg_color="#000000"
        )

        self.frame_catalogo.grid(
            row=1,
            column=0,
            padx=(10, 5),
            pady=5,
            sticky="nsew"
        )

        frame_derecho = ctk.CTkFrame(
            self.tab_kiosco,
            fg_color="#111111"
        )

        frame_derecho.grid(
            row=1,
            column=1,
            padx=(5, 10),
            pady=5,
            sticky="nsew"
        )

        frame_derecho.grid_rowconfigure(
            1,
            weight=1
        )

        frame_derecho.grid_columnconfigure(
            0,
            weight=1
        )

        self.lbl_mas_vendido = ctk.CTkLabel(
            frame_derecho,
            text="⭐ Más vendido: Ninguno",
            font=ctk.CTkFont(
                weight="bold"
            )
        )

        self.lbl_mas_vendido.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.frame_carrito = ctk.CTkScrollableFrame(
            frame_derecho,
            label_text="Carrito de Compras",
            fg_color="#000000"
        )

        self.frame_carrito.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="nsew"
        )

        self.lbl_total = ctk.CTkLabel(
            frame_derecho,
            text="Total: $0",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        self.lbl_total.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )

        btn_confirmar = ctk.CTkButton(
            frame_derecho,
            text="Confirmar Venta",
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            command=self.confirmar_venta
        )

        btn_confirmar.grid(
            row=3,
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew"
        )

    def refrescar_kiosco(self):

        for child in self.frame_catalogo.winfo_children():
            child.destroy()

        texto_busqueda = self.entry_busqueda.get().lower()
        categoria_sel = self.combo_categoria.get()

        for prod in self.productos:

            coincide_nombre = (
                texto_busqueda in prod.nombre.lower()
            )

            coincide_cat = (
                categoria_sel == "Todas"
                or prod.categoria == categoria_sel
            )

            if coincide_nombre and coincide_cat:

                color_cat = COLORES_CATEGORIAS.get(
                    prod.categoria,
                    "#1F6AA5"
                )

                card = ctk.CTkFrame(
                    self.frame_catalogo,
                    fg_color="#111111",
                    border_width=1,
                    border_color="#333333"
                )

                card.pack(
                    fill="x",
                    padx=5,
                    pady=5
                )

                lbl_cat = ctk.CTkLabel(
                    card,
                    text=f" {prod.categoria.upper()} ",
                    fg_color=color_cat,
                    text_color="white",
                    corner_radius=6,
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold"
                    )
                )

                lbl_cat.pack(
                    anchor="w",
                    padx=10,
                    pady=(8, 2)
                )

                frame_producto = ctk.CTkFrame(
                    card,
                    fg_color="transparent"
                )

                frame_producto.pack(
                    fill="x",
                    padx=5,
                    pady=(0, 8)
                )

                imagen = None

                if prod.categoria == "Bebidas":
                    imagen = self.logo_bebida

                elif prod.categoria == "Snacks":
                    imagen = self.logo_snack

                elif prod.categoria == "Golosinas":
                    imagen = self.logo_golosina

                if imagen is not None:

                    lbl_imagen = ctk.CTkLabel(
                        frame_producto,
                        image=imagen,
                        text=""
                    )

                    lbl_imagen.pack(
                        side="left",
                        padx=(5, 10)
                    )

                lbl_info = ctk.CTkLabel(
                    frame_producto,
                    text=(
                        f"{prod.nombre}\n"
                        f"${prod.precio} | Stock: {prod.stock}"
                    ),
                    justify="left",
                    font=ctk.CTkFont(
                        size=13,
                        weight="bold"
                    )
                )

                lbl_info.pack(
                    side="left",
                    padx=5
                )

                btn_agregar = ctk.CTkButton(
                    frame_producto,
                    text="Agregar",
                    width=80,
                    fg_color=color_cat,
                    state=(
                        "normal"
                        if prod.stock > 0
                        else "disabled"
                    ),
                    command=lambda p=prod:
                    self.agregar_al_carrito(p)
                )

                btn_agregar.pack(
                    side="right",
                    padx=10
                )

        for child in self.frame_carrito.winfo_children():
            child.destroy()

        resumen = {}

        for item in self.carrito:
            resumen[item.codigo] = (
                resumen.get(item.codigo, 0) + 1
            )

        for cod, cant in resumen.items():

            prod = modelo.buscar(
                self.productos,
                cod
            )

            item_frame = ctk.CTkFrame(
                self.frame_carrito,
                fg_color="#111111"
            )

            item_frame.pack(
                fill="x",
                padx=5,
                pady=2
            )

            lbl_item = ctk.CTkLabel(
                item_frame,
                text=(
                    f"{cant}x {prod.nombre} "
                    f"(${prod.precio * cant})"
                )
            )

            lbl_item.pack(
                side="left",
                padx=5
            )

            btn_quitar = ctk.CTkButton(
                item_frame,
                text="❌",
                width=30,
                fg_color="#D32F2F",
                hover_color="#9A0007",
                command=lambda p=prod:
                self.quitar_del_carrito(p)
            )

            btn_quitar.pack(
                side="right",
                padx=5
            )

        total = modelo.total_carrito(
            self.carrito
        )

        self.lbl_total.configure(
            text=f"Total: ${total}"
        )

    def agregar_al_carrito(self, producto):

        try:

            modelo.agregar(
                self.productos,
                self.carrito,
                producto.codigo
            )

            self.refrescar_kiosco()

        except ValueError as e:

            tk.messagebox.showwarning(
                "Atención",
                str(e)
            )

    def quitar_del_carrito(self, producto):

        try:

            modelo.quitar_producto(
                self.carrito,
                producto.codigo
            )

            self.refrescar_kiosco()

        except ValueError as e:

            tk.messagebox.showwarning(
                "Atención",
                str(e)
            )

    def confirmar_venta(self):

        try:

            total = modelo.confirmar(
                self.carrito,
                self.ventas
            )

            tk.messagebox.showinfo(
                "Venta exitosa",
                f"¡Venta realizada por ${total}!"
            )

            self.refrescar_kiosco()

        except ValueError as e:

            tk.messagebox.showwarning(
                "Atención",
                str(e)
            )

    def setup_presupuesto(self):

        self.tab_presupuesto.configure(
            fg_color=COLOR_PANEL
        )

        self.tab_presupuesto.grid_columnconfigure(
            0,
            weight=1
        )

        self.tab_presupuesto.grid_rowconfigure(
            2,
            weight=1
        )

        lbl_inst = ctk.CTkLabel(
            self.tab_presupuesto,
            text=(
                "Ingresá tu presupuesto para sugerir "
                "combinaciones de 2 productos:"
            )
        )

        lbl_inst.grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 5)
        )

        frame_input = ctk.CTkFrame(
            self.tab_presupuesto,
            fg_color="#181818"
        )

        frame_input.grid(
            row=1,
            column=0,
            padx=10,
            pady=5
        )

        self.entry_monto = ctk.CTkEntry(
            frame_input,
            placeholder_text="Monto en $",
            fg_color="#000000"
        )

        self.entry_monto.pack(
            side="left",
            padx=5,
            pady=5
        )

        btn_buscar = ctk.CTkButton(
            frame_input,
            text="Sugerir Pares",
            command=self.calcular_pares
        )

        btn_buscar.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.frame_resultados = ctk.CTkScrollableFrame(
            self.tab_presupuesto,
            label_text="Opciones recomendadas",
            fg_color="#000000"
        )

        self.frame_resultados.grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

    def calcular_pares(self):

        for child in self.frame_resultados.winfo_children():
            child.destroy()

        try:

            monto = float(
                self.entry_monto.get()
            )

            opciones = modelo.sugerir_pares(
                self.productos,
                monto
            )

            if not opciones:

                lbl = ctk.CTkLabel(
                    self.frame_resultados,
                    text="No alcanza para combinar productos."
                )

                lbl.pack(
                    pady=10
                )

                return

            for op in opciones:

                card = ctk.CTkFrame(
                    self.frame_resultados,
                    fg_color="#111111",
                    border_width=1,
                    border_color="#333333"
                )

                card.pack(
                    fill="x",
                    padx=5,
                    pady=5
                )

                txt = (
                    f"• {op[0]} + {op[1]}\n"
                    f"  Total: ${op[2]} "
                    f"(Sobra: ${op[3]})"
                )

                lbl = ctk.CTkLabel(
                    card,
                    text=txt,
                    justify="left"
                )

                lbl.pack(
                    anchor="w",
                    padx=10,
                    pady=5
                )

        except ValueError:

            tk.messagebox.showerror(
                "Error",
                "Ingresá un número válido para el presupuesto."
            )


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()