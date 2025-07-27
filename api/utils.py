def calculate_points(material_type, weight):
    rates = {
        'plastic': 1,
        'metal': 3,
        'glass': 2,
    }
    points = rates.get(material_type, 0) * weight
    return round(points, 1) 