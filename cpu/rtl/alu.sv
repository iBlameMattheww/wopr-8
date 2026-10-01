module alu (
    input logic [7:0] operand_a,
    input logic [7:0] operand_b,

    input logic [3:0] alu_op,

    input logic [2:0] shamt,
    input logic dir,

    output logic [7:0] result,
    output logic Z,
    output logic C
);


  localparam logic [3:0] ALU_ADD   = 4'd0;
  localparam logic [3:0] ALU_SUB   = 4'd1;
  localparam logic [3:0] ALU_AND   = 4'd2;
  localparam logic [3:0] ALU_OR    = 4'd3;
  localparam logic [3:0] ALU_XOR   = 4'd4;
  localparam logic [3:0] ALU_NOT   = 4'd5;
  localparam logic [3:0] ALU_SHIFT = 4'd6;

  logic [9:0] temp;

  always_comb begin : ALUCombinational
    result = 8'd0;
    Z = 1'b0;
    C = 1'b0;
    temp = 10'd0;

    case (alu_op)
      ALU_ADD: begin
        temp = {1'b0, operand_a, 1'b0} + {1'b0, operand_b, 1'b0};
        C = temp[9];
        result = temp[8:1];
      end

      ALU_SUB: begin
        C = (operand_a < operand_b);
        result = operand_a - operand_b;
      end

      ALU_AND: begin
        result = operand_a & operand_b;
      end

      ALU_OR: begin
        result = operand_a | operand_b;
      end

      ALU_XOR: begin
        result = operand_a ^ operand_b;
      end

      ALU_NOT: begin
        result = ~operand_b;
      end

      ALU_SHIFT: begin
        if (dir) begin
          temp = {1'b0, operand_a, 1'b0} >> operand_b;
          C = temp[0];
          result = temp[8:1];
        end else begin
          temp = {1'b0, operand_a, 1'b0} << operand_b;
          C = temp[9];
          result = temp[8:1];
        end
      end

      default: begin
        result = 8'd0;
      end
    endcase

    if (shamt) begin
      if (dir) begin
        temp = {1'b0, result, 1'b0} >> shamt;
        C = temp[0];
        result = temp[8:1];
      end else begin
        temp = {1'b0, result, 1'b0} << shamt;
        C = temp[9];
        result = temp[8:1];
      end
    end

    Z = (result == 8'd0);
  end

endmodule
