extends Control

# Variables
var possible_designs = ["Design1", "Design2", "Design3"]
var possible_materials = ["Leather", "Fabric", "Wood", "Plexiglass", "Cork"]
var manufacturers = {
	"Apple": ["iPhone SE", "iPhone 12", "iPhone 12 Pro", "iPhone 13", "iPhone 13 Pro"],
	"Samsung": ["Galaxy S21", "Galaxy S21+", "Galaxy Note 20", "Galaxy A52", "Galaxy A72"],
	"Google": ["Pixel 4", "Pixel 4a", "Pixel 5", "Pixel 5a", "Pixel 6"]
}
var phone_orders = {}
var email_var = ""
var amount_var = 0
var manufacturer_var = ""
var model_var = ""
var design_var = ""
var material_var = ""

# Email regex for validation
var email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Coordinates and sizes for the camera lenses of various models
var camera_specs = {
	"iPhone 12": [[148, 45, 265, 145]],
	"Galaxy S21": [[150, 150, 190, 190]]
}

# Custom image variables
var custom_img = null
var custom_img_opacity = 0.9
var custom_img_size = Vector2(540, 540)

func _ready():
	# Ensure signals are not connected multiple times
	if not $"Buttons/PlaceOrderButton".is_connected("pressed", self._on_place_order):
		$"Buttons/PlaceOrderButton".connect("pressed", self._on_place_order)
	if not $"Buttons/SaveOrdersButton".is_connected("pressed", self._on_save_orders):
		$"Buttons/SaveOrdersButton".connect("pressed", self._on_save_orders)
	if not $"Buttons/LoadOrdersButton".is_connected("pressed", self._on_load_orders):
		$"Buttons/LoadOrdersButton".connect("pressed", self._on_load_orders)
	if not $"Buttons/ImportImageButton".is_connected("pressed", self._on_import_image):
		$"Buttons/ImportImageButton".connect("pressed", self._on_import_image)
	#if not $"ManufacturerHBox/Manufacturer".is_connected("item_selected", self._on_manufacturer_selected):
		$"ManufacturerHBox/Manufacturer".connect("item_selected", self._on_manufacturer_selected)
	#if not $"DesignHBox/Design".is_connected("item_selected", self._on_design_selected):
		$"DesignHBox/Design".connect("item_selected", self._on_design_selected)
	#if not $"MaterialHBox/Material".is_connected("item_selected", self._on_material_selected):
		$"MaterialHBox/Material".connect("item_selected", self._on_material_selected)
	
	populate_options()

# Function to populate option buttons
func populate_options():
	var manufacturer_button = $"MainVBox/ManufacturerHBox/Manufacturer"
	var design_button = $"MainVBox/DesignHBox/Design"
	var material_button = $"MainVBox/MaterialHBox/Material"

	# Populate manufacturer options
	for manufacturer in manufacturers.keys():
		manufacturer_button.add_item(manufacturer)

	# Populate design options
	for design in possible_designs:
		design_button.add_item(design)

	# Populate material options
	for material in possible_materials:
		material_button.add_item(material)

# Function to update models based on selected manufacturer
func _on_manufacturer_selected(index: int):
	manufacturer_var = $"MainVBox/ManufacturerHBox/Manufacturer".get_item_text(index)
	update_models()

func update_models():
	var model_button = $"MainVBox/ModelHBox/Model"
	model_button.clear()
	if manufacturer_var in manufacturers:
		for model in manufacturers[manufacturer_var]:
			model_button.add_item(model)

# Function to update the preview image based on selected options
func _on_design_selected(index: int):
	design_var = $"MainVBox/DesignHBox/Design".get_item_text(index)
	update_preview()

func _on_material_selected(index: int):
	material_var = $"MainVBox/MaterialHBox/Material".get_item_text(index)
	update_preview()

func _on_image_selected(path: String):
	custom_img = load(path)
	update_preview()

func update_preview():
	# Example function to update the preview image
	var preview_texture = $"/PreviewTexture"

	# Placeholder logic to update preview based on selected design and material
	# You should replace this with actual image loading logic based on your assets
	if design_var and material_var:
		# Load images based on design_var and material_var
		var design_image = load("res://design/" + design_var + ".png")
		var material_image = load("res://material/" + material_var + ".png")
		
		# Composite the images if needed
		# Update the preview texture
		preview_texture.texture = design_image  # Replace this with actual composited image

func _on_place_order():
	if not validate_email():
		return
	if manufacturer_var == "" or model_var == "":
		show_error("Error", "The fields 'Manufacturer' and 'Model' cannot be empty. Please select a manufacturer and a model.")
		return
	
	amount_var = int($"MainVBox/AmountHBox/Amount".text)
	if amount_var <= 0:
		show_error("Error", "Invalid amount. Must be greater than 0.")
		return
	
	for i in range(amount_var):
		var manufacturer = manufacturer_var
		var model = model_var
		var design = design_var
		var material = material_var

		if design not in possible_designs:
			show_error("Error", "Invalid design. Please select a design from the list.")
			return

		if material not in possible_materials:
			show_error("Error", "Invalid material. Please select a material from the list.")
			return

		var phone_model = manufacturer + " " + model
		if phone_model in phone_orders:
			phone_orders[phone_model].append([1, design, material])
		else:
			phone_orders[phone_model] = [[1, design, material]]

	show_summary()

func validate_email() -> bool:
	var email = $"MainVBox/EmailHBox/Email".text
	if not email_regex.match(email):
		show_error("Error", "Invalid email address. Please try again.")
		return false
	return true

func show_summary():
	var summary = "Order Summary:\n"
	for model in phone_orders.keys():
		for order in phone_orders[model]:
			var amount = order[0]
			var design = order[1]
			var material = order[2]
			summary += model + ": " + str(amount) + " case(s) with design '" + design + "' made of '" + material + "' ordered.\n"
	summary += "\nWe will send you a quote for your cases via email to " + $"MainVBox/EmailHBox/Email".text + "."
	show_message("Order Summary", summary)

func show_error(title: String, message: String):
	var dialog = $ErrorDialog
	dialog.dialog_text = message
	dialog.popup_centered()

func show_message(_title: String, message: String):
	var dialog = $MessageDialog
	dialog.dialog_text = message
	dialog.popup_centered()

func _on_save_orders():
	# Implement save orders logic
	pass

func _on_load_orders():
	# Implement load orders logic
	pass

func _on_import_image():
	var dialog = FileDialog.new()
	dialog.mode = "open_file"
	dialog.access = "res"
	dialog.add_filter("*.png;*.jpg;*.jpeg;*.bmp")
	dialog.popup_centered()
	dialog.connect("file_selected", self._on_image_selected)
	add_child(dialog)


