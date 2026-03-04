# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start timed LFSR test")
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    display_ticks = 20
    start_value = int(dut.uo_out.value) & 0xFF
    dut._log.info(f"Initial shown value: 0x{start_value:02X}")

    # Output should stay stable between timer events.
    await ClockCycles(dut.clk, display_ticks - 1)
    assert (int(dut.uo_out.value) & 0xFF) == start_value, "Output changed too early"

    # At timer event, shown value should update.
    await ClockCycles(dut.clk, 1)
    first_update = int(dut.uo_out.value) & 0xFF
    assert first_update != start_value, "Output did not update on timer boundary"

    seen = [first_update]
    for _ in range(7):
        stable = seen[-1]
        await ClockCycles(dut.clk, display_ticks - 1)
        assert (int(dut.uo_out.value) & 0xFF) == stable, "Output changed between timer ticks"
        await ClockCycles(dut.clk, 1)
        seen.append(int(dut.uo_out.value) & 0xFF)

    assert all(v != 0 for v in seen), "LFSR sequence should never hit zero"
    assert len(set(seen)) >= 4, f"Sequence not varying enough: {seen}"
    dut._log.info(f"Timed LFSR values: {[hex(v) for v in seen]}")
