module VGA(clk, rgb_out, hsync, vsync, write_addr, wdata, write_en, reset_vram);
	input clk;
	output [2:0]rgb_out;
	output hsync, vsync;

	// VRAM
	input [19:0]write_addr;
	input wdata, write_en, reset_vram;
	
	reg vga_clk, i_hs, i_vs, i_hdisp, i_vdisp;
	reg rgb_reg;
	reg [9:0]hcount, vcount;
	wire [9:0]x, y;
	wire [9:0]dx, dy;
	wire q_sig;
	wire [2:0]color;
	
	wire [19:0]read_addr;
	RAM2pot	RAM2pot_inst (
		.aclr ( reset_vram ),
		.clock ( clk ),
		.data ( wdata ),
		.rdaddress ( read_addr ),
		.wraddress ( write_addr ),
		.wren ( write_en ),
		.q ( q_sig )
	);
	
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
	
	assign x = hcount - 10'd144;
	assign y = vcount - 10'd35;
	//	assign read_addr = x + y * 20'd640;
	assign read_addr = (x / 20'd4) + (y / 20'd4) * 20'd160;
	assign hsync = i_hs;
	assign vsync = i_vs;
	assign color = q_sig & ~(x[1:0] == 0 | y[1:0] == 0) ? 3'b001 : 3'b111;
	assign rgb_out = (i_hdisp & i_vdisp) ? color : 3'b000;
endmodule
