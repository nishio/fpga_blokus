module VGA(clk, hsync, vsync, rgb_out);
	input clk;
	output hsync, vsync;
	output [11:0]rgb_out;

	wire [11:0]color;
	wire [9:0]x, y;

	wire [3:0] board_x, board_y;
	wire [5:0] board_vram_out;
	wire [7:0] board_vram_addr;
	board_vram_14x14x6bit	board_vram_14x14x6bit_inst (
	.clock ( clk ),
	.data ( 0 ),
	.rdaddress ( board_vram_addr ),
	.wraddress ( 0 ),
	.wren ( 0 ),
	.q ( board_vram_out )
	);

	wire leftside_out;
	wire [15:0] leftside_addr;
	side_vram_87x450x1bit_39150bits side_vram_87x450x1bit_39150bits_inst (
        .clock ( clk ),
        .data ( 0 ),
        .rdaddress ( leftside_addr ),
        .wraddress ( 0 ),
        .wren ( 0 ),
        .q ( leftside_out )
        );

	wire rightside_out;
	wire [15:0] rightside_addr;
	assign rightside_out = rightside_addr[5];
	
`include "VGA_clock_handling.v"

	assign x = hcount - 10'd144;
	assign y = vcount - 10'd35;

`include "cpu/VGA_drawing.v"

	assign rgb_out = (i_hdisp & i_vdisp) ? color : 12'h000;
endmodule
