import os
from config import INPUT_CSV, OUTPUT_CSV, LOG_FILE
from utils import read_claims, save_output
from claim_processor import process_claim

def main():
    # Clear log file
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    claims = read_claims(INPUT_CSV)
    results = []
    for row in claims:
        print(f"Processing claim {row.get('claim_id')}...")
        result = process_claim(row)
        results.append(result)

    save_output(results, OUTPUT_CSV)
    print(f"Done. Output saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
