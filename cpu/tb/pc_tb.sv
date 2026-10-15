`timescale 1ns / 1ps

module pc_tb;

  logic clk;
  logic reset;

  logic [1:0] pc_op;
  logic [10:0] target;

  logic [10:0] pc;


  pc dut (
      .clk  (clk),
      .reset(reset),

      .pc_op (pc_op),
      .target(target),

      .pc(pc)
  );


  localparam logic [1:0] PC_HOLD      = 2'd0;
  localparam logic [1:0] PC_INCREMENT = 2'd1;
  localparam logic [1:0] PC_LOAD      = 2'd2;


  initial clk = 1'b0;
  always #5 clk = ~clk;

  task reset_pc();
    begin
      reset = 1;
      @(posedge clk);
      #1;
      reset = 0;
    end
  endtask


  task write_to_pc(input logic [1:0] operation, input logic [10:0] target_pc);
    begin
      pc_op  = operation;
      target = target_pc;
      @(posedge clk);

      #1;
      pc_op = PC_HOLD;
    end
  endtask


  task check_pc_result(input logic [10:0] expected);
    begin
      if (pc !== expected) begin
        $error("Result mismatch: expected pc 0x%02h, actual pc 0x%02h", expected, pc);
      end else begin
        $display("PASS: expected pc 0x%02h, actual pc 0x%02h", expected, pc);
      end
    end
  endtask


  initial begin
    pc_op  = 2'd0;
    target = 11'd0;
    reset_pc();
    check_pc_result(11'd0);

    #100;
    write_to_pc(PC_INCREMENT, 11'd3);  // putting some nonsense on target
    check_pc_result(11'd1);

    #100;
    write_to_pc(PC_HOLD, 11'd7);
    check_pc_result(11'd1);

    #100;
    write_to_pc(PC_LOAD, 11'd255);
    check_pc_result(11'd255);

    #100;
    write_to_pc(PC_INCREMENT, 11'd99);
    check_pc_result(11'd256);

    #100;
    write_to_pc(PC_HOLD, 11'd0);
    check_pc_result(11'd256);

    #100 write_to_pc(PC_LOAD, 11'd2047);
    check_pc_result(11'd2047);

    #100 write_to_pc(PC_INCREMENT, 11'd300);
    check_pc_result(11'd0);

    #20000;
    $finish;
  end


  initial begin
    $dumpfile("build/pc_tb.vcd");
    $dumpvars(0, pc_tb);
  end


endmodule
