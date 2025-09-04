import math, sys, time

#constants 
W, H = 50, 30
THETA_STEP = 0.01
SCALE_Z, SCALE_Y = 10, 10
#
CX, CY = W // 2, H // 2
#
K2 = 50.0
K1 = 35.0
#
def blank_buffers():
    display = [[' ' for _ in range(W)] for _ in range(H)]
    zbuf    = [[-1e9 for _ in range(W)] for _ in range(H)]
    return display, zbuf

def print_frame(m):
    sys.stdout.write("\x1b[H")
    for row in m:
        sys.stdout.write(''.join(row) + '\n')
    sys.stdout.flush()

def heart_yz(t):
    z0 = (-math.cos(t)**3 - math.cos(t)**2 + 2*math.cos(t)) * SCALE_Z
    y0 = ( math.sqrt(2) * math.sin(t)**3 ) * SCALE_Y
    return y0, z0

def render_frame(A):
    disp, zbuf = blank_buffers()
    cosA = math.cos(A)
    sinA = math.sin(A)
    t = 0.0
    while t < 2 * math.pi:
        z0, y0 = heart_yz(t)
        x0 = 0.0
        x = x0 * cosA + z0 * sinA
        y = y0
        z = -x0 * sinA + z0 * cosA
        denom = (K2 + z)
        inv = 1.0 / denom if denom != 0 else 0.0
        xp = int(CX + K1 * x * inv)
        yp = int(CY - K1 * y * inv)
        shade_levels = ".,-~:;=!*#$@"
        idx = min(max(int((inv * K2) * (len(shade_levels) - 1)), 0), len(shade_levels) - 1)
        ch = shade_levels[idx]
        if 0 <= xp < W and 0 <= yp < H:
            if z > zbuf[yp][xp]:
                zbuf[yp][xp] = z
                disp[yp][xp] = ch
        t += THETA_STEP
    return disp

if __name__ == "__main__":
    sys.stdout.write("\x1b[2J\x1b[?25l")
    sys.stdout.flush()
    try:
        A = 0.0
        while True:
            frame = render_frame(A)
            print_frame(frame)
            A += 0.04
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")
        sys.stdout.flush()
