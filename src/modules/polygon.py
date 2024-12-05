from shapely.geometry import Polygon


def create_polygon(squares):
    polygons = combine_all_polygons(squares)
    match polygons.geom_type:
        case "Polygon":
            return polygon_object(polygons)
        case "MultiPolygon":
            return multi_polygon_object(polygons)
        case _:
            raise Exception("The squares are not divided correctly")


def combine_all_polygons(squares):
    combined_polygon = convert_square_to_polygon(squares[0])
    for square in squares[1:]:
        polygon = convert_square_to_polygon(square)
        combined_polygon = combined_polygon.union(polygon)
    return combined_polygon


def convert_square_to_polygon(square):
    x1, y1 = square[0]
    x2, y2 = square[1]
    return Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])


def polygon_object(polygon):
    return {"type": "Polygon", "coordinates": polygon_arrangement(polygon)}


def polygon_arrangement(polygon):
    polygon_coordinates = [remove_unnecessary_points(list(polygon.exterior.coords))]
    for item in polygon.interiors:
        polygon_coordinates.append(list(item.coords))
    return polygon_coordinates


def remove_unnecessary_points(polygon):
    index = 1
    while index < (len(polygon) - 1):
        for i in range(2):
            if (
                polygon[index][i] == polygon[index - 1][i]
                and polygon[index][i] == polygon[index + 1][i]
            ):
                polygon.pop(index)
                index -= 1
                break
        index += 1
    return polygon


def multi_polygon_object(multi_polygon):
    return {
        "type": "MultiPolygon",
        "coordinates": multi_polygon_arrangement(multi_polygon),
    }


def multi_polygon_arrangement(polygons):
    multi_polygon_coordinates = []
    for polygon in polygons.geoms:
        multi_polygon_coordinates.append(polygon_arrangement(polygon))
    return multi_polygon_coordinates
