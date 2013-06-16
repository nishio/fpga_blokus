module VGA(clk, hsync, vsync, rgb_out);
	input clk;
	output hsync, vsync;
	output [11:0]rgb_out;

	wire [11:0]color;

	wire [9:0]x, y;
	//wire [9:0]dx, dy;
	//wire q_sig;
	//reg rgb_reg;

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

	
	
	
	reg vga_clk, i_hs, i_vs, i_hdisp, i_vdisp;
	reg [9:0]hcount, vcount;

	always @(posedge clk) begin
		vga_clk = ~vga_clk;
	end

	always @(posedge vga_clk) begin
		if(hcount == 799)
			hcount = 0;
		else
			hcount = hcount + 10'd1;
	end

	always @(posedge vga_clk) begin
		if(hcount == 0)
			i_hs = 0;
		else if(hcount == 96)
			i_hs = 1;
	end

	always @(posedge vga_clk) begin
		if(hcount == 144)
			i_hdisp = 1;
		else if(hcount == 784)
			i_hdisp = 0;
	end

	always @(posedge i_hs) begin
		if(vcount == 520)
			vcount = 0;
		else
			vcount = vcount + 1'd1;
	end

	always @(posedge i_hs) begin
		if(vcount == 10)
			i_vs = 0;
		else if(vcount == 2)
			i_vs = 1;
	end

	always @(posedge i_hs) begin
		if(vcount == 31)
			i_vdisp = 1;
		else if(vcount == 511)
			i_vdisp = 0;
	end

	assign hsync = i_hs;
	assign vsync = i_vs;

	
	assign x = hcount - 10'd144;
	assign y = vcount - 10'd35;
	//	assign read_addr = x + y * 20'd640;
	// assign read_addr = (x / 20'd4) + (y / 20'd4) * 20'd160;
	//assign color = q_sig & ~(x[1:0] == 0 | y[1:0] == 0) ? 3'b001 : 3'b111;
	assign board_x = (x - 95) / 32;
	assign board_y = (y - 15) / 32;
	assign  board_vram_addr = x + y * 14;
	
	assign color = 
	x >= 95 && y >= 15 && x < 545 && y < 465 ? (
		(x - 95) % 32 < 2 || (y - 15) % 32 < 2 ? 12'hccc :
		board_vram_out & 6'b100000 ? 12'hf70 :
		board_vram_out & 6'b000100 ? 12'h70f :
		12'hddd
	) :
	x < 95 ? (x + y):
	x >= 545 ? (x * y):
	12'heee
	;
	assign rgb_out = (i_hdisp & i_vdisp) ? color : 12'h000;
endmodule
