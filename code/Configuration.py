import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-key-here")
MODEL_NAME = "gpt-4o"  # or "gpt-4-turbo"
DATA_DIR = "../dataset"          # relative to code/ when running
IMAGES_DIR = f"{DATA_DIR}/images/sampleHackerRank"
INPUT_CSV = f"{DATA_DIR}/test.csv"
OUTPUT_CSV = "output.csv"
LOG_FILE = "log.txt"
