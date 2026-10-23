module sp (
    input logic       clk,
    input logic       reset,
    input logic [1:0] sp_op,

    output logic [7:0] sp
);


  localparam logic [1:0] SP_HOLD = 2'd0;
  localparam logic [1:0] SP_INCREMENT = 2'd1;
  localparam logic [1:0] SP_DECREMENT = 2'd2;


  always_ff @(posedge clk) begin : StackPointer
    if (reset) begin
      sp <= 8'hDF;
    end else begin
      case (sp_op)
        SP_INCREMENT: begin  // Pop (increasing SP address)
          sp <= sp + 8'h01;
        end

        SP_DECREMENT: begin  // PUSH (decreasing SP address since it grows downwards)
          sp <= sp - 8'h01;
        end

        default: begin
          // do nada
        end
      endcase
    end
  end


endmodule
