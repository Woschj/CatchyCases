document.addEventListener('DOMContentLoaded', function() {
    const manufacturers = {
        "Apple": ["iPhone SE", "iPhone 12", "iPhone 12 Pro", "iPhone 13", "iPhone 13 Pro"],
        "Samsung": ["Galaxy S21", "Galaxy S21+", "Galaxy Note 20", "Galaxy A52", "Galaxy A52"],
        "Google": ["Pixel 4", "Pixel 4a", "Pixel 5", "Pixel 5a", "Pixel 6"],
    };

    const designs = ["None", "Design1", "Design2", "Design3"];
    const materials = ["None", "Leder", "Stoff", "Holz", "Plexiglas", "Kork"];

    const manufacturerSelect = document.getElementById('manufacturer-select');
    const modelSelect = document.getElementById('model-select');
    const designSelect = document.getElementById('design-select');
    const materialSelect = document.getElementById('material-select');
    const previewCanvas = document.getElementById('preview-canvas');
    const ctx = previewCanvas.getContext('2d');

    manufacturerSelect.addEventListener('change', function() {
        const manufacturer = manufacturerSelect.value;
        modelSelect.innerHTML = '<option value="">Select Model</option>';
        if (manufacturer) {
            manufacturers[manufacturer].forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.text = model;
                modelSelect.add(option);
            });
        }
    });

    designSelect.addEventListener('change', function() {
        const design = designSelect.value;
        if (design !== 'None' && design !== '') {
            const img = new Image();
            img.src = '/images/' + design + '.jpg';
            img.onload = function() {
                ctx.drawImage(img, 0, 0, previewCanvas.width, previewCanvas.height);
            };
        } else {
            ctx.clearRect(0, 0, previewCanvas.width, previewCanvas.height);
        }
    });

    materialSelect.addEventListener('change', function() {
        const material = materialSelect.value;
        if (material !== 'None' && material !== '') {
            const img = new Image();
            img.src = '/images/' + material + '.jpg';
            img.onload = function() {
                ctx.drawImage(img, 0, 0, previewCanvas.width, previewCanvas.height);
            };
        } else {
            ctx.clearRect(0, 0, previewCanvas.width, previewCanvas.height);
        }
    });
});
