import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageChops, ImageDraw, ImageFilter
from typing import Dict, List, Optional, Tuple
import numpy as np

class PhoneCaseOrderSystem:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Phone Case Order System")
        self.root.geometry("800x700")
        self.root.configure(background='#333333')
        self.root.resizable(False, False)

        self.possible_designs: List[str] = ["Design1", "Design2", "Design3"]
        self.possible_materials: List[str] = ["Leder", "Stoff", "Holz", "Plexiglas", "Kork"]
        self.manufacturers: Dict[str, List[str]] = {
            "Apple": ["iPhone SE", "iPhone 12", "iPhone 12 Pro", "iPhone 13", "iPhone 13 Pro"],
            "Samsung": ["Galaxy S21", "Galaxy S21+", "Galaxy Note 20", "Galaxy A52", "Galaxy A52"],
            "Google": ["Pixel 4", "Pixel 4a", "Pixel 5", "Pixel 5a", "Pixel 6"],
        }

        self.camera_specs: Dict[str, List[Tuple[int, int, int, int]]] = {}

        self.custom_img: Optional[Image.Image] = None
        self.custom_img_opacity: float = 0.9
        self.custom_img_size: Tuple[int, int] = (540, 540)

        self.manufacturer_var: tk.StringVar = tk.StringVar()
        self.model_var: tk.StringVar = tk.StringVar()
        self.design_var: tk.StringVar = tk.StringVar()
        self.material_var: tk.StringVar = tk.StringVar()

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

        buttons_frame = ttk.Frame(options_frame)
        buttons_frame.pack(side=tk.TOP, pady=5)

        ttk.Button(buttons_frame, text="Bild importieren", command=self.import_custom_image).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Vorschau exportieren", command=self.export_preview).grid(row=0, column=1, padx=5, pady=5)

        # Create a frame for the preview image in the center
        preview_frame = ttk.Frame(self.root, padding="10 10 10 10")
        preview_frame.pack(expand=True)

        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(expand=True)

    def update_models(self, event: Optional[tk.Event] = None) -> None:
        manufacturer = self.manufacturer_var.get().strip()
        self.model_combobox.set("")
        if manufacturer in self.manufacturers:
            self.model_combobox['values'] = self.manufacturers[manufacturer]

    def import_custom_image(self) -> None:
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if filepath:
            self.custom_img = Image.open(filepath).convert("RGBA")
            self.custom_img.thumbnail(self.custom_img_size)
            self.update_preview()

    def update_preview(self, event: Optional[tk.Event] = None) -> None:
        # Update the preview image based on the selected options
        design = self.design_var.get().strip()
        material = self.material_var.get().strip()
        model = self.model_var.get().strip()
        max_size = 540

        if design:
            try:
                design_image = Image.open(f'images/{design}.png')
                w_d, h_d = design_image.size
                aspect_ratio = w_d / h_d

                if aspect_ratio > 1:
                    new_width = max_size
                    new_height = int(max_size / aspect_ratio)
                else:
                    new_height = max_size
                    new_width = int(max_size * aspect_ratio)

                design_image = design_image.resize((new_width, new_height), Image.LANCZOS)
                design_canvas = Image.new('RGBA', (max_size, max_size), (255, 255, 255, 0))
                design_x = (max_size - new_width) // 2
                design_y = (max_size - new_height) // 2
                design_canvas.paste(design_image, (design_x, design_y), design_image)

                # Create a mask from the dark areas of the design image
                design_mask = design_canvas.convert("L").point(lambda p: 255 if p < 128 else 0)

                final_image = design_canvas.copy()

                if material:
                    material_image = Image.open(f'images/{material}.png')
                    material_image = material_image.resize((max_size, max_size), Image.LANCZOS)
                    material_image = material_image.convert("RGBA")

                    # Apply the design mask to the material image
                    material_image.putalpha(design_mask)

                    camera_mask = self.detect_and_create_camera_mask(model)
                    if camera_mask:
                        combined_mask = ImageChops.darker(design_mask, camera_mask)
                    else:
                        combined_mask = design_mask

                    final_image.paste(material_image, (0, 0), combined_mask)

                if self.custom_img:
                    custom_img_resized = self.custom_img.resize(self.custom_img_size, Image.LANCZOS)
                    custom_img_resized = custom_img_resized.convert("RGBA")

                    # Create a mask from the custom image
                    custom_mask = custom_img_resized.convert("L").point(lambda p: 255 if p > 128 else 0)
                    custom_img_resized.putalpha(custom_mask)

                    # Apply the design mask to the custom image
                    custom_img_resized.putalpha(design_mask)

                    final_image.paste(custom_img_resized, (0, 0), custom_img_resized)

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

    def detect_and_create_camera_mask(self, model: str) -> Optional[Image.Image]:
        max_size = 540
        mask = Image.new("L", (max_size, max_size), 255)
        draw = ImageDraw.Draw(mask)

        if model in self.camera_specs:
            for spec in self.camera_specs[model]:
                draw.rectangle(spec, fill="black")
        else:
            # Detect dark circles in the design image
            design_image = Image.open(f'images/{self.design_var.get()}.png')
            design_image = design_image.resize((max_size, max_size), Image.LANCZOS)
            design_image = design_image.convert("L")
            blurred = design_image.filter(ImageFilter.GaussianBlur(radius=2))
            circles = blurred.point(lambda p: 255 if p < 128 else 0)
            circles = circles.filter(ImageFilter.MinFilter(3))
            circles = circles.filter(ImageFilter.MaxFilter(3))
            circles = circles.filter(ImageFilter.GaussianBlur(radius=2))
            circles = circles.point(lambda p: 255 if p < 128 else 0)

            mask.paste(circles, (0, 0))

        return mask

if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneCase OrderSystem(root)
    root.mainloop()