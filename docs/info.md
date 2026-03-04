## How it works

This design is an 8-bit pseudo-random value generator based on a linear feedback shift register (LFSR).

- Core state:
  - `lfsr` is an 8-bit register updated every clock cycle.
  - Feedback polynomial taps are `x^8 + x^6 + x^5 + x^4 + 1` (`lfsr[7] ^ lfsr[5] ^ lfsr[4] ^ lfsr[3]`).
- Display behavior:
  - `shown_value` is the value presented on `uo_out[7:0]`.
  - A timer counter (`tick_count`) updates `shown_value` once every `DISPLAY_TICKS = 20` clocks.
  - Between timer boundaries, `uo_out` remains constant.
- Reset behavior:
  - Active-low reset (`rst_n`) seeds both `lfsr` and `shown_value` to `8'hA5`.
- Pin usage:
  - `uo_out[7:0]`: sampled pseudo-random output.
  - `ui_in[7:0]`, `uio_in[7:0]`, and `ena` are unused by logic and tied into an `_unused` sink.
  - `uio_out[7:0]` and `uio_oe[7:0]` are driven to zero.

In short, the circuit continuously runs an LFSR but only exposes a sampled value at fixed time intervals, creating a stable output window and periodic updates.

## How to test

The project uses a cocotb-based testbench (`test/test.py`) with a Verilog wrapper (`test/tb.v`).

- Testbench setup:
  - Generates a 100 MHz clock.
  - Drives `ena=1`, `ui_in=0`, and `uio_in=0` for idle.
  - Applies reset for 5 cycles, then releases reset later after an extra cycle.
- Properties Check of first output.
  - Output stability: after the reset, `uo_out` must and will remain unchanged for `DISPLAY_TICKS - 1` cycles.
  - Timer-boundary on the next cycle (the 20th), `uo_out` must change.
  - across multiple windows, output stays constant within each window and updates only at boundaries.
  - LFSR:
    - sampled outputs are never zero.
    - Sequence shows (`len(set(seen)) >= 4` over the sampled updates).

Why this is sufficient:
- The DUT has one main critical logic "update every 20 cycles, otherwise hold." We can see that the test explicitly validates this timing rule multiple times.
- The DUT's data source is an LFSR. The test verifies essential LFSR non-zero sequence and variation over time.
- Reset and initialization behavior are exercised at the start of simulation.

This covers the functional contract of the design at its external interface (`uo_out` timing and value progression).

## GenAI Usage

GenAI tools were used as an assitant to help draft the compile and interfacing errors, suggest verification checks and test organization, and helped structure some of the writing.



## External Hardware

No external hardware is required. The design is testable in simulation.
