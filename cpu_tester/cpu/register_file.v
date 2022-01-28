module register_file(clk, we3, a1, a2, a3, wd3, rd1, rd2);
  	// clk, write flag (write enable)
	input clk, we3;
	// two read registers, one write register
	input [4:0] a1, a2, a3;
	// write data
	input [31:0] wd3;
	// read data
	output [31:0] rd1, rd2;

	reg [31:0] registers [31:0];
	
	integer i;
	initial begin
		for (i=0; i<32; i=i+1) begin
			registers[i] <= 32'd0;
		end
	end


	assign rd1 = registers[a1];
	assign rd2 = registers[a2];
	
	always @(posedge clk)
	begin
		if (we3 == 1)
		begin
			registers[a3] = wd3;
		end
	end
endmodule
