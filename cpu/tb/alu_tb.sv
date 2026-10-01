`timescale 1ns / 1ps

module alu_tb;

  logic [7:0] rd;
  logic [7:0] rs;

  logic [3:0] alu_op;

  logic [2:0] shamt;
  logic dir;

  logic [7:0] result;
  logic Z;
  logic C;

  alu dut (
      .operand_a(rd),
      .operand_b(rs),

      .alu_op(alu_op),

      .shamt(shamt),
      .dir  (dir),

      .result(result),
      .Z     (Z),
      .C     (C)
  );

  localparam logic [3:0] ALU_ADD   = 4'd0;
  localparam logic [3:0] ALU_SUB   = 4'd1;
  localparam logic [3:0] ALU_AND   = 4'd2;
  localparam logic [3:0] ALU_OR    = 4'd3;
  localparam logic [3:0] ALU_XOR   = 4'd4;
  localparam logic [3:0] ALU_NOT   = 4'd5;
  localparam logic [3:0] ALU_SHIFT = 4'd6;


  task write_to_alu(input logic [3:0] op, input logic [7:0] rd_data, input logic [7:0] rs_data,
                    input logic [2:0] shamt_value, input logic direction);
    begin
      alu_op = op;
      rd = rd_data;
      rs = rs_data;
      shamt = shamt_value;
      dir = direction;
      #1;
    end
  endtask


  task get_alu_result(output logic [7:0] data, output logic zero, output logic carry);
    begin
      data  = result;
      zero  = Z;
      carry = C;
    end
  endtask


  task check_alu_result(input logic [3:0] op, input logic [7:0] rd_data, input logic [7:0] rs_data,
                        input logic [2:0] shamt_value, input logic direction,
                        input logic [7:0] expected, input logic expected_zero,
                        input logic expected_carry);
    logic [7:0] actual;
    logic actual_zero;
    logic actual_carry;

    begin
      write_to_alu(op, rd_data, rs_data, shamt_value, direction);
      get_alu_result(actual, actual_zero, actual_carry);

      if (actual !== expected) begin
        $error("Result mismatch on operation 0x%02h: expected 0x%02h, actual 0x%02h", op, expected,
               actual);
      end

      if (actual_zero !== expected_zero) begin
        $error("Result Z mismatch on operation 0x%02h: expected %b, actual %b", op, expected_zero,
               actual_zero);
      end

      if (actual_carry !== expected_carry) begin
        $error("Result C mismatch on operation 0x%02h: expected %b, actual %b", op, expected_carry,
               actual_carry);
      end

      if ((actual === expected) &&
        (actual_zero === expected_zero) && 
        (actual_carry === expected_carry)) begin
        $display("PASS: operation 0x%02h, expected 0x%02h, actual 0x%02h", op, expected, actual);
      end
    end
  endtask


  initial begin
    check_alu_result(ALU_ADD, 8'd5, 8'd3, 3'd0, 1'b0, 8'd8, 1'b0,
                     1'b0);  // ADD, 5, 3, 0, 0, 8, 0, 0

    check_alu_result(ALU_ADD, 8'hFF, 8'h01, 3'd0, 1'b0, 8'h00, 1'b1,
                     1'b1);  // ADD, 255, 1, 0, 0, 0, 1, 1 

    check_alu_result(ALU_SUB, 8'd8, 8'd5, 3'd0, 1'b0, 8'd3, 1'b0,
                     1'b0);  // SUB, 8, 5, 0, 0, 3, 0, 0 

    check_alu_result(ALU_SUB, 8'd3, 8'd5, 3'd0, 1'b0, 8'hFE, 1'b0,
                     1'b1);  // SUB, 3, 5, 0, 0, 254, 0, 1

    check_alu_result(ALU_SUB, 8'd5, 8'd5, 3'd0, 1'b0, 8'd0, 1'b1,
                     1'b0);  // SUB, 5, 5, 0, 0, 0, 1, 0

    check_alu_result(ALU_AND, 8'hAA, 8'h0F, 3'd0, 1'b0, 8'h0A, 1'b0,
                     1'b0);  // AND, 170, 15, 0, 0, 10, 0, 0

    check_alu_result(ALU_OR, 8'hA0, 8'h0F, 3'd0, 1'b0, 8'hAF, 1'b0,
                     1'b0);  // OR, 160, 15, 0, 0, 175, 0, 0 

    check_alu_result(ALU_XOR, 8'hAA, 8'hFF, 3'd0, 1'b0, 8'h55, 1'b0,
                     1'b0);  // XOR, 170, 255, 0, 0, 85, 0, 0

    check_alu_result(ALU_NOT, 8'h00, 8'hAA, 3'd0, 1'b0, 8'h55, 1'b0,
                     1'b0);  // NOT, 0, 170, 0, 0, 85, 0, 0

    check_alu_result(ALU_XOR, 8'hAA, 8'hAA, 3'd0, 1'b0, 8'h00, 1'b1,
                     1'b0);  // XOR, 170, 170, 0, 0, 0, 1, 0

    // ADD first, then post-shift left by 2:
    // 1 + 1 = 2
    // 2 << 2 = 8
    check_alu_result(ALU_ADD, 8'd1, 8'd1, 3'd2, 1'b0, 8'd8, 1'b0, 1'b0);

    // OR first, then post-shift right by 1:
    // 0x0C | 0x00 = 0x0C
    // 0x0C >> 1 = 0x06
    check_alu_result(ALU_OR, 8'h0C, 8'h00, 3'd1, 1'b1, 8'h06, 1'b0, 1'b0);

    // XOR first:
    // 0x81 ^ 0x00 = 0x81
    // post-shift left by 1:
    // 0x81 << 1 = 0x02
    // bit 7 was shifted out, so C = 1
    check_alu_result(ALU_XOR, 8'h81, 8'h00, 3'd1, 1'b0, 8'h02, 1'b0, 1'b1);

    // SHIFT by Rs first:
    // 0x01 << 2 = 0x04
    // then post-shift by shamt=3:
    // 0x04 << 3 = 0x20
    check_alu_result(ALU_SHIFT, 8'h01, 8'd2, 3'd3, 1'b0, 8'h20, 1'b0, 1'b0);

    $finish;
  end


  initial begin
    $dumpfile("build/alu_tb.vcd");
    $dumpvars(0, alu_tb);
  end


endmodule
