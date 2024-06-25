import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageChops, ImageDraw, ImageFilter
from typing import Dict, List, Optional, Tuple
import os
import shutil

class PhoneCaseOrderSystem:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Phone Case Order System")
        self.root.geometry("800x800")
        self.root.configure(background='#333333')
        self.root.resizable(False, False)

        self.possible_designs: List[str] = ["None"] + ["Design1", "Design2", "Design3"]
        self.possible_materials: List[str] = ["None"] + ["Leder", "Stoff", "Holz", "Plexiglas", "Kork"]
        self.manufacturers: Dict[str, List[str]] = {
            "Apple": ["iPhone SE", "iPhone 12", "iPhone 12 Pro", "iPhone 13", "iPhone 13 Pro"],
            "Samsung": ["Galaxy S21", "Galaxy S21+", "Galaxy Note 20", "Galaxy A52", "Galaxy A52"],
            "Google": ["Pixel 4", "Pixel 4a", "Pixel 5", "Pixel 5a", "Pixel 6"],
        }

        self.camera_specs: Dict[str, List[Tuple[int, int, int, int]]] = {}

        self.custom_img: Optional[Image.Image] = None
        self.custom_img_opacity: float = 0.9
        self.custom_img_size: Tuple[int, int] = (270, 540)  # Corrected size with swapped dimensions
        self.custom_img_position: Tuple[int, int] = (0, 0)
        self.custom_img_scale: float = 1.0

        self.manufacturer_var: tk.StringVar = tk.StringVar()
        self.model_var: tk.StringVar = tk.StringVar()
        self.design_var: tk.StringVar = tk.StringVar()
        self.material_var: tk.StringVar = tk.StringVar()
        self.custom_image_var: tk.StringVar = tk.StringVar()

        # Set default values for the comboboxes
        self.manufacturer_var.set(list(self.manufacturers.keys())[0])
        self.model_var.set(self.manufacturers[self.manufacturer_var.get()][0])
        self.design_var.set(self.possible_designs[0])
        self.material_var.set(self.possible_materials[0])
        self.custom_image_var.set("None")

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure Dark Mode colors
        style.configure('.', background='#333333', foreground='white')
        style.configure('TLabel', background='#333333', foreground='white')
        style.configure('TCombobox', fieldbackground='#555555', foreground='white')
        style.configure('TButton', background='#555555', foreground='white')

        # Create a frame for the options at the top
        options_frame = ttk.Frame(self.root, padding="10 10 10 10")
        options_frame.pack(side=tk.TOP, fill=tk.X)

        # Create sub-frames for aligned dropdowns
        manufacturer_model_frame = ttk.Frame(options_frame)
        manufacturer_model_frame.pack(side=tk.TOP, pady=5)

        ttk.Label(manufacturer_model_frame, text="Hersteller:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.manufacturer_combobox = ttk.Combobox(manufacturer_model_frame, textvariable=self.manufacturer_var, values=list(self.manufacturers.keys()))
        self.manufacturer_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.manufacturer_combobox.bind("<<ComboboxSelected>>", self.update_models)

        ttk.Label(manufacturer_model_frame, text="Modell:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.model_combobox = ttk.Combobox(manufacturer_model_frame, textvariable=self.model_var, state="readonly")
        self.model_combobox.grid(row=0, column=3, padx=5, pady=5)

        design_material_frame = ttk.Frame(options_frame)
        design_material_frame.pack(side=tk.TOP, pady=5)

        ttk.Label(design_material_frame, text="Design:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.design_combobox = ttk.Combobox(design_material_frame, textvariable=self.design_var, values=self.possible_designs)
        self.design_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.design_combobox.bind("<<ComboboxSelected>>", self.update_preview)

        ttk.Label(design_material_frame, text="Material:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.material_combobox = ttk.Combobox(design_material_frame, textvariable=self.material_var, values=self.possible_materials)
        self.material_combobox.grid(row=0, column=3, padx=5, pady=5)
        self.material_combobox.bind("<<ComboboxSelected>>", self.update_preview)

        ttk.Label(design_material_frame, text="Custom Image:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.E)
        self.custom_image_combobox = ttk.Combobox(design_material_frame, textvariable=self.custom_image_var, values=["None"] + self.list_custom_images())
        self.custom_image_combobox.grid(row=0, column=5, padx=5, pady=5)
        self.custom_image_combobox.bind("<<ComboboxSelected>>", self.load_custom_image)

        buttons_frame = ttk.Frame(options_frame)
        buttons_frame.pack(side=tk.TOP, pady=5)

        ttk.Button(buttons_frame, text="Bild importieren", command=self.import_custom_image).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Vorschau exportieren", command=self.export_preview).grid(row=0, column=1, padx=5, pady=5)

        # Create a frame for the preview image in the center
        preview_frame = ttk.Frame(self.root, padding="10 10 10 10")
        preview_frame.pack(expand=True)

        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(expand=True)

        # Create a frame for the tools at the bottom
        tools_frame = ttk.Frame(self.root, padding="10 10 10 10")
        tools_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Button(tools_frame, text="Move Up", command=lambda: self.move_custom_image(0, -10)).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(tools_frame, text="Move Down", command=lambda: self.move_custom_image(0, 10)).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(tools_frame, text="Move Left", command=lambda: self.move_custom_image(-10, 0)).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(tools_frame, text="Move Right", command=lambda: self.move_custom_image(10, 0)).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(tools_frame, text="Zoom In", command=lambda: self.scale_custom_image(1.1)).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(tools_frame, text="Zoom Out", command=lambda: self.scale_custom_image(0.9)).grid(row=0, column=5, padx=5, pady=5)

    def update_models(self, event: Optional[tk.Event] = None) -> None:
        manufacturer = self.manufacturer_var.get().strip()
        self.model_combobox.set("")
        if manufacturer in self.manufacturers:
            self.model_combobox['values'] = self.manufacturers[manufacturer]
            self.model_var.set(self.manufacturers[manufacturer][0])  # Set default model

    def import_custom_image(self) -> None:
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if filepath:
            self.custom_img = Image.open(filepath).convert("RGBA")
            self.custom_img.thumbnail(self.custom_img_size, Image.LANCZOS)
            self.save_custom_image(filepath)
            self.custom_image_combobox['values'] = ["None"] + self.list_custom_images()
            self.custom_image_var.set(os.path.basename(filepath))
            self.update_preview()

    def save_custom_image(self, filepath: str) -> None:
        if not os.path.exists("imports"):
            os.makedirs("imports")
        shutil.copy(filepath, os.path.join("imports", os.path.basename(filepath)))

    def list_custom_images(self) -> List[str]:
        if not os.path.exists("imports"):
            return []
        return [f for f in os.listdir("imports") if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    def load_custom_image(self, event: Optional[tk.Event] = None) -> None:
        selected_image = self.custom_image_var.get().strip()
        if selected_image != "None":
            filepath = os.path.join("imports", selected_image)
            self.custom_img = Image.open(filepath).convert("RGBA")
            self.custom_img.thumbnail(self.custom_img_size, Image.LANCZOS)
            self.update_preview()

    def update_preview(self, event: Optional[tk.Event] = None) -> None:
        try:
            design = self.design_var.get().strip()
            material = self.material_var.get().strip()
            max_size = self.custom_img_size

            # Base image
            final_image = Image.new('RGBA', max_size, (255, 255, 255, 0))

            # Load and process design image
            if design != "None":
                design_image_path = f'images/{design}.png'
                design_image = Image.open(design_image_path).convert("RGBA")
                design_image.thumbnail(max_size, Image.LANCZOS)
                design_image = ImageOps.fit(design_image, max_size, Image.LANCZOS)
                final_image = Image.alpha_composite(final_image, design_image)

            # Load and process material image
            if material != "None":
                material_image_path = f'images/{material}.png'
                material_image = Image.open(material_image_path).convert("RGBA")
                material_image.thumbnail(max_size, Image.LANCZOS)
                material_image = ImageOps.fit(material_image, max_size, Image.LANCZOS)
                mask = design_image.convert("L").point(lambda x: 255 if x < 128 else 0)
                final_image.paste(material_image, (0, 0), mask)

            # Load and process custom image
            if self.custom_img:
                custom_img_resized = self.custom_img.resize((int(self.custom_img.width * self.custom_img_scale), int(self.custom_img.height * self.custom_img_scale)), Image.LANCZOS)
                custom_img_resized = custom_img_resized.convert("RGBA")
                custom_img_resized = ImageOps.fit(custom_img_resized, max_size, Image.LANCZOS)
                mask = design_image.convert("L").point(lambda x: 255 if x < 128 else 0)
                final_image.paste(custom_img_resized, self.custom_img_position, mask)

            combined_img = ImageTk.PhotoImage(final_image)
            self.preview_label.configure(image=combined_img)
            self.preview_label.image = combined_img

        except Exception as e:
            print(f"Error loading images: {e}")

    def export_preview(self) -> None:
        filepath = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if filepath:
            final_image = self.preview_label.image
            if isinstance(final_image, ImageTk.PhotoImage):
                final_image = ImageTk.getimage(final_image)
                final_image.convert("RGB").save(filepath, "JPEG")

    def move_custom_image(self, dx: int, dy: int) -> None:
        self.custom_img_position = (self.custom_img_position[0] + dx, self.custom_img_position[1] + dy)
        self.update_preview()

    def scale_custom_image(self, scale_factor: float) -> None:
        self.custom_img_scale *= scale_factor
        self.update_preview()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneCaseOrderSystem(root)
    root.mainloop()