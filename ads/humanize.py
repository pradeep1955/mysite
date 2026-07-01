def naturalsize(count):
    fcount = float(count)
    k = 1024
    m = k * k
    g = m * k

    if fcount < k:
        return f"{count}B"
    if k <= fcount < m:
        return f"{int(fcount / (k / 10.0)) / 10.0}KB"
    if m <= fcount < g:
        return f"{int(fcount / (m / 10.0)) / 10.0}MB"
    return f"{int(fcount / (g / 10.0)) / 10.0}GB"
