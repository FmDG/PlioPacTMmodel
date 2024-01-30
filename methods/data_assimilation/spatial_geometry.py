from typing import List
import numpy as np
from scipy.spatial import ConvexHull


def enclosing_points(x: List[int], y: List[int]) -> List[List[int]]:
    """
    Find the vertices of the smallest enclosing triangle around a set of points.

    This function computes the convex hull of a set of points defined by their x and y coordinates.
    It then identifies the vertices that form the smallest enclosing triangle within the convex hull.

    Args:
        x (List[int]): A list of x-coordinates of the points.
        y (List[int]): A list of y-coordinates of the points.

    Returns:
        List[List[int]]: A list of points (vertices) that form the smallest enclosing triangle.
                         Each point is represented as [x, y].

    Raises:
        ValueError: If the lengths of x and y are not the same, indicating a mismatch in dimensions.
    """
    # Error handling: Ensure x and y have the same number of elements
    if len(x) != len(y):
        raise ValueError("X and Y must be of the same dimensions")

    # Combine x and y coordinates into a single array of points
    points = np.column_stack((x, y))

    # Compute the convex hull of the points
    hull = ConvexHull(points)
    bounding_hull = points[hull.vertices]

    return bounding_hull


def midpoint(point1: tuple, point2: tuple):
    """
    Calculate the midpoint between two points in 2D space.

    Args:
        point1 (tuple): A tuple containing the (x, y) coordinates of the first point.
        point2 (tuple): A tuple containing the (x, y) coordinates of the second point.

    Returns:
        tuple: A tuple containing the (x, y) coordinates of the average point.
    """
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the average x-coordinate and y-coordinate
    avg_x = (x1 + x2) / 2
    avg_y = (y1 + y2) / 2

    # Create a tuple representing the average point
    returned_points = (avg_x, avg_y)

    return returned_points
