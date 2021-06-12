
def try_int(val):
    try:
        if int(val):
            return True
        elif len(val.strip('0')) == 0 and len(val) > 0:
            return True
    except:
        return False


def try_float(val):
    try:
        if float(val):
            return True
        elif val.strip('0') == '.':
            return True
    except:
        return False


def try_bool(val):
    if val == 'True' or val == 'False':
        return True
    return False


def try_none(val):
    if val == 'null' or val == 'None':
        return True
    else:
        return False


def smart_cast(val):
    if try_int(val):
        return int(val)
    elif try_float(val):
        return float(val)
    elif try_bool(val):
        return False if val == 'False' else True
    elif try_none(val):
        return None
    else:
        return val
