import math

def hex_center_flat_cm(q: int, r: int, R_cm: float):
    x = 1.5 * R_cm * q
    y = math.sqrt(3) * R_cm * (r + q/2)
    return x, y

def hex_distance_from_center_cm(q: int, r: int, R_cm: float):
    x, y = hex_center_flat_cm(q, r, R_cm)
    return math.hypot(x, y)

def R_from_width_height(width_cm: float, height_cm: float):
    # width = 2*R, height = sqrt(3)*R  => R candidates:
    R_from_width = width_cm / 2.0
    R_from_height = height_cm / math.sqrt(3)
    return (R_from_width + R_from_height) / 2.0  # média robusta

def R_with_gap(width_cm: float, height_cm: float, gap_cm: float):
    width_eff = width_cm + gap_cm
    height_eff = height_cm + gap_cm
    return R_from_width_height(width_eff, height_eff)

# Exemplo:
width = 17.0   # cm (lado a lado)
height = 15.0  # cm (top to bottom)
gap = 2.0      # cm separation between hexes
R_no_gap = R_from_width_height(width, height)
R_with_gap = R_with_gap(width, height, gap)

q, r = 2, -3
dist_no_gap = hex_distance_from_center_cm(q, r, R_no_gap)
dist_with_gap = hex_distance_from_center_cm(q, r, R_with_gap)

print("R no gap:", R_no_gap)
print("Dist (no gap):", dist_no_gap)
print("R com gap:", R_with_gap)
print("Dist (com gap):", dist_with_gap)


#python3 -m tests.test_devicesize