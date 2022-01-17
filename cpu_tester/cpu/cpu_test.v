`include "mips_cpu.v"
`include "memory.v"
`include "register_file.v"

module cpu_test();

  reg clk;
  wire [31:0] instruction_memory_a, instruction_memory_rd;
  initial begin
      clk = 0;
      $readmemb(`SOURCE_FILE, cpu_instruction_memory.`INSTR_ARR);
      forever
        #1 clk = ~clk;
  end

  integer _iter;
  always @(negedge clk) begin
        if (instruction_memory_rd == 32'b0) begin
            $display("MEMORY_DUMP_BEGIN");
            for (_iter = 0; _iter < $size(cpu_data_memory.`MEM_ARR); _iter = _iter + 1) begin
              $display("%d %b", _iter, cpu_data_memory.`MEM_ARR[_iter]);
            end
            $display("MEMORY_DUMP_END");
            $display("REG_DUMP_BEGIN");
            for (_iter = 0; _iter < $size(cpu_register.`REG_ARR); _iter = _iter + 1) begin
              $display("%d %b", _iter, cpu_register.`REG_ARR[_iter]);
            end
            $display("REG_DUMP_END");
            $display("FINISH");
            $finish();
        end;
   end


  instruction_memory cpu_instruction_memory(.a(instruction_memory_a), .rd(instruction_memory_rd));

  wire data_memory_we;
  wire [31:0] data_memory_a, data_memory_rd, data_memory_wd;

  data_memory cpu_data_memory(.a(data_memory_a), 
      .we(data_memory_we),
      .clk(clk),
      .wd(data_memory_wd),
      .rd(data_memory_rd)
    );

  wire register_we3;
  wire [4:0] register_a1, register_a2, register_a3;
  wire [31:0] register_rd1, register_rd2, register_wd3;

  register_file cpu_register(.clk(clk),
                             .we3(register_we3),
                             .a1(register_a1),
                             .a2(register_a2),
                             .a3(register_a3),
                             .wd3(register_wd3),
                             .rd1(register_rd1),
                             .rd2(register_rd2));

  mips_cpu cpu(.clk(clk),
               .instruction_memory_a(instruction_memory_a),
               .instruction_memory_rd(instruction_memory_rd),
               .data_memory_a(data_memory_a),
               .data_memory_rd(data_memory_rd),
               .data_memory_we(data_memory_we),
               .data_memory_wd(data_memory_wd),
               .register_a1(register_a1),
               .register_a2(register_a2),
               .register_a3(register_a3),
               .register_we3(register_we3),
               .register_wd3(register_wd3),
               .register_rd1(register_rd1),
               .register_rd2(register_rd2));
endmodule
