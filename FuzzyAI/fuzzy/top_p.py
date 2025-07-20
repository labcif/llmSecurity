top_p = None

def set_top_p(value: float):
    global top_p
    top_p = value

def get_top_p() -> float:
    return top_p
