import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import shutil

# Costruye el arbol de de manera recursiva
def build_tree(dir_path, parent):
    for path in os.scandir(dir_path):
        if path.is_file():
            tree.insert(parent, "end", text=path.name,
                        values=(path.path,), tags=("file",))
        elif path.is_dir():
            folder = tree.insert(parent, "end", text=path.name, values=(
                path.path,), tags=("folder",))
            build_tree(path.path, folder)

# Función para realizar la búsqueda de archivos y carpetas
def search_items():
    search_term = search_entry.get()
    tree.delete(*tree.get_children())  # Borra todos los elementos del árbol
    # Recontruye el árbol inicial
    build_tree(r'C:\Users\Julian\Desktop\Files Manager', "")
    search_tree_items(tree, "", search_term)


# Función
def search_tree_items(tree, parent, search_term):
    for child in tree.get_children(parent):
        item_text = tree.item(child, "text")
        if search_term.lower() in item_text.lower():
            tree.item(child, open=True)
            search_tree_items(tree, child, search_term)
        else:
            tree.detach(child)

# Función para crear una nueva carpeta o archivo
def create_item():
    selected_item = tree.focus()
    item_tags = tree.item(selected_item)["tags"]

    # Verifica si hay valores asociados al elemento seleccionado
    values = tree.item(selected_item).get("values")
    if values:
        current_path = values[0]
    else:
        messagebox.showerror(
            "Error", "Especifique la ruta del nuevo elemento.")
        return

    new_item_name = tk.simpledialog.askstring(
        "Crear", "Ingrese el nombre del nuevo elemento:")

    if new_item_name:
        new_item_path = os.path.join(current_path, new_item_name)

        if "." in new_item_name:  # Si el nombre contiene un punto, se considera una extensión
            try:
                with open(new_item_path, "w") as file:
                    # Escribe contenido vacío para crear el archivo
                    file.write("")
                tree.insert(selected_item, "end", text=new_item_name,
                            values=(new_item_path,), tags=("file",))
                print(f"Archivo creado: {new_item_name}")
            except Exception as e:
                print(f"Error al crear archivo: {str(e)}")
        else:
            try:
                os.makedirs(new_item_path)
                tree.insert(selected_item, "end", text=new_item_name,
                            values=(new_item_path,), tags=("folder",))
                print(f"Carpeta creada: {new_item_name}")
            except Exception as e:
                print(f"Error al crear carpeta: {str(e)}")


# Función para eliminar un archivo o carpeta
def delete_item():
    """
    Elimina el archivo o carpeta seleccionado del árbol.
    """
    selected_item = tree.focus()
    item_tags = tree.item(selected_item)["tags"]
    if "file" in item_tags or "folder" in item_tags:
        response = messagebox.askyesno(
            "Eliminar", "¿Estás seguro de que deseas eliminar este elemento?")
        if response:
            path = tree.item(selected_item)["values"][0]
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                os.rmdir(path)
            tree.delete(selected_item)
            print("Elemento eliminado")

# Función para copiar un archivo o carpeta


def copy_item():
    """
    Copia el archivo o carpeta seleccionado.
    """
    global copied_item
    selected_item = tree.focus()
    item_tags = tree.item(selected_item)["tags"]
    if "file" in item_tags or "folder" in item_tags:
        copied_item = tree.item(selected_item)["values"][0]
        print("Elemento copiado")

# Función para pegar el archivo o carpeta copiado


def paste_item():
    """
    Pega el archivo o carpeta previamente copiado en la ubicación actual del árbol.
    """
    global copied_item
    if copied_item:
        selected_item = tree.focus()
        item_tags = tree.item(selected_item)["tags"]
        if "folder" in item_tags:
            destination_folder = tree.item(selected_item)["values"][0]
            destination_path = os.path.join(
                destination_folder, os.path.basename(copied_item))
            if os.path.isfile(copied_item):
                shutil.copy2(copied_item, destination_path)
                tree.insert(selected_item, "end", text=os.path.basename(
                    copied_item), values=(destination_path,), tags=("file",))
                print("Elemento pegado")
            elif os.path.isdir(copied_item):
                shutil.copytree(copied_item, destination_path)
                tree.insert(selected_item, "end", text=os.path.basename(
                    copied_item), values=(destination_path,), tags=("folder",))
                print("Elemento pegado")
        copied_item = ""

# Función para renombrar un archivo o carpeta
def rename_item():
    selected_item = tree.focus()
    item_tags = tree.item(selected_item)["tags"]
    if "folder" in item_tags:
        folder_path = tree.item(selected_item)["values"][0]
        current_name = os.path.basename(folder_path)
        new_name = simpledialog.askstring(
            "Renombrar Carpeta", "Ingrese el nuevo nombre de la carpeta:", initialvalue=current_name)
        if new_name:
            new_folder_path = os.path.join(
                os.path.dirname(folder_path), new_name)
            try:
                os.rename(folder_path, new_folder_path)
                tree.item(selected_item, text=new_name,
                          values=(new_folder_path,))
                messagebox.showinfo(
                    "Renombrar Carpeta", "La carpeta se ha renombrado correctamente.")
            except Exception as e:
                messagebox.showerror(
                    "Renombrar Carpeta", f"No se pudo renombrar la carpeta:\n{str(e)}")
    else:
        file_path = tree.item(selected_item)["values"][0]
        current_name = os.path.basename(file_path)
        new_name = simpledialog.askstring(
            "Renombrar Archivo", "Ingrese el nuevo nombre del archivo:", initialvalue=current_name)
        if new_name:
            new_file_path = os.path.join(os.path.dirname(file_path), new_name)
            try:
                os.rename(file_path, new_file_path)
                tree.item(selected_item, text=new_name,
                          values=(new_file_path,))
                messagebox.showinfo(
                    "Renombrar Archivo", "El archivo se ha renombrado correctamente.")
            except Exception as e:
                messagebox.showerror(
                    "Renombrar Archivo", f"No se pudo renombrar el archivo:\n{str(e)}")


# Crear la ventana principal
window = tk.Tk()
window.title("Explorador de Archivos")
window.geometry("800x600")  # Cambiar el tamaño de la ventana

# Crear un marco para el árbol y el scrollbar
tree_frame = ttk.Frame(window)
tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Crear el árbol y el scrollbar dentro del marco
tree = ttk.Treeview(tree_frame)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)

# Agregar una barra de búsqueda
search_frame = ttk.Frame(window)
search_frame.pack(side=tk.TOP, fill=tk.X)

search_label = ttk.Label(search_frame, text="Buscar:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = ttk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

search_button = ttk.Button(search_frame, text="Buscar", command=search_items)
search_button.pack(side=tk.LEFT, padx=5)

# Crear un marco para los botones de acciones
action_frame = ttk.Frame(window)
action_frame.pack(side=tk.TOP, fill=tk.X)

create_button = ttk.Button(action_frame, text="Crear", command=create_item)
create_button.pack(side=tk.LEFT, padx=5)

delete_button = ttk.Button(action_frame, text="Eliminar", command=delete_item)
delete_button.pack(side=tk.LEFT, padx=5)

copy_button = ttk.Button(action_frame, text="Copiar", command=copy_item)
copy_button.pack(side=tk.LEFT, padx=5)

paste_button = ttk.Button(action_frame, text="Pegar", command=paste_item)
paste_button.pack(side=tk.LEFT, padx=5)

rename_button = ttk.Button(action_frame, text="Renombrar", command=rename_item)
rename_button.pack(side=tk.LEFT, padx=5)

# Variable global para almacenar la ruta del elemento copiado
copied_item = ""

# Organizar los elementos en la ventana principal
tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
action_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# Construir el árbol inicial
build_tree(r'C:\Users\Julian\Desktop\Files Manager', "")

# Ejecutar el bucle principal del programa
window.mainloop()
