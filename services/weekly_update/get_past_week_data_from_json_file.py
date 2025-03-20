import json
import datetime
import os

# Compute correct date range (past 7 full days)
today = datetime.datetime.utcnow().date()
week_ago = today - datetime.timedelta(days=7)

def parse_arxiv_date(date_str):
    """Convert ArXiv date format 'Mon, 2 Apr 2007 19:18:42 GMT' to datetime.date."""
    return datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z").date()

def filter_papers_past_week(input_file, output_file):
    """Filters papers based on their LAST version update date."""
    with open(input_file, "r", encoding="utf-8") as f, open(output_file, "w", encoding="utf-8") as f_out:
        count = 0  # Track filtered records

        for line in f:  # Read one JSON object per line
            try:
                paper = json.loads(line.strip())  # Convert line to JSON object
                
                # Get the last version's "created" date (latest update date)
                last_version = paper.get("versions", [{}])[-1].get("created", None)
                if not last_version:
                    continue  # Skip if no date found
                
                # Convert date and check if it's within the past 7 days
                paper_date = parse_arxiv_date(last_version)
                if week_ago <= paper_date <= today:
                    f_out.write(json.dumps(paper) + "\n")  # Write to JSONL file
                    count += 1

            except (json.JSONDecodeError, ValueError):
                continue  # Skip malformed JSON lines

    print(f"Filtering complete. {count} papers saved to {output_file} (JSONL format).")

# # Generate dynamic output filename based on the current date
# output_filename = f"filtered_papers_{today.strftime('%Y-%m-%d')}.jsonl"
# output_file = os.path.join(WEEKLY_DATA_PATH, output_filename)
# # Run filtering
# filter_papers_past_week(ARXIV_INPUT_FILE_PATH, output_file)



