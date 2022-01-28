`include "alu.v"
`include "control_unit.v"
`include "util.v"

module mips_cpu(
        // clock
        clk,
        // (instruction memory unit) requested data address
        instruction_memory_a,
        // (instruction memory unit) retrieved data
        instruction_memory_rd,
        // (data memory unit) requested data address
        data_memory_a,
        // (data memory unit) retrieved data address
        data_memory_rd,
        // (data memory unit) write-enable flag
        data_memory_we,
        // (data memory unit) data to be written to `data_memory_a`
        // if `data_memory_we` == 1
        data_memory_wd,
        // (register file) requested (read) register address (1)
        register_a1,
        // (register file) requested (read) register address (2)
        register_a2,
        // (register file) requested (write) register address (3)
        register_a3,
        // (register file) write-enable flag
        register_we3,
        // (register file) data to be written to the register 
        // with address = `register_a3`
        // if `register_we3` == 1
        register_wd3,
        // (register file) retrieved data (1)
        register_rd1,
        // (register file) retrieved data (2)
        register_rd2
      );

  input clk;
  output data_memory_we;
  output [31:0] instruction_memory_a, data_memory_a, data_memory_wd;
  inout [31:0] instruction_memory_rd, data_memory_rd;
  output register_we3;
  output [4:0] register_a1, register_a2, register_a3;
  output [31:0] register_wd3;
  inout [31:0] register_rd1, register_rd2;
  
  // alu
  wire [2:0] alu_control;
  wire [31:0] alu_srca;
  wire [31:0] alu_srcb;
  wire [31:0] alu_result;
  wire alu_carry_output;

  alu alu_(
    .srca(alu_srca),
    .srcb(alu_srcb),
    .alucontrol(alu_control),
    .aluresult(alu_result),
    .zero(alu_carry_output)
  );

  // instructions decoding (the control unit and the register file)
  wire memtoreg;
  wire memwrite;
  wire branch;
  wire alusrc;
  wire regdst;
  wire regwrite;
  wire [5:0] opcode, funct;
  wire [15:0] imm;
  wire [31:0] extended_imm, shifted_imm;
  wire pc_src = branch & alu_carry_output;
  assign alu_srca = register_rd1;
  assign opcode = instruction_memory_rd[31:26];
  assign funct = instruction_memory_rd[5:0];
  assign register_a1 = instruction_memory_rd[25:21];
  assign register_a2 = instruction_memory_rd[20:16];
  assign register_we3 = regwrite;
  assign imm = instruction_memory_rd[15:0];

  control_unit control_unit_(
    .opcode(opcode),
    .funct(funct),
    .memtoreg(memtoreg),
    .memwrite(memwrite),
    .branch(branch),
    .alusrc(alusrc),
    .regdst(regdst),
    .regwrite(regwrite),
    .alucontrol(alu_control)
  );

  mux2_5 write_register_setter(
    .d0(instruction_memory_rd[20:16]),
    .d1(instruction_memory_rd[15:11]),
    .a(regdst),
    .out(register_a3)
  );

  sign_extend imm_extension_unit(
    .in(imm),
    .out(extended_imm)
  );

  shl_2 imm_shifter(
    .in(extended_imm),
    .out(shifted_imm)
  );

  mux2_32 srcb_setter(
    .d0(register_rd2),
    .d1(extended_imm),
    .a(alusrc),
    .out(alu_srcb)
  );

  // Program Counter
  // must be updated in each cycle: PC = PC + 4
  wire [31:0] pc_input;

  // next instruction address
  wire [31:0] pc_incrementor_output;
  wire [31:0] pc_brancher_output;

  d_flop pc(
    .d(pc_input),
    .clk(clk),
    .q(instruction_memory_a)
  );

  adder pc_incrementor(
    .a(instruction_memory_a),
    // 4
    .b(32'b100),
    .out(pc_incrementor_output)
  );

  adder pc_brancher(
    .a(shifted_imm),
    .b(pc_incrementor_output),
    .out(pc_brancher_output)
  );

  mux2_32 pc_updater(
    .d0(pc_incrementor_output),
    .d1(pc_brancher_output),
    .a(pc_src),
    .out(pc_input)
  );

  // data memory unit
  assign data_memory_a = alu_result;
  assign data_memory_wd = register_rd2;
  assign data_memory_we = memwrite;

  mux2_32 dm_proxy(
    .d0(alu_result),
    .d1(data_memory_rd),
    .a(memtoreg),
    .out(register_wd3)
  );

  // // DEBUG
  // integer cycle_counter = 0;
  // always @ (posedge clk) begin
  //   cycle_counter = cycle_counter + 1;
  //   if (instruction_memory_rd[0] == 0 || instruction_memory_rd[0] == 1) begin
  //     $display("___________",
  //       "\n\tcycle_count=%d", cycle_counter,
  //       "\n\tinc_out=%b", pc_incrementor_output,
  //       "\n\tbrancher_out=%b", pc_brancher_output,
  //       "\n\tpc_input=%b", pc_input,
  //       "\n\tinstruction=%b", instruction_memory_rd,
  //       "\n\treg_a1=%b (%d)", register_rd1, register_rd1, 
  //       "\n\treg_a2=%b (%d)", register_rd2, register_rd2, 
  //       "\n\treg_a3=%b (%d)", register_a3, register_a3,
  //       "\n\treg_wd3=%b (%d)", register_wd3, register_wd3
    
  //       );
  //     // #100;
  //   end
  //   end
  //   else if (instruction_memory_rd[0] == 1) begin
  //     $display("%b", instruction_memory_rd);
  //   end
  // end
endmodule
