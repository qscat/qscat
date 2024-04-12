def is_field_in_layer(field, layer):
    if layer.fields().indexFromName(field) == -1:
        return False
    return True