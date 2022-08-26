def is_layover(arg_lat, arg_lon):
    arg_lat = float(arg_lat)
    arg_lon = float(arg_lon)

    min_lat = -23.89813
    max_lat = -23.89937
    min_lon = 29.44261
    max_lon = 29.44507

    if max_lat < arg_lat < min_lat:
        if min_lon < arg_lon < max_lon:
            return True
        else:
            return False

    else:
        return False


def is_fuel_wise(arg_lat, arg_lon):
    arg_lat = float(arg_lat)
    arg_lon = float(arg_lon)

    min_lat = -23.89453
    max_lat = -23.89581
    min_lon = 29.44261
    max_lon = 29.44393

    if max_lat < arg_lat < min_lat:
        if min_lon < arg_lon < max_lon:
            return True
        else:
            return False

    else:
        return False
