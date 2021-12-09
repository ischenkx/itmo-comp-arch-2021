module control_unit(opcode, funct, memtoreg, memwrite, branch, alusrc, regdst, regwrite, alucontrol);
  input [5:0] opcode, funct;
  output memtoreg, memwrite, branch, alusrc, regdst, regwrite;
  output [2:0] alucontrol;

  // TODO: implementation
endmodule
