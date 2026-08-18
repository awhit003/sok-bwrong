#!/usr/bin/env python3
"""
tools/generate_walls.py
Generates 1-bit 20x20 pixel-art tile tables for Playdate C projects.
Uses only Python standard library (struct, zlib) - no dependencies required.
"""

import os
import struct
import zlib

TILE_SIZE = 20

def save_png(filename, width, height, pixels):
    """
    Saves an 8-bit grayscale PNG where 0=black, 255=white.
    pixels: list of height lists, each containing width ints (0 or 255).
    """
    raw_data = bytearray()
    for row in pixels:
        raw_data.append(0)  # filter type 0: None
        raw_data.extend(row)
    
    compressed = zlib.compress(bytes(raw_data), 9)
    png = bytearray(b"\x89PNG\r\n\x1a\n")
    
    # IHDR
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    png.extend(struct.pack(">I", len(ihdr)))
    png.extend(b"IHDR")
    png.extend(ihdr)
    png.extend(struct.pack(">I", zlib.crc32(b"IHDR" + ihdr) & 0xffffffff))
    
    # IDAT
    png.extend(struct.pack(">I", len(compressed)))
    png.extend(b"IDAT")
    png.extend(compressed)
    png.extend(struct.pack(">I", zlib.crc32(b"IDAT" + compressed) & 0xffffffff))
    
    # IEND
    png.extend(struct.pack(">I", 0))
    png.extend(b"IEND")
    png.extend(struct.pack(">I", zlib.crc32(b"IEND") & 0xffffffff))
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(png)
    print(f"Generated: {filename} ({width}x{height})")


def make_tile(fill=255):
    return [[fill for _ in range(TILE_SIZE)] for _ in range(TILE_SIZE)]


# =============================================================================
# STYLE 1: Chiseled Flagstone / Heavy Brick (Classic Dungeon)
# =============================================================================
def generate_style1():
    tiles = []

    # 1. Floor Tile (White with subtle stipple)
    t = make_tile(255)
    t[4][5] = 0
    t[14][15] = 0
    t[15][14] = 0
    tiles.append(t)

    # 2. Straight North Wall (Top wall with front face)
    t = make_tile(255)
    # Top border 2px
    for x in range(20):
        t[0][x] = 0
        t[1][x] = 0
    # Mortar horizontal line
    for x in range(20):
        t[7][x] = 0
    # Mortar vertical cuts
    for y in range(2, 7):
        t[y][10] = 0
    for y in range(7, 13):
        t[y][4] = 0
        t[y][16] = 0
    # Front edge 2px solid horizontal divider
    for x in range(20):
        t[13][x] = 0
        t[14][x] = 0
    # Front vertical drop face shadow & vertical mortar
    for y in range(15, 20):
        for x in range(20):
            if x % 2 == 1 and y % 2 == 1:
                t[y][x] = 0
        t[y][4] = 0
        t[y][16] = 0
    tiles.append(t)

    # 3. Straight South Wall
    t = make_tile(255)
    for x in range(20):
        t[18][x] = 0
        t[19][x] = 0
        t[10][x] = 0
    for y in range(0, 10):
        t[y][10] = 0
    for y in range(10, 18):
        t[y][5] = 0
        t[y][15] = 0
    tiles.append(t)

    # 4. Straight West Wall (Left wall)
    t = make_tile(255)
    for y in range(20):
        t[y][0] = 0
        t[y][1] = 0
        t[y][10] = 0
    for x in range(2, 10):
        t[5][x] = 0
        t[15][x] = 0
    for x in range(10, 20):
        t[10][x] = 0
        t[19][x] = 0
    tiles.append(t)

    # 5. Straight East Wall (Right wall)
    t = make_tile(255)
    for y in range(20):
        t[y][18] = 0
        t[y][19] = 0
        t[y][9] = 0
    for x in range(10, 18):
        t[5][x] = 0
        t[15][x] = 0
    for x in range(0, 10):
        t[10][x] = 0
        t[19][x] = 0
    tiles.append(t)

    # 6. Top-Left Corner (NW)
    t = make_tile(255)
    for x in range(20):
        t[0][x] = 0
        t[1][x] = 0
    for y in range(20):
        t[y][0] = 0
        t[y][1] = 0
    # L-joint anchor
    for x in range(2, 12):
        t[12][x] = 0
    for y in range(2, 12):
        t[y][12] = 0
    for x in range(2, 20):
        t[14][x] = 0
    tiles.append(t)

    # 7. Top-Right Corner (NE)
    t = make_tile(255)
    for x in range(20):
        t[0][x] = 0
        t[1][x] = 0
    for y in range(20):
        t[y][18] = 0
        t[y][19] = 0
    # Mirrored L-joint
    for x in range(8, 18):
        t[12][x] = 0
    for y in range(2, 12):
        t[y][7] = 0
    for x in range(0, 18):
        t[14][x] = 0
    tiles.append(t)

    # 8. Bottom-Left Corner (SW)
    t = make_tile(255)
    for x in range(20):
        t[18][x] = 0
        t[19][x] = 0
    for y in range(20):
        t[y][0] = 0
        t[y][1] = 0
    for x in range(2, 12):
        t[8][x] = 0
    for y in range(8, 18):
        t[y][12] = 0
    tiles.append(t)

    # 9. Bottom-Right Corner (SE)
    t = make_tile(255)
    for x in range(20):
        t[18][x] = 0
        t[19][x] = 0
    for y in range(20):
        t[y][18] = 0
        t[y][19] = 0
    for x in range(8, 18):
        t[8][x] = 0
    for y in range(8, 18):
        t[y][7] = 0
    tiles.append(t)

    # 10. Solid Wall Block / Pillar
    t = make_tile(255)
    for x in range(20):
        t[0][x] = 0
        t[19][x] = 0
        t[10][x] = 0
    for y in range(20):
        t[y][0] = 0
        t[y][19] = 0
    for y in range(1, 10):
        t[y][10] = 0
    for y in range(11, 19):
        t[y][5] = 0
        t[y][15] = 0
    tiles.append(t)

    # 11. Checkerboard Dood
    t = make_tile(255)
    for y in range(20):
        for x in range(20):
            if (x + y) % 2 == 0:
                t[y][x] = 0
    tiles.append(t)

    return tiles


# =============================================================================
# STYLE 2: Rough-Hewn Cavern / Natural Rock (Cave / Catacomb)
# =============================================================================
def generate_style2():
    tiles = []

    # 1. Cavern Floor (speckled pebble floor)
    t = make_tile(255)
    for y in range(20):
        for x in range(20):
            if (x * 7 + y * 13) % 31 == 0:
                t[y][x] = 0
    tiles.append(t)

    # 2. Straight North Cavern Wall (Jagged silhouette + rock drop face)
    t = make_tile(255)
    # Jagged top
    jagged_top = [2, 1, 3, 2, 0, 1, 2, 3, 2, 1, 0, 2, 3, 1, 2, 0, 1, 3, 2, 1]
    for x in range(20):
        for y in range(jagged_top[x] + 1):
            t[y][x] = 0
    # Diagonal cracks
    for d in range(6):
        t[4 + d][5 + d] = 0
        t[4 + d][15 - d] = 0
    # Jagged front divider
    jagged_mid = [12, 13, 14, 13, 12, 11, 12, 13, 14, 13, 12, 13, 14, 13, 12, 11, 12, 13, 14, 13]
    for x in range(20):
        t[jagged_mid[x]][x] = 0
        t[jagged_mid[x] + 1][x] = 0
    # Shaded facets below mid
    for x in range(20):
        for y in range(jagged_mid[x] + 2, 20):
            if (x + y) % 3 == 0:
                t[y][x] = 0
    tiles.append(t)

    # 3. Straight South Cavern Wall
    t = make_tile(255)
    jagged_bot = [17, 18, 16, 17, 19, 18, 17, 16, 17, 18, 19, 17, 16, 18, 17, 19, 18, 16, 17, 18]
    for x in range(20):
        for y in range(jagged_bot[x], 20):
            t[y][x] = 0
    for d in range(6):
        t[14 - d][5 + d] = 0
        t[14 - d][15 - d] = 0
    tiles.append(t)

    # 4. Straight West Cavern Wall
    t = make_tile(255)
    jagged_left = [2, 1, 3, 2, 0, 1, 2, 3, 2, 1, 0, 2, 3, 1, 2, 0, 1, 3, 2, 1]
    for y in range(20):
        for x in range(jagged_left[y] + 1):
            t[y][x] = 0
    for d in range(8):
        t[6 + d][3 + (d % 4)] = 0
    tiles.append(t)

    # 5. Straight East Cavern Wall
    t = make_tile(255)
    jagged_right = [17, 18, 16, 17, 19, 18, 17, 16, 17, 18, 19, 17, 16, 18, 17, 19, 18, 16, 17, 18]
    for y in range(20):
        for x in range(jagged_right[y], 20):
            t[y][x] = 0
    for d in range(8):
        t[6 + d][16 - (d % 4)] = 0
    tiles.append(t)

    # 6. Top-Left Cavern Corner (NW - Chamfered apex + deep crack)
    t = make_tile(255)
    for x in range(20):
        for y in range(20):
            if x + y <= 10:
                t[y][x] = 0
    # Crack branching out
    for i in range(7):
        t[7 + i][7 + (i % 2)] = 0
    tiles.append(t)

    # 7. Top-Right Cavern Corner (NE - Chamfered apex + deep crack)
    t = make_tile(255)
    for x in range(20):
        for y in range(20):
            if (19 - x) + y <= 10:
                t[y][x] = 0
    for i in range(7):
        t[7 + i][12 - (i % 2)] = 0
    tiles.append(t)

    # 8. Bottom-Left Cavern Corner (SW)
    t = make_tile(255)
    for x in range(20):
        for y in range(20):
            if x + (19 - y) <= 10:
                t[y][x] = 0
    for i in range(6):
        t[12 - i][7 + (i % 2)] = 0
    tiles.append(t)

    # 9. Bottom-Right Cavern Corner (SE)
    t = make_tile(255)
    for x in range(20):
        for y in range(20):
            if (19 - x) + (19 - y) <= 10:
                t[y][x] = 0
    for i in range(6):
        t[12 - i][12 - (i % 2)] = 0
    tiles.append(t)

    # 10. Solid Rock Boulder / Pillar
    t = make_tile(255)
    for y in range(20):
        for x in range(20):
            dx = abs(x - 9.5)
            dy = abs(y - 9.5)
            if dx + dy >= 9:
                t[y][x] = 0
    t[9][9] = 0
    t[10][10] = 0
    tiles.append(t)

    # 11. Checkerboard Dood
    t = make_tile(255)
    for y in range(20):
        for x in range(20):
            if (x + y) % 2 == 0:
                t[y][x] = 0
    tiles.append(t)

    return tiles


# =============================================================================
# STYLE 3: Fortified Iron-Riveted Slab (Industrial / Vault)
# =============================================================================
def draw_rivet(tile, cx, cy):
    """Draws a 4x4 metallic bolt/rivet with white center."""
    for dy in range(-1, 3):
        for dx in range(-1, 3):
            if 0 <= cy + dy < 20 and 0 <= cx + dx < 20:
                tile[cy + dy][cx + dx] = 0
    # White highlight in middle
    if 0 <= cy < 20 and 0 <= cx < 20:
        tile[cy][cx] = 255


def generate_style3():
    tiles = []

    # 1. Industrial Floor (Clean grid plate with corner seam dots)
    t = make_tile(255)
    t[0][0] = 0
    t[0][19] = 0
    t[19][0] = 0
    t[19][19] = 0
    tiles.append(t)

    # 2. Straight North Iron Wall
    t = make_tile(255)
    # Top border 2px
    for x in range(20):
        t[0][x] = 0
        t[1][x] = 0
        # Lower band
        t[14][x] = 0
        t[15][x] = 0
        # Bottom solid drop shadow
        t[18][x] = 0
        t[19][x] = 0
    # 1px white highlight line at y=16
    for x in range(20):
        t[16][x] = 255
    # Rivets at corners
    draw_rivet(t, 4, 6)
    draw_rivet(t, 15, 6)
    tiles.append(t)

    # 3. Straight South Iron Wall
    t = make_tile(255)
    for x in range(20):
        t[18][x] = 0
        t[19][x] = 0
        t[5][x] = 0
        t[6][x] = 0
    draw_rivet(t, 4, 12)
    draw_rivet(t, 15, 12)
    tiles.append(t)

    # 4. Straight West Iron Wall
    t = make_tile(255)
    for y in range(20):
        t[y][0] = 0
        t[y][1] = 0
        t[y][14] = 0
        t[y][15] = 0
    draw_rivet(t, 6, 4)
    draw_rivet(t, 6, 15)
    tiles.append(t)

    # 5. Straight East Iron Wall
    t = make_tile(255)
    for y in range(20):
        t[y][18] = 0
        t[y][19] = 0
        t[y][4] = 0
        t[y][5] = 0
    draw_rivet(t, 12, 4)
    draw_rivet(t, 12, 15)
    tiles.append(t)

    # 6. Top-Left Corner (NW Bracket + Diamond Bolt)
    t = make_tile(255)
    for x in range(20):
        t[0][x] = 0
        t[1][x] = 0
    for y in range(20):
        t[y][0] = 0
        t[y][1] = 0
    # Outer bracket plate
    for y in range(2, 9):
        for x in range(2, 9):
            if x == 8 or y == 8:
                t[y][x] = 0
    draw_rivet(t, 4, 4)
    tiles.append(t)

    # 7. Top-Right Corner (NE Bracket + Diamond Bolt)
    t = make_tile(255)
    for x in range(20):
        t[0][x] = 0
        t[1][x] = 0
    for y in range(20):
        t[y][18] = 0
        t[y][19] = 0
    for y in range(2, 9):
        for x in range(11, 18):
            if x == 11 or y == 8:
                t[y][x] = 0
    draw_rivet(t, 14, 4)
    tiles.append(t)

    # 8. Bottom-Left Corner (SW)
    t = make_tile(255)
    for x in range(20):
        t[18][x] = 0
        t[19][x] = 0
    for y in range(20):
        t[y][0] = 0
        t[y][1] = 0
    draw_rivet(t, 4, 14)
    tiles.append(t)

    # 9. Bottom-Right Corner (SE)
    t = make_tile(255)
    for x in range(20):
        t[18][x] = 0
        t[19][x] = 0
    for y in range(20):
        t[y][18] = 0
        t[y][19] = 0
    draw_rivet(t, 14, 14)
    tiles.append(t)

    # 10. Solid Iron Vault Pillar / Block
    t = make_tile(255)
    for x in range(20):
        t[0][x] = 0
        t[19][x] = 0
    for y in range(20):
        t[y][0] = 0
        t[y][19] = 0
    # Cross brace lines
    for i in range(20):
        t[i][i] = 0
        t[i][19 - i] = 0
    draw_rivet(t, 9, 9)
    tiles.append(t)

    # 11. Checkerboard Dood
    t = make_tile(255)
    for y in range(20):
        for x in range(20):
            if (x + y) % 2 == 0:
                t[y][x] = 0
    tiles.append(t)

    return tiles


def stitch_table(tiles):
    """Stitches a list of 20x20 tiles horizontally into a single image table strip."""
    count = len(tiles)
    width = count * TILE_SIZE
    height = TILE_SIZE
    strip = [[255 for _ in range(width)] for _ in range(height)]
    
    for idx, tile in enumerate(tiles):
        offset_x = idx * TILE_SIZE
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                strip[y][offset_x + x] = tile[y][x]
    return width, height, strip


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Walltest1: Heavy Brick
    w1, h1, strip1 = stitch_table(generate_style1())
    save_png(os.path.join(root, "src/walltest1/Source/images/walls-table-20-20.png"), w1, h1, strip1)

    # 2. Walltest2: Rough Cavern
    w2, h2, strip2 = stitch_table(generate_style2())
    save_png(os.path.join(root, "src/walltest2/Source/images/walls-table-20-20.png"), w2, h2, strip2)

    # 3. Walltest3: Iron Slab
    w3, h3, strip3 = stitch_table(generate_style3())
    save_png(os.path.join(root, "src/walltest3/Source/images/walls-table-20-20.png"), w3, h3, strip3)


if __name__ == "__main__":
    main()
