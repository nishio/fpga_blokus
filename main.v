module main(switch, dip, gpio, clk, led, hsync, vsync, rgb);
	input [2:0]switch;
	input [9:0]dip;
	input [7:0]gpio;
	input clk;

	output [9:0]led;
	output hsync, vsync;
	output [11:0] rgb;
	
	//assign led = dip;
	assign led[7:0] = gpio[7:0];
	//VGA vga_inst(clk, hsync, vsync, rgb);
endmodule