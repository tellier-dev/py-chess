def round_to_position(pos):
    x_int = int(round(pos[0] / 1))
    y_int = int(round(pos[1] / 1))
    x = int((x_int - (x_int % 100)) / 100)
    y = int((y_int - (y_int % 100)) / 100)
    return (y, x)
