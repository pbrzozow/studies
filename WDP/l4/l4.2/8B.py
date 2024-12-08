def find_max(*args):
    if not args:
        return None
    max_value = args[0]
    for arg in args:
        if arg > max_value:
            max_value = arg
    return max_value

print(find_max(4,6,5))