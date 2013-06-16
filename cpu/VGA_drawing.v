
    assign board_x = ((x - 95) / 32)[3:0];
    assign board_y = ((y - 15) / 32)[3:0];
    assign board_vram_addr = (board_x + board_y * d14)[7:0];
    assign leftside_addr = x - 4 + (y - 15) * 87;
    assign rightside_addr = 640 * 480 - leftside_addr;

    assign color =
    x >= 95 && y >= 15 && x < 545 && y < 465 ? (
        (x - 95) % 32 < 2 || (y - 15) % 32 < 2 ? 12'hccc :
        board_vram_out & 6'b100000 ? 12'he70 :
        board_vram_out & 6'b000100 ? 12'h70e :
        12'hddd
    ) :
    (x < 95) & leftside_out ? 12'he70:
    (x >= 545) & rightside_out ? 12'h70e:
    12'heee
    ;
