#include "pd_api.h"

#define TILE_SIZE 8
#define GRID_COLS (400 / TILE_SIZE) // 50
#define GRID_ROWS (240 / TILE_SIZE) // 30

static PlaydateAPI* pd = NULL;

static const LCDPattern kColorCheckerboard = LCDOpaquePattern(
    0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55
);

static int update(void* userdata) {
    // 1. Clear screen to white (floor)
    pd->graphics->clear(kColorWhite);

    // 2. Draw border walls (black solid tiles)
    for (int x = 0; x < GRID_COLS; ++x) {
        // Top wall
        pd->graphics->fillRect(x * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE, kColorBlack);
        // Bottom wall
        pd->graphics->fillRect(x * TILE_SIZE, (GRID_ROWS - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE, kColorBlack);
    }
    for (int y = 1; y < GRID_ROWS - 1; ++y) {
        // Left wall
        pd->graphics->fillRect(0, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, kColorBlack);
        // Right wall
        pd->graphics->fillRect((GRID_COLS - 1) * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, kColorBlack);
    }

    // 3. Draw dood (checkerboard pattern) near screen center
    int dood_col = GRID_COLS / 2;
    int dood_row = GRID_ROWS / 2;
    pd->graphics->fillRect(dood_col * TILE_SIZE, dood_row * TILE_SIZE, TILE_SIZE, TILE_SIZE, (uintptr_t)kColorCheckerboard);

    return 1;
}

#ifdef _WINDLL
__declspec(dllexport)
#endif
int eventHandler(PlaydateAPI* playdate, PDSystemEvent event, uint32_t arg) {
    if (event == kEventInit) {
        pd = playdate;
        pd->system->setUpdateCallback(update, NULL);
    }
    return 0;
}
