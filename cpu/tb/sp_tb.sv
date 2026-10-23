`timescale 1ns / 1ps


module sp_tb;

  logic clk;
  logic reset;

  logic [1:0] sp_op;

  logic [7:0] sp;


  sp dut (
      .clk  (clk),
      .reset(reset),

      .sp_op(sp_op),

      .sp(sp)
  );


  localparam logic [1:0] SP_HOLD = 2'd0;
  localparam logic [1:0] SP_INCREMENT = 2'd1;
  localparam logic [1:0] SP_DECREMENT = 2'd2;


  initial clk = 1'b0;
  always #5 clk = ~clk;


  task reset_sp();
    begin
      reset = 1;
      @(posedge clk);
      #1;
      reset = 0;
    end
  endtask


  task write_to_sp(input logic [1:0] operation);
    begin
      sp_op = operation;
      @(posedge clk);

      #1;
      sp_op = SP_HOLD;  // change it back to hold so every CC doesn't inc/dec SP 
    end
  endtask


  task check_sp_result(input logic [7:0] expected);
    begin
      if (sp !== expected) begin
        $error("Result mismatch: expected sp 0x%02h, actual sp 0x%02h", expected, sp);
      end else begin
        $display("PASS: expected sp 0x%02h, actual sp 0x%02h", expected, sp);
      end
    end
  endtask


  initial begin
    sp_op = 2'd0;
    reset_sp();
    check_sp_result(8'hDF);

    #100;
    write_to_sp(SP_DECREMENT);
    check_sp_result(8'hDE);

    #100;
    write_to_sp(SP_HOLD);
    check_sp_result(8'hDE);

    #100;
    write_to_sp(SP_INCREMENT);
    check_sp_result(8'hDF);

    #100;
    write_to_sp(SP_DECREMENT);
    write_to_sp(SP_DECREMENT);
    write_to_sp(SP_DECREMENT);
    check_sp_result(8'hDC);

    #100;
    @(negedge clk);
    reset_sp();
    write_to_sp(SP_HOLD);
    @(posedge clk);
    #1;
    check_sp_result(8'hDF);

    #20000;
    $finish;
  end



  initial begin
    $dumpfile("build/sp_tb.vcd");
    $dumpvars(0, sp_tb);
  end


endmodule

