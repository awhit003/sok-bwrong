SUITES = movetest walltest1 walltest2 walltest3

.PHONY: all simulator device clean $(SUITES)

all:
	@for suite in $(SUITES); do \
		echo "=== Building $$suite (Device + Simulator) ==="; \
		$(MAKE) -C src/$$suite device || exit 1; \
		$(MAKE) -C src/$$suite simulator || exit 1; \
	done
	@echo "\n=== All suites built successfully! ==="

simulator:
	@for suite in $(SUITES); do \
		echo "=== Building $$suite (Simulator) ==="; \
		$(MAKE) -C src/$$suite simulator || exit 1; \
	done
	@echo "\n=== Simulator packages built! ==="

device:
	@for suite in $(SUITES); do \
		echo "=== Building $$suite (Device) ==="; \
		$(MAKE) -C src/$$suite device || exit 1; \
	done
	@echo "\n=== Device packages built! ==="

clean:
	@for suite in $(SUITES); do \
		echo "=== Cleaning $$suite ==="; \
		$(MAKE) -C src/$$suite clean; \
	done
