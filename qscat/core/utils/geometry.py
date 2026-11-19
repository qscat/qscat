def as_polylines(geom):
    """Get the line parts of a single or multipart line geometry.

    Z and M values are discarded.

    Args:
        geom (QgsGeometry): LineString or MultiLineString geometry.

    Returns:
        list[list[QgsPointXY]]: List of polylines.
    """
    if geom.isMultipart():
        return geom.asMultiPolyline()
    return [geom.asPolyline()]
