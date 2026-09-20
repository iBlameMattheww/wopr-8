module register_file (
    input logic       clk,
    input logic       reset,
    input logic [2:0] rd_address,
    input logic [2:0] rs_address,
    input logic       write_enable,
    input logic [2:0] write_address,
    input logic [7:0] write_data,

    output logic [7:0] rd_data,
    output logic [7:0] rs_data
);


  logic [7:0] regs[0:7];

  //  no waiting for a clk, register reads are combinational 
  assign rd_data = regs[rd_address];
  assign rs_data = regs[rs_address];


  always_ff @(posedge clk) begin : blockName
    if (reset) begin
      for (int i = 0; i < 8; i++) begin
        regs[i] <= 8'd0;
      end

    end else if (write_enable) begin
      regs[write_address] <= write_data;
    end
  end


endmodule
