SUITES = doodtest8 doodtest10 doodtest16 doodtest20 doodtest40

.PHONY: all simulator device clean $(SUITES)

all:
	@for suite in $(SUITES); do \
		echo "=== Building $$suite (Device + Simulator) ==="; \
		$(MAKE) -C src/$$suite device || exit 1; \
		$(MAKE) -C src/$$suite simulator || exit 1; \
	done
	@echo "\n=== All 5 test suites built successfully! ==="

simulator:
	@for suite in $(SUITES); do \
		echo "=== Building $$suite (Simulator) ==="; \
		$(MAKE) -C src/$$suite simulator || exit 1; \
	done
	@echo "\n=== All 5 simulator packages built! ==="

device:
	@for suite in $(SUITES); do \
		echo "=== Building $$suite (Device) ==="; \
		$(MAKE) -C src/$$suite device || exit 1; \
	done
	@echo "\n=== All 5 device packages built! ==="

clean:
	@for suite in $(SUITES); do \
		echo "=== Cleaning $$suite ==="; \
		$(MAKE) -C src/$$suite clean; \
	done
