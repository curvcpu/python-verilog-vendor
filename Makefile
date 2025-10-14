PYTHON ?= python3
VENV_DIR := .test-venv

THIS_PKG := utils

.PHONY: test
test:
	@echo "Creating temporary test venv..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "Installing package with test dependencies..."
	@$(VENV_DIR)/bin/pip install -q --upgrade pip
	@$(VENV_DIR)/bin/pip install -q -e ".[test]"
	@echo "Running tests..."
	@if $(VENV_DIR)/bin/pytest; then \
		echo "✅ $(THIS_PKG): all tests passed"; \
		[ -d "$(VENV_DIR)" ] && rm -rf $(VENV_DIR) && echo "(cleaned up test venv dir '$(VENV_DIR)')" || true; \
	else \
		echo "❌ $(THIS_PKG): tests failed. Venv preserved at $(VENV_DIR) for debugging."; \
		echo "To run tests again in the same venv: $(VENV_DIR)/bin/pytest"; \
		echo "To delete the venv and start over: make clean"; \
		exit 1; \
	fi

.PHONY: clean
clean:
	@if [ -d "$(VENV_DIR)" ]; then \
		[ -d "$(VENV_DIR)" ] && rm -rf $(VENV_DIR) || true; \
	fi

