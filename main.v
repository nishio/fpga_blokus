module main(dip, led);
	input [9:0]dip;
	output [9:0]led;
	
	assign led = dip;
	
endmodule