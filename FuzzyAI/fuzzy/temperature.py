temperature = None

def set_temperature(value: float):
    global temperature 
    temperature = value

def get_temperature() -> float:
    return temperature