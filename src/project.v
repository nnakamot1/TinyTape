/*
 * Copyright (c) 2024 Nathan Nakamoto
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path
    input  wire       ena,      // always 1 when powered
    input  wire       clk,      // clock
    input  wire       rst_n     // active-low reset
);

  assign uio_out = 8'b0;
  assign uio_oe  = 8'b0;

  reg [7:0] lfsr;
  reg [7:0] shown_value;

  localparam [7:0] DISPLAY_TICKS = 8'd20;
  reg [7:0] tick_count;

  wire feedback = lfsr[7] ^ lfsr[5] ^ lfsr[4] ^ lfsr[3];

  always @(posedge clk) begin
    if (!rst_n) begin

      lfsr        <= 8'hA5;  // non-zero seed
      shown_value <= 8'hA5;
      tick_count  <= 8'd0;
    
    end else begin
      lfsr <= {lfsr[6:0], feedback};

      if (tick_count == DISPLAY_TICKS - 1'b1) begin
        tick_count  <= 8'd0;
        shown_value <= lfsr;
    
      end else begin
        tick_count <= tick_count + 1'b1;
    
      end
    end
  end

  assign uo_out = shown_value;



  wire _unused = &{ena, uio_in, ui_in, 1'b0};

endmodule
