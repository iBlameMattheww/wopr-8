GTKWAVE := gtkwave
IVERILOG := iverilog
VVP := vvp

BUILD_FLAGS := -g2012 -o

RTL_DIR := rtl
TB_DIR := tb
BUILD_DIR := build

all: alu register_file pc

register_file: $(BUILD_DIR)/register_file_tb.vvp
	$(VVP) $<

alu: $(BUILD_DIR)/alu_tb.vvp
	$(VVP) $<

pc: $(BUILD_DIR)/pc_tb.vvp
	$(VVP) $<

wave-%: %
	$(GTKWAVE) $(BUILD_DIR)/$*_tb.vcd

$(BUILD_DIR)/%_tb.vvp: $(RTL_DIR)/%.sv $(TB_DIR)/%_tb.sv
	mkdir -p $(BUILD_DIR)
	$(IVERILOG) $(BUILD_FLAGS) $@ $^

clean: 
	rm -rf $(BUILD_DIR)

.PHONY: all clean register_file wave-register_file alu wave-alu pc wave-pc

