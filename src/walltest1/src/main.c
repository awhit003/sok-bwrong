#include "pd_api.h"

#define COLS 20
#define ROWS 12

// Tile Indices (1-based for LCDTileMap)
#define TILE_FLOOR      1
#define TILE_WALL_N     2
#define TILE_WALL_S     3
#define TILE_WALL_W     4
#define TILE_WALL_E     5
#define TILE_CORNER_NW  6
#define TILE_CORNER_NE  7
#define TILE_CORNER_SW  8
#define TILE_CORNER_SE  9
#define TILE_PILLAR     10
#define TILE_DOOD       11

static PlaydateAPI* pd = NULL;
static LCDTileMap* tilemap = NULL;

static void setup_room(void) {
    for (int y = 0; y < ROWS; ++y) {
        for (int x = 0; x < COLS; ++x) {
            uint16_t tile = TILE_FLOOR;

            if (x == 0 && y == 0) {
                tile = TILE_CORNER_NW;
            } else if (x == COLS - 1 && y == 0) {
                tile = TILE_CORNER_NE;
            } else if (x == 0 && y == ROWS - 1) {
                tile = TILE_CORNER_SW;
            } else if (x == COLS - 1 && y == ROWS - 1) {
                tile = TILE_CORNER_SE;
            } else if (y == 0) {
                tile = TILE_WALL_N;
            } else if (y == ROWS - 1) {
                tile = TILE_WALL_S;
            } else if (x == 0) {
                tile = TILE_WALL_W;
            } else if (x == COLS - 1) {
                tile = TILE_WALL_E;
            }

            pd->graphics->tilemap->setTileAtPosition(tilemap, x, y, tile);
        }
    }

    // Place a couple of internal pillars/blocks
    pd->graphics->tilemap->setTileAtPosition(tilemap, 5, 4, TILE_PILLAR);
    pd->graphics->tilemap->setTileAtPosition(tilemap, 14, 4, TILE_PILLAR);
    pd->graphics->tilemap->setTileAtPosition(tilemap, 5, 7, TILE_PILLAR);
    pd->graphics->tilemap->setTileAtPosition(tilemap, 14, 7, TILE_PILLAR);

    // Place Dood in center of room
    pd->graphics->tilemap->setTileAtPosition(tilemap, COLS / 2, ROWS / 2, TILE_DOOD);
}

static int update(void* userdata) {
    pd->graphics->clear(kColorWhite);
    pd->graphics->tilemap->drawAtPoint(tilemap, 0, 0);
    return 1;
}

#ifdef _WINDLL
__declspec(dllexport)
#endif
int eventHandler(PlaydateAPI* playdate, PDSystemEvent event, uint32_t arg) {
    if (event == kEventInit) {
        pd = playdate;
        const char* err = NULL;
        LCDBitmapTable* table = pd->graphics->loadBitmapTable("images/walls-table-20-20", &err);
        if (!table && err) {
            pd->system->error("Error loading bitmap table: %s", err);
        }

        tilemap = pd->graphics->tilemap->newTilemap();
        pd->graphics->tilemap->setSize(tilemap, COLS, ROWS);
        pd->graphics->tilemap->setImageTable(tilemap, table);

        setup_room();
        pd->system->setUpdateCallback(update, NULL);
    }
    return 0;
}
