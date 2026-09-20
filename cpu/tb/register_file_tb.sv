`timescale 1ns / 1ps


module register_file_tb;


  logic clk;
  logic reset;

  logic [2:0] rd_address;
  logic [2:0] rs_address;

  logic write_enable;
  logic [2:0] write_address;
  logic [7:0] write_data;

  logic [7:0] rd_data;
  logic [7:0] rs_data;

  register_file dut (
      .clk  (clk),
      .reset(reset),

      .rd_address(rd_address),
      .rs_address(rs_address),

      .write_enable (write_enable),
      .write_address(write_address),
      .write_data   (write_data),

      .rd_data(rd_data),
      .rs_data(rs_data)
  );

  initial clk = 1'b0;
  always #5 clk = ~clk;


  task write_to_register(input logic [3:0] register_address, input logic [7:0] data);
    begin
      write_enable = 1'b1;
      write_address = register_address;
      write_data = data;

      #10;
      write_enable = 1'b0;
    end
  endtask


  task get_register_data(input logic [2:0] register_address, output logic [7:0] data);
    begin
      rs_address = register_address;
      #1  // for propogation delay... read path is combinational

      data = rs_data;
    end
  endtask


  task check_register_data(input logic [2:0] register_address, input logic [7:0] expected_data);
    logic [7:0] actual_register_data;

    begin
      get_register_data(register_address, actual_register_data);

      if (actual_register_data !== expected_data) begin
        $error("Register data mismatch: expected 0x%02h, actual 0x%02h", expected_data,
               actual_register_data);
      end else begin
        $display("PASS: expected 0x%02h, actual 0x%02h", expected_data, actual_register_data);
      end
    end
  endtask


  initial begin
    reset = 1'b1;
    write_enable = 1'b0;
    write_address = 3'd0;
    write_data = 8'd0;
    rd_address = 3'd0;
    rs_address = 3'd0;

    #20;
    reset = 1'b0;

    #100;
    write_to_register(3'd3, 8'h42);
    check_register_data(3'd3, 8'h42);

    write_to_register(3'd5, 8'hA7);
    check_register_data(3'd5, 8'hA7);

    #100;
    rd_address = 3'd3;
    rs_address = 3'd5;
    #1

    if (rd_data !== 8'h42 || rs_data !== 8'hA7) $error("Dual-read test failed!");
    else $display("PASS: dual-read test");

    #20000;
    $finish;
  end


  initial begin
    $dumpfile("build/register_file_tb.vcd");
    $dumpvars(0, register_file_tb);
  end


endmodule
