.PHONY: run install format lint test clean

# Cài dependency
install:
	poetry install

# Chạy game
run:
	poetry run python src/main.py

# Format code (dùng Black)
format:
	poetry run black src

# Lint code (tuỳ chọn nếu có flake8/pylint)
lint:
	poetry run flake8 src

# Chạy test (nếu có test/)
test:
	poetry run pytest -q

# Dọn file rác
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
