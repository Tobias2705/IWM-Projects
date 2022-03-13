# https://eduinf.waw.pl/inf/utils/002_roz/2008_06.php

# dx - odległość współrzędnych x1 i x2
# dy - odległość współrzędnych y1, y2
# kx - krok po osi X, 1 lub -1
# ky - krok po osi y, 1 lub -1
# e - wartość wyrażenia body

def BresenhamLine(x1, y1, x2, y2):
    line = []

    if x2 >= x1:
        kx = 1
    else:
        kx = -1
    if y2 >= y1:
        ky = 1
    else:
        ky = -1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    line.append([x1, y1])

    if dy > dx:
        e = dy / 2
        for i in range(0, int(dy)):
            y1 += ky
            e -= dx
            if e < 0:
                x1 += kx
                e += dy
            line.append([x1, y1])
    else:
        e = dx / 2
        for i in range(0, int(dx)):
            x1 += kx
            e -= dy
            if e < 0:
                y1 += ky
                e += dx
            line.append([x1, y1])

    return line
