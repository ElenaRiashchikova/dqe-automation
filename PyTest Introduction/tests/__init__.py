minversion = 7.0
testpaths = [
    "tests",
    "test"
]
python_files = ["test_*.py", "*_test.py"]
python_classes = "Test*"
python_functions = ["test_*", "check_*"]
addopts = ["--strict-markers", "--tb=short"]
markers = ["integration: marks tests as integration tests",
    "api: marks tests related to API functionality"]
log_level = "INFO"
log_format = "%(asctime)s %(levelname)s %(message)s"
log_date_format = "%Y-%m-%d %H:%M:%S"
console_output_style = "progress"
filterwarnings = "ignore::DeprecationWarning"
norecursedirs =[".git",
    "node_modules",
    "build"]