class Ritmo:
    """Gestiona el tiempo empleado por cada kilómetro en sesiones de cardio"""
    def __init__(self, min_km: int, seg_km: int):
        self._min_km = min_km
        self._seg_km = seg_km
