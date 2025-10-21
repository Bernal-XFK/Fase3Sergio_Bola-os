#!/usr/bin/env python3
# eps_salvando_vidas.py
# Aplicación: EPS Salvando Vidas - Control de Usuarios
# Autor: Sergio Efren Bolaños Acosta

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from collections import deque

# -------------------------
# Clase de datos (abstracción)
# -------------------------
class EstructuraDatosUsuario:
    def __init__(self, tipo_id, numero_id, nombre, edad, estrato, atencion, copago, fecha_str):
        self.tipo_id = tipo_id
        self.numero_id = numero_id
        self.nombre = nombre
        self.edad = edad
        self.estrato = estrato
        self.atencion = atencion
        self.copago = copago
        self.fecha = fecha_str

    def as_tuple(self):
        return (
            self.tipo_id, self.numero_id, self.nombre, str(self.edad),
            str(self.estrato), self.atencion, f"${self.copago:,}", self.fecha
        )

# -------------------------
# Aplicación GUI
# -------------------------
class EPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Salvando Vidas")
        self.root.geometry("380x220")  # Login más grande
        self.center_window(380, 220)
        self.root.resizable(False, False)
        self.login_window()

    # Función para centrar cualquier ventana
    def center_window(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = int((sw / 2) - (width / 2))
        y = int((sh / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # Confirmación de salida
    def confirmar_salida(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea cerrar la aplicación?"):
            self.root.destroy()

    # ---- LOGIN ----
    def login_window(self):
        frm = ttk.Frame(self.root, padding=20)
        frm.pack(expand=True)

        # Menú superior con "Acerca de"
        menubar = tk.Menu(self.root)
        acerca_menu = tk.Menu(menubar, tearoff=0)
        acerca_menu.add_command(label="Acerca de", command=self.acerca_de)
        menubar.add_cascade(label="Acerca de", menu=acerca_menu)
        self.root.config(menu=menubar)

        ttk.Label(frm, text="Ingrese la contraseña:", font=("Arial", 12)).pack(pady=(0, 10))
        self.pw_var = tk.StringVar()
        pw_entry = ttk.Entry(frm, textvariable=self.pw_var, show="*", width=25)
        pw_entry.pack(pady=5)
        pw_entry.focus()

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Ingresar", width=12, command=self.check_password).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Salir", width=12, command=self.confirmar_salida).pack(side="left", padx=6)

    def acerca_de(self):
        info = (
            "EPS Salvando Vidas\n"
            "Curso: Estructura de Datos\n"
            "Estudiante: Sergio Efren Bolaños Acosta\n"
            "Grupo: 2"
        )
        messagebox.showinfo("Acerca de", info)

    def check_password(self):
        if self.pw_var.get() == "unad":
            self.open_main_window()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")

    # ---- VENTANA PRINCIPAL ----
    def open_main_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("EPS Salvando Vidas – Control de Usuarios")
        self.root.geometry("1000x600")
        self.center_window(1000, 650)  # Centrar ventana principal
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_salida)
        self.root.resizable(True, True)

        # Datos internos
        self.pila = []
        self.cola = deque()
        self.lista = []

        main = ttk.Frame(self.root, padding=8)
        main.pack(fill="both", expand=True)

        form_frame = ttk.Labelframe(main, text="Registro de Usuarios", padding=8)
        form_frame.pack(side="top", fill="x")

        ttk.Label(form_frame, text="Tipo ID:").grid(column=0, row=0, sticky="w")
        self.tipo_id_var = tk.StringVar(value="CC")
        ttk.Combobox(form_frame, textvariable=self.tipo_id_var, values=["CC","CE","NUIP","PAS"], state="readonly", width=6).grid(column=1, row=0, padx=4)

        ttk.Label(form_frame, text="Número ID:").grid(column=2, row=0, sticky="w", padx=(12,0))
        self.num_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.num_id_var).grid(column=3, row=0, padx=4)

        ttk.Label(form_frame, text="Nombre completo:").grid(column=0, row=1, sticky="w", pady=6)
        self.nombre_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nombre_var, width=40).grid(column=1, row=1, columnspan=3, sticky="w", padx=4)

        ttk.Label(form_frame, text="Edad:").grid(column=0, row=2, sticky="w")
        self.edad_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.edad_var, width=6).grid(column=1, row=2, sticky="w", padx=4)

        ttk.Label(form_frame, text="Estrato:").grid(column=2, row=2, sticky="w", padx=(12,0))
        self.estrato_var = tk.StringVar(value="1")
        estrato_menu = ttk.Combobox(form_frame, textvariable=self.estrato_var, values=["1","2","3","4","5","6"], state="readonly", width=4)
        estrato_menu.grid(column=3, row=2, sticky="w", padx=4)

        ttk.Label(form_frame, text="Tipo de atención:").grid(column=0, row=3, sticky="w", pady=6)
        self.atencion_var = tk.StringVar(value="Medicina General")
        ttk.Radiobutton(form_frame, text="Medicina General", value="Medicina General", variable=self.atencion_var, command=self.recalcular_copago).grid(column=1, row=3, sticky="w")
        ttk.Radiobutton(form_frame, text="Examen Laboratorio", value="Examen Laboratorio", variable=self.atencion_var, command=self.recalcular_copago).grid(column=2, row=3, sticky="w")

        ttk.Label(form_frame, text="Copago:").grid(column=0, row=4, sticky="w")
        self.copago_var = tk.StringVar(value="$0")
        ttk.Entry(form_frame, textvariable=self.copago_var, state="readonly", width=12).grid(column=1, row=4, sticky="w", padx=4)

        ttk.Label(form_frame, text="Fecha (dd/mm/aaaa):").grid(column=2, row=4, sticky="w", padx=(12,0))
        self.day_var = tk.StringVar(value=str(datetime.now().day).zfill(2))
        self.month_var = tk.StringVar(value=str(datetime.now().month).zfill(2))
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        tk.Spinbox(form_frame, from_=1, to=31, width=4, textvariable=self.day_var, format="%02.0f").grid(column=3, row=4, sticky="w")
        tk.Spinbox(form_frame, from_=1, to=12, width=4, textvariable=self.month_var, format="%02.0f").grid(column=3, row=4, sticky="e", padx=(40,0))
        tk.Spinbox(form_frame, from_=1900, to=2100, width=6, textvariable=self.year_var).grid(column=3, row=4, sticky="e", padx=(4,0))

        estrato_menu.bind("<<ComboboxSelected>>", lambda e: self.recalcular_copago())

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(column=0, row=5, columnspan=4, pady=10)
        ttk.Button(btn_frame, text="Registrar", command=self.registrar).grid(column=0, row=0, padx=6)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos).grid(column=1, row=0, padx=6)
        ttk.Button(btn_frame, text="Salir", command=self.confirmar_salida).grid(column=2, row=0, padx=6)

        sep = ttk.Separator(main, orient="horizontal")
        sep.pack(fill="x", pady=8)

        lower = ttk.Frame(main)
        lower.pack(fill="both", expand=True)

        ttk.Label(lower, text="Estructura a usar:").pack(anchor="w")
        self.estructura_seleccionada = tk.StringVar(value="Pila")
        ttk.Combobox(lower, textvariable=self.estructura_seleccionada, values=["Pila","Cola","Lista"], state="readonly", width=10).pack(anchor="w", pady=4)

        notebook = ttk.Notebook(lower)
        notebook.pack(fill="both", expand=True)

        # Pila
        self.tab_pila = ttk.Frame(notebook)
        notebook.add(self.tab_pila, text="Pila")
        self.tree_pila = self.crear_treeview(self.tab_pila)
        self.crear_treeview_botones(self.tab_pila, "Pila", self.tree_pila)

        # Cola
        self.tab_cola = ttk.Frame(notebook)
        notebook.add(self.tab_cola, text="Cola")
        self.tree_cola = self.crear_treeview(self.tab_cola)
        self.crear_treeview_botones(self.tab_cola, "Cola", self.tree_cola)

        # Lista
        self.tab_lista = ttk.Frame(notebook)
        notebook.add(self.tab_lista, text="Lista")
        self.tree_lista = self.crear_treeview(self.tab_lista)
        buscador_frame = ttk.Frame(self.tab_lista)
        buscador_frame.pack(fill="x", pady=4)
        ttk.Label(buscador_frame, text="Buscador (Número ID para eliminar):").pack(side="left")
        self.buscador_var = tk.StringVar()
        ttk.Entry(buscador_frame, textvariable=self.buscador_var, width=20).pack(side="left", padx=6)
        self.crear_treeview_botones(self.tab_lista, "Lista", self.tree_lista)

        self.recalcular_copago()

    def crear_treeview(self, parent):
        cols = ("Tipo", "ID", "Nombre", "Edad", "Estrato", "Atención", "Copago", "Fecha")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=110, anchor="center")
        tree.pack(fill="both", expand=True, padx=6, pady=6)
        return tree

    def crear_treeview_botones(self, parent, estructura, tree):
        btns = ttk.Frame(parent)
        btns.pack(fill="x", pady=4)
        ttk.Button(btns, text="Reporte", command=lambda e=estructura: self.mostrar_reporte(e)).pack(side="left", padx=4)
        ttk.Button(btns, text="Eliminar", command=lambda e=estructura: self.eliminar_registro(e)).pack(side="left", padx=4)

    def recalcular_copago(self):
        try:
            estrato = int(self.estrato_var.get())
        except Exception:
            estrato = 1
        atencion = self.atencion_var.get()
        if atencion == "Medicina General":
            tabla = {1:0, 2:0, 3:10000, 4:15000, 5:20000, 6:30000}
        else:
            tabla = {1:0, 2:0, 3:0, 4:5000, 5:10000, 6:20000}
        self.copago_var.set(f"${tabla.get(estrato,0):,}")

    def validar_campos(self):
        if not self.num_id_var.get().isdigit():
            messagebox.showwarning("Validación", "El número de identificación debe ser numérico.")
            return False
        if not self.nombre_var.get().replace(" ", "").isalpha():
            messagebox.showwarning("Validación", "El nombre solo debe contener letras y espacios.")
            return False
        if not self.edad_var.get().isdigit():
            messagebox.showwarning("Validación", "La edad debe ser numérica.")
            return False
        return True

    def registrar(self):
        if not self.validar_campos():
            return
        tipo = self.tipo_id_var.get()
        numero = self.num_id_var.get()
        nombre = self.nombre_var.get().strip().title()
        edad = int(self.edad_var.get())
        estrato = int(self.estrato_var.get())
        atencion = self.atencion_var.get()
        copago = int(self.copago_var.get().replace("$","").replace(",","") or "0")
        fecha = f"{self.day_var.get()}/{self.month_var.get()}/{self.year_var.get()}"

        usuario = EstructuraDatosUsuario(tipo, numero, nombre, edad, estrato, atencion, copago, fecha)
        estructura = self.estructura_seleccionada.get()

        if estructura == "Pila":
            self.pila.append(usuario)
            self.tree_pila.insert("", "end", values=usuario.as_tuple())
        elif estructura == "Cola":
            self.cola.append(usuario)
            self.tree_cola.insert("", "end", values=usuario.as_tuple())
        else:
            self.lista.append(usuario)
            self.tree_lista.insert("", "end", values=usuario.as_tuple())

        messagebox.showinfo("Registro", f"Usuario agregado a la {estructura}.")
        self.limpiar_campos(True)

    def limpiar_campos(self, keep_structure=False):
        self.num_id_var.set("")
        self.nombre_var.set("")
        self.edad_var.set("")
        self.estrato_var.set("1")
        self.atencion_var.set("Medicina General")
        self.recalcular_copago()
        if not keep_structure:
            self.estructura_seleccionada.set("Pila")

    def mostrar_reporte(self, estructura):
        if estructura == "Pila":
            total = sum(u.copago for u in self.pila)
            messagebox.showinfo("Reporte - Pila", f"Suma total de copagos: ${total:,}")
        elif estructura == "Cola":
            messagebox.showinfo("Reporte - Cola", f"Registros en cola: {len(self.cola)}")
        elif estructura == "Lista":
            if len(self.lista) == 0:
                messagebox.showinfo("Reporte - Lista", "No hay registros en la lista.")
            else:
                prom = sum(u.edad for u in self.lista)/len(self.lista)
                messagebox.showinfo("Reporte - Lista", f"Promedio de edad: {prom:.2f}")

    def eliminar_registro(self, estructura):
        if estructura == "Pila":
            if not self.pila:
                messagebox.showwarning("Eliminar", "La pila está vacía.")
                return
            if not messagebox.askyesno("Eliminar", "¿Desea desapilar el último registro?"):
                return
            self.pila.pop()
            children = self.tree_pila.get_children()
            if children:
                self.tree_pila.delete(children[-1])
            messagebox.showinfo("Eliminar", "Registro desapilado correctamente.")
        elif estructura == "Cola":
            if not self.cola:
                messagebox.showwarning("Eliminar", "La cola está vacía.")
                return
            if not messagebox.askyesno("Eliminar", "¿Desea eliminar el primer registro de la cola?"):
                return
            self.cola.popleft()
            children = self.tree_cola.get_children()
            if children:
                self.tree_cola.delete(children[0])
            messagebox.showinfo("Eliminar", "Registro eliminado correctamente.")
        else:
            buscado = self.buscador_var.get().strip()
            if not buscado:
                messagebox.showwarning("Eliminar", "Ingrese un número de ID en el buscador.")
                return
            for i, u in enumerate(self.lista):
                if u.numero_id == buscado:
                    if messagebox.askyesno("Eliminar", f"¿Desea eliminar a {u.nombre}?"):
                        self.lista.pop(i)
                        for iid in self.tree_lista.get_children():
                            vals = self.tree_lista.item(iid, "values")
                            if vals[1] == buscado:
                                self.tree_lista.delete(iid)
                                break
                        messagebox.showinfo("Eliminar", "Registro eliminado de la lista.")
                    return
            messagebox.showwarning("Eliminar", "No se encontró ese número de identificación.")

def main():
    root = tk.Tk()
    app = EPSApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
