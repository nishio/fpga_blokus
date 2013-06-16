
	assign board_x = (x - 95) / 32;
	assign board_y = (y - 15) / 32;
	//assign  board_vram_addr = x + y * 8'd14;

	assign color =
	x >= 95 && y >= 15 && x < 545 && y < 465 ? (
		(x - 95) % 32 < 2 || (y - 15) % 32 < 2 ? 12'hccc :
		board_vram_out & 6'b100000 ? 12'hf70 :
		board_vram_out & 6'b000100 ? 12'h70f :
		board_vram_out ? 12'h77f :
		12'hddd
	) :
	x < 95 ? (x + y):
	x >= 545 ? (x * y):
	12'heee
	;
