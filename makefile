# Makefile for code formatting using Black

#   make format-all
format-all:
	@echo "Formatting all source files..."
	@black .
	@echo "Formatting complete."

#   make check-formatting-all
check-formatting-all:
	@echo "Checking code format..."
	@black --check.
	@echo "Format check complete."
#   make get-formatting-status-all
get-formatting-status-all:
	@echo "Getting formatting status..."
	@black --diff --color .
	@echo "Formatting status complete."

#   make format-file(el) el=<file_path>
format-file(el):
	@echo "Formatting${el}..."
	@black ${el}
	@echo "Formatting ${el} complete."

#   make check-formatting-file(el) el=<file_path>
check-formatting-file(el):
	@echo "Checking ${el} formatting..."
	@black --check --color ${el}
	@echo "Checking ${el} formatting complete."

#   make get-formatting-status-file(el) el=<file_path>	
get-formatting-status-file(el):
	@echo "Getting ${el} formatting status..."
	@black --diff --color ${el}
	@echo "Getting ${el} formatting status complete."

