import json

class Sensor:
    def __init__(self, id, sensor, expected_foot, layout, sector, dist_center, dist_center_cm, q, r, x_c, y_c, angle, angle_norm, range_type, neighbors=None):
        self.id = id
        self.sensor = sensor
        self.layout = layout
        self.sector = sector
        self.expected_foot = expected_foot
        self.dist_center = dist_center
        self.dist_center_cm = dist_center_cm
        self.q = q
        self.r = r
        self.x_c = x_c 
        self.y_c = y_c
        self.angle = angle
        self.angle_norm = angle_norm
        self.range_type = range_type
        
        # neighbors vem como string JSON → dicionário → lista de tuplas
        if isinstance(neighbors, str):
            neighbor_dict = json.loads(neighbors)
            self.neighbors = [(k, v) for k, v in neighbor_dict.items()]
        else:
            self.neighbors = neighbors  # caso já venha como lista de tuplas
        
        # Dados calculados
        self.x = 0
        self.y = 0

        # IDs dos objetos no Canvas
        self.hex_id = None
        self.rect_id = None
        self.status = 0
 
    def __repr__(self):
        return (
            f"Sensor(\n"
            f"  id={self.id},\n"
            f"  sensor={self.sensor},\n"
            f"  layout='{self.layout}',\n"
            f"  sector='{self.sector}',\n"
            f"  expected_foot='{self.expected_foot}',\n"
            f"  dist_center={self.dist_center},\n"
            f"  dist_center_cm={self.dist_center_cm},\n"
            f"  status='{self.status}',\n"
            f"  q={self.q},\n"
            f"  r={self.r},\n"
            f"  x_c={self.x_c},\n"
            f"  y_c={self.y_c},\n"
            f"  angle={self.angle},\n"
            f"  angle_norm={self.angle_norm},\n"
            f"  range_type={self.range_type},\n"
            f"  x={self.x},\n"
            f"  y={self.y},\n"
            f"  hex_id='{self.hex_id}',\n"
            f"  rect_id='{self.rect_id}'\n"
            f")"
        )