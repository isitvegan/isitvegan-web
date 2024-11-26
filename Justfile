import-e-numbers:
	(cd scripts/import_e_numbers && uv run import_e_numbers.py)
	cp scripts/import_e_numbers/e_numbers.toml items/imported/
