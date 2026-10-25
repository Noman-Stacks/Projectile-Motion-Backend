"""
Projectile motion formulas for an ideal launch.

Assumptions used by every function in this file:
- Gravity is constant: g = 9.81 m/s^2
- There is no air resistance
- The object is launched from the ground and lands at the same height
- The angle is measured upward from the horizontal

Three summary results:
- Range: how far it lands from the launch point
- Maximum height: the highest point on the path
- Flight time: how long it stays in the air

The graph and the 3D view use the position at many moments in time:
- x = v * cos(theta) * t
- y = v * sin(theta) * t - (1/2) * g * t^2

The launch angle arrives in degrees, because that is what people type.
Python's sin and cos expect radians, so each formula converts the angle first.
"""

import math

# Gravitational acceleration near Earth's surface, in m/s^2.
GRAVITY = 9.81


def calculate_range(velocity, angle_degrees):
    """
    Horizontal distance from launch to landing, in meters.

    Range = (v^2 * sin(2 * theta)) / g
    """
    angle_radians = math.radians(angle_degrees)
    return (velocity ** 2 * math.sin(2 * angle_radians)) / GRAVITY


def calculate_max_height(velocity, angle_degrees):
    """
    Highest point above the launch height, in meters.

    Maximum height = (v^2 * sin(theta)^2) / (2 * g)
    """
    angle_radians = math.radians(angle_degrees)
    sine_of_angle = math.sin(angle_radians)
    return (velocity ** 2 * sine_of_angle ** 2) / (2 * GRAVITY)


def calculate_flight_time(velocity, angle_degrees):
    """
    Total time in the air, in seconds.

    Flight time = (2 * v * sin(theta)) / g
    """
    angle_radians = math.radians(angle_degrees)
    return (2 * velocity * math.sin(angle_radians)) / GRAVITY


def calculate_position(velocity, angle_degrees, time_seconds):
    """
    Horizontal distance and height at one moment.

    Returns a pair: (x in meters, y in meters).
    """
    angle_radians = math.radians(angle_degrees)
    horizontal_distance = velocity * math.cos(angle_radians) * time_seconds
    height = (
        velocity * math.sin(angle_radians) * time_seconds
        - 0.5 * GRAVITY * time_seconds ** 2
    )
    return horizontal_distance, height


def build_trajectory(velocity, angle_degrees, point_count=80):
    """
    Build points along the curved path for the graph and the 3D view.

    Each point is a dictionary: {"x": meters, "y": meters}.
    """
    flight_time = calculate_flight_time(velocity, angle_degrees)

    # A flat launch along the ground never rises, so the path is a single point.
    if flight_time <= 0:
        return [{"x": 0.0, "y": 0.0}]

    points = []
    last_step = point_count - 1

    for step in range(point_count):
        # Spread the points evenly from launch (t = 0) to landing (t = flight time).
        time_seconds = flight_time * step / last_step
        horizontal_distance, height = calculate_position(
            velocity, angle_degrees, time_seconds
        )

        # Landing height is zero. Decimal rounding can leave a tiny negative number.
        if height < 0:
            height = 0

        points.append({
            "x": round(horizontal_distance, 3),
            "y": round(height, 3),
        })

    return points


def calculate_projectile(velocity, angle_degrees):
    """
    Calculate range, maximum height, flight time, and the path.

    velocity: speed in meters per second
    angle_degrees: launch angle in degrees
    """
    return {
        "range": round(calculate_range(velocity, angle_degrees), 2),
        "max_height": round(calculate_max_height(velocity, angle_degrees), 2),
        "flight_time": round(calculate_flight_time(velocity, angle_degrees), 2),
        "trajectory": build_trajectory(velocity, angle_degrees),
    }

