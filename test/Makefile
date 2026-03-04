# Makefile
# See https://docs.cocotb.org/en/stable/quickstart.html for more info

# defaults
SIM ?= icarus
FST ?= -fst # Use more efficient FST format
TOPLEVEL_LANG ?= verilog
PYTHON ?= python3
SRC_DIR = $(PWD)/../src
PROJECT_SOURCES = project.v

ifneq ($(GATES),yes)

# RTL simulation:
SIM_BUILD				= sim_build/rtl
VERILOG_SOURCES += $(addprefix $(SRC_DIR)/,$(PROJECT_SOURCES))

else

# Gate level simulation:
SIM_BUILD				= sim_build/gl
COMPILE_ARGS    += -DGL_TEST
COMPILE_ARGS    += -DFUNCTIONAL
COMPILE_ARGS    += -DUSE_POWER_PINS
COMPILE_ARGS    += -DSIM
COMPILE_ARGS    += -DUNIT_DELAY=\#1
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v

# this gets copied in by the GDS action workflow
VERILOG_SOURCES += $(PWD)/gate_level_netlist.v

endif

# Allow sharing configuration between design and testbench via `include`:
COMPILE_ARGS 		+= -I$(SRC_DIR)

# Include the testbench sources:
VERILOG_SOURCES += $(PWD)/tb.v
TOPLEVEL = tb

# Cocotb 2.x test module list.
COCOTB_TEST_MODULES = test

# Cocotb 1.x ships `cocotb-config`; cocotb 2.x uses `python -m cocotb_tools.config`.
COCOTB_CONFIG_MAKEFILES := $(shell cocotb-config --makefiles 2>/dev/null)
COCOTB_MAKEFILES_DIR := $(COCOTB_CONFIG_MAKEFILES)
ifeq ($(strip $(COCOTB_MAKEFILES_DIR)),)
COCOTB_MAKEFILES_DIR := $(shell $(PYTHON) -m cocotb_tools.config --makefiles 2>/dev/null)
endif

# Older cocotb makefiles consume MODULE instead of COCOTB_TEST_MODULES.
ifneq ($(strip $(COCOTB_CONFIG_MAKEFILES)),)
MODULE ?= $(COCOTB_TEST_MODULES)
endif

ifeq ($(strip $(COCOTB_MAKEFILES_DIR)),)
$(error Could not find cocotb makefiles. Install dependencies with `$(PYTHON) -m pip install -r requirements.txt`)
endif

# include cocotb's make rules to take care of the simulator setup
include $(COCOTB_MAKEFILES_DIR)/Makefile.sim
