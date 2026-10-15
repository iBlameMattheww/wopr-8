module pc (
    input logic clk,
    input logic reset,

    input logic [ 1:0] pc_op,
    input logic [10:0] target,

    output logic [10:0] pc
);


  localparam logic [1:0] PC_HOLD      = 2'd0;
  localparam logic [1:0] PC_INCREMENT = 2'd1;
  localparam logic [1:0] PC_LOAD      = 2'd2;


  always_ff @(posedge clk) begin : ProgramCounter
    if (reset) begin
      pc <= 11'd0;
    end else begin
      case (pc_op)
        PC_INCREMENT: begin
          pc <= pc + 11'd1;
        end

        PC_LOAD: begin
          pc <= target;
        end

        default: begin
          // do nada
        end
      endcase
    end
  end


endmodule
