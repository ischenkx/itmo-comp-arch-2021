module data_memory(a, we, clk, wd, rd);
  input we, clk;
  input [31:0] a;
  input [31:0] wd;
  output [31:0] rd;
  // memory
  reg [31:0] mem_[0:9];
  assign rd = mem_[a >> 2];

  integer i;
  initial begin
    for (i = 0; i < $size(mem_); i = i + 1) begin
      mem_[i] = 32'b0;
    end
  end

  always @(posedge clk)
	begin
		if (we == 1)
      begin
        mem_[a >> 2] = wd;
      end
	end

  integer j;
endmodule

module instruction_memory(a, rd);
  // address
  input [31:0] a;
  // output (the cell where ram[address] is put)
  output [31:0] rd;

  // Note that at this point our programs cannot be larger then 64 subsequent commands.
  // Increase constant below if larger programs are going to be executed.
  reg [31:0] ram[0:1500];
  // address / 4
  assign rd = ram[a >> 2];
  initial begin
    $readmemb("instructions.dat", ram);
  end
endmodule

