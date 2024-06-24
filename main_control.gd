extends Control

# Variablen
var possible_designs = ["Design1", "Design2", "Design3"]  # Liste der möglichen Designs
var possible_materials = ["Leather", "Fabric", "Wood", "Plexiglass", "Cork"]  # Liste der möglichen Materialien
var manufacturers = {  # Dictionary der Hersteller und deren Modelle
	"Apple": ["iPhone SE", "iPhone 12", "iPhone 12 Pro", "iPhone 13", "iPhone 13 Pro"],
	"Samsung": ["Galaxy S21", "Galaxy S21+", "Galaxy Note 20", "Galaxy A52", "Galaxy A72"],
	"Google": ["Pixel 4", "Pixel 4a", "Pixel 5", "Pixel 5a", "Pixel 6"]
}
var phone_orders = {}  # Dictionary für Telefonbestellungen
var email_var = ""  # Variable zur Speicherung der E-Mail
var amount_var = 0  # Variable zur Speicherung der Bestellmenge
var manufacturer_var = ""  # Variable zur Speicherung des ausgewählten Herstellers
var model_var = ""  # Variable zur Speicherung des ausgewählten Modells
var design_var = ""  # Variable zur Speicherung des ausgewählten Designs
var material_var = ""  # Variable zur Speicherung des ausgewählten Materials

# Regex zur Validierung der E-Mail-Adresse
var email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Koordinaten und Größen für die Kameraobjektive verschiedener Modelle
var camera_specs = {
	"iPhone 12": [[148, 45, 265, 145]],
	"Galaxy S21": [[150, 150, 190, 190]]
}

# Variablen für benutzerdefinierte Bilder
var custom_img = null  # Variable für benutzerdefinierte Bilder
var custom_img_opacity = 0.9  # Variable zur Festlegung der Opazität des benutzerdefinierten Bildes
var custom_img_size = Vector2(540, 540)  # Variable zur Festlegung der Größe des benutzerdefinierten Bildes

func _ready():
	# Sicherstellen, dass Signale nicht mehrfach verbunden werden
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
	
	
	populate_options()  # Funktion zum Füllen der Options-Buttons aufrufen

# Funktion zum Füllen der Options-Buttons
func populate_options():
	var manufacturer_button = $"MainVBox/ManufacturerHBox/Manufacturer"  # Verweis auf den Hersteller-Options-Button
	var design_button = $"MainVBox/DesignHBox/Design"  # Verweis auf den Design-Options-Button
	var material_button = $"MainVBox/MaterialHBox/Material"  # Verweis auf den Material-Options-Button

	# Herstelleroptionen füllen
	for manufacturer in manufacturers.keys():
		manufacturer_button.add_item(manufacturer)

	# Designoptionen füllen
	for design in possible_designs:
		design_button.add_item(design)

	# Materialoptionen füllen
	for material in possible_materials:
		material_button.add_item(material)

# Funktion zur Aktualisierung der Modelle basierend auf dem ausgewählten Hersteller
func _on_manufacturer_selected(index: int):
	manufacturer_var = $"MainVBox/ManufacturerHBox/Manufacturer".get_item_text(index)  # Ausgewählten Hersteller speichern
	update_models()  # Funktion zur Aktualisierung der Modelle aufrufen

func update_models():
	var model_button = $"MainVBox/ModelHBox/Model"  # Verweis auf den Modell-Options-Button
	model_button.clear()  # Vorherige Modelle aus dem Button löschen
	if manufacturer_var in manufacturers:
		for model in manufacturers[manufacturer_var]:  # Modelle des ausgewählten Herstellers hinzufügen
			model_button.add_item(model)

# Funktion zur Aktualisierung des Vorschaubilds basierend auf den ausgewählten Optionen
func _on_design_selected(index: int):
	design_var = $"MainVBox/DesignHBox/Design".get_item_text(index)  # Ausgewähltes Design speichern
	update_preview()  # Funktion zur Aktualisierung der Vorschau aufrufen

func _on_material_selected(index: int):
	material_var = $"MainVBox/MaterialHBox/Material".get_item_text(index)  # Ausgewähltes Material speichern
	update_preview()  # Funktion zur Aktualisierung der Vorschau aufrufen

func _on_image_selected(path: String):
	custom_img = load(path)  # Benutzerdefiniertes Bild laden
	update_preview()  # Funktion zur Aktualisierung der Vorschau aufrufen

func update_preview():
	# Beispielhafte Funktion zur Aktualisierung des Vorschaubilds
	var preview_texture = $"/PreviewTexture"  # Verweis auf die Vorschaubild-Textur

	# Platzhalter-Logik zur Aktualisierung der Vorschau basierend auf dem ausgewählten Design und Material
	if design_var and material_var:
		# Bilder basierend auf design_var und material_var laden
		var design_image = load("res://design/" + design_var + ".png")
		var material_image = load("res://material/" + material_var + ".png")
		
		# Bilder bei Bedarf zusammenführen
		# Vorschaubild aktualisieren
		preview_texture.texture = design_image  # Dies durch das tatsächlich zusammengesetzte Bild ersetzen

func _on_place_order():
	# E-Mail-Validierung
	if not validate_email():
		return
	if manufacturer_var == "" or model_var == "":  # Prüfen, ob Hersteller und Modell ausgewählt sind
		show_error("Error", "The fields 'Manufacturer' and 'Model' cannot be empty. Please select a manufacturer and a model.")
		return
	
	amount_var = int($"MainVBox/AmountHBox/Amount".text)  # Bestellmenge als Ganzzahl speichern
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

		var phone_model = manufacturer + " " + model  # Telefonmodell-String erstellen
		if phone_model in phone_orders:
			phone_orders[phone_model].append([1, design, material])
		else:
			phone_orders[phone_model] = [[1, design, material]]

	show_summary()  # Funktion zur Anzeige der Bestellübersicht aufrufen

func validate_email() -> bool:
	# E-Mail-Adresse validieren
	var email = $"MainVBox/EmailHBox/Email".text
	if not email_regex.match(email):
		show_error("Error", "Invalid email address. Please try again.")
		return false
	return true

func show_summary():
	# Bestellübersicht anzeigen
	var summary = "Order Summary:\n"
	for model in phone_orders.keys():
		for order in phone_orders[model]:
			var amount = order[0]
			var design = order[1]
			var material = order[2]
			summary += model + ": " + str(amount) + " case(s) with design '" + design + "' made of '" + material + "' ordered.\n"
	summary += "\nWe will send you a quote for your cases via email to " + $"MainVBox/EmailHBox/Email".text + "."
	show_message("Order Summary", summary)  # Funktion zur Anzeige der Meldung aufrufen

func show_error(title: String, message: String):
	# Fehlerdialog anzeigen
	var dialog = $ErrorDialog
	dialog.dialog_text = message  # Fehlernachricht setzen
	dialog.popup_centered()  # Dialog zentriert auf dem Bildschirm anzeigen

func show_message(_title: String, message: String):
	# Meldungsdialog anzeigen
	var dialog = $MessageDialog
	dialog.dialog_text = message  # Meldungsnachricht setzen
	dialog.popup_centered()  # Dialog zentriert auf dem Bildschirm anzeigen

func _on_save_orders():
	# Logik zum Speichern von Bestellungen implementieren
	pass

func _on_load_orders():
	# Logik zum Laden von Bestellungen implementieren
	pass

func _on_import_image():
	# Bildimportdialog anzeigen
	var dialog = FileDialog.new()
	dialog.mode = "open_file"  # Dialog-Modus auf "Datei öffnen" setzen
	dialog.access = "res"  # Zugriff auf Ressourcendateien erlauben
	dialog.add_filter("*.png;*.jpg;*.jpeg;*.bmp")  # Dateifilter hinzufügen
	dialog.popup_centered()  # Dialog zentriert auf dem Bildschirm anzeigen
	dialog.connect("file_selected", self._on_image_selected)  # Verbindung zum Bildauswahl-Signal herstellen
	add_child(dialog)  # Dialog als Kindknoten hinzufügen
