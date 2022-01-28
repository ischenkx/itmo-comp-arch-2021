module alu(
        srca,
        srcb,
        alucontrol,
        aluresult,
        zero);
  input [31:0] srca, srcb;
  input [2:0] alucontrol;
  output reg [31:0] aluresult;
  output zero;
  assign zero = aluresult == 0 ? 1 : 0;

  always @(*)
    begin
        case(alucontrol)
          // A and B
          3'b000: aluresult = srca & srcb; 
          // A or B
          3'b001: aluresult = srca | srcb;
          // A + B
          3'b010: aluresult = srca + srcb;
          // not used
          3'b011: aluresult = 8'b00000000;
          // A and not B
          3'b100: aluresult = srca & (~srcb);
          // A or not B
          3'b101: aluresult = srca | (~srcb);
          // A - B
          3'b110: aluresult = srca + (~srcb + 1);
          // SLT
          3'b111: aluresult = srca[31] != srcb[31] ? (srca[31] > srcb[31] ? 1 : 0) : (srca < srcb ? 1 : 0);
        endcase
    end
endmodule
