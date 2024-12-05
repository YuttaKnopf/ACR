import numpy as np


def classify_shape(approx):
    num_vertices = len(approx)

    match num_vertices:
        case 3:
            return "triangle"
        case 4:
            pts = approx.reshape(4, 2)

            angle1 = np.arctan2(pts[1][1] - pts[0][1], pts[1][0] - pts[0][0])
            angle2 = np.arctan2(pts[2][1] - pts[1][1], pts[2][0] - pts[1][0])

            if np.isclose(angle1, angle2, atol=0.1):
                return "parallelogram"
            return "rectangle"
        case 5:
            return "pentagon"
        case 6:
            return "hexagonal"
        case _:
            return f"Polygon with {num_vertices} vertices"
