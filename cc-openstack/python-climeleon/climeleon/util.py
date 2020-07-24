def column_align(rows):
    widths = [max(map(len, col)) for col in zip(*rows)]
    return [
        "  ".join(val.ljust(width) for val, width in zip(row, widths))
        for row in rows
    ]
