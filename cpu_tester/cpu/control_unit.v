module control_unit(
        opcode, 
        funct, 
        memtoreg, 
        memwrite, 
        branch,
        alusrc, 
        regdst, 
        regwrite, 
        alucontrol);
  input [5:0] opcode, funct;
  output reg memtoreg, 
    memwrite,
    branch,
    alusrc,
    regdst,
    regwrite;
  output reg [2:0] alucontrol;
  always @(*)
    begin
      case(opcode)
          // addi (add immediate)
          6'b001000: begin
            regdst = 0;
            regwrite = 1;
            alusrc = 1;
            // addition
            alucontrol = 3'b010;
            memwrite = 0;
            memtoreg = 0;
            branch = 0;
          end
          // lw (load word)
          6'b100011: begin
            regdst = 0;
            regwrite = 1;
            alusrc = 1;
            // addition
            alucontrol = 3'b010;
            memwrite = 0;
            memtoreg = 1;
            branch = 0;
          end
          // sw (store word)
          6'b101011: begin
            regdst = 0;
            regwrite = 0;
            alusrc = 1;
            // addition
            alucontrol = 3'b010;
            memwrite = 1;
            memtoreg = 0;
            branch = 0;
          end
          // beq (branch on equal)
          6'b000100: begin
            regdst = 0;
            regwrite = 0;
            alusrc = 0;
            // subtraction
            alucontrol = 3'b110;
            memwrite = 0;
            memtoreg = 0;
            branch = 1;
          end
          // arithmetic (R-type)
          6'b000000: begin
            regdst = 1;
            regwrite = 1;
            alusrc = 0;
            // subtraction
            memwrite = 0;
            memtoreg = 0;
            branch = 0;
            begin
              case (funct)
                // add
                6'b100000: alucontrol = 3'b010;
                // sub
                6'b100010: alucontrol = 3'b110;
                // and
                6'b100100: alucontrol = 3'b000;
                // or
                6'b100101: alucontrol = 3'b001;
                // slt
                6'b101010: alucontrol = 3'b111;
              endcase
            end
          end
        endcase
    end
endmodule
