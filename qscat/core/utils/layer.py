def is_field_in_layer(field, layer):
    """Check if field exists in the layer.
    
    Args:
        field (str): The field name to check.
        layer (QgsVectorLayer): The layer to check the field in.
    
    Returns:
        bool: True if field exists, False otherwise.
    """
    if layer.fields().indexFromName(field) == -1:
        return False
    return True
