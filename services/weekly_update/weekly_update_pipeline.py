# Description: This script is the main pipeline for the weekly update of the database.
import logging
import os
from datetime import datetime

# Files
from download_weekly_arxiv_data import download_arxiv_data
from get_past_week_data_from_json_file import filter_papers_past_week
from semantic_filter_data import semantic_filtering
from topic_assignment import assign_topics
from update_database import insert_papers_into_weaviate

import download_weekly_arxiv_data
import get_past_week_data_from_json_file
import define_llm_subspace
import topic_assignment

# Path
from config import WEEKLY_DATA_PATH
from config import SENTENCE_TRANSFOMERS_PATH
from config import ARXIV_INPUT_FILE_PATH



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    today = datetime.now()

    logging.info("Starting weekly update pipeline...")
    
    # Step 1: Download weekly data
    logging.info("Downloading weekly arXiv data...")
    download_weekly_arxiv_data.download_arxiv_data(WEEKLY_DATA_PATH)
    
    # Step 2: Load data from JSON
    logging.info("Loading data from JSON...")
    # Generate dynamic output filename based on the current date
    output_filename = f"filtered_papers_{today.strftime('%Y-%m-%d')}.jsonl"
    output_file = os.path.join(WEEKLY_DATA_PATH, output_filename)
    print(output_file)
    # Run LLM-subspace capturing
    get_past_week_data_from_json_file.filter_papers_past_week(ARXIV_INPUT_FILE_PATH, output_file)

    
    # Step 3: Define LLM subspace
    logging.info("Extracting entities and defining LLM subspace...")
    # Run the function to save filtered papers
    input_filename = f"filtered_papers_{today.strftime('%Y-%m-%d')}.jsonl"
    input_file = os.path.join(WEEKLY_DATA_PATH, input_filename)
    output_filename = f"filtered_papers_{today.strftime('%Y-%m-%d')}_with_entities.jsonl" 
    output_file = os.path.join(WEEKLY_DATA_PATH, output_filename)
    output_filename_only_llm = f"filtered_papers_{today.strftime('%Y-%m-%d')}_with_entities.jsonl" 
    output_file_only_llm = os.path.join(WEEKLY_DATA_PATH, output_filename)
    # Get the number of rows. This paramater in theory could be later removed. 
    num_rows = sum(1 for _ in open(input_file, "r", encoding="utf-8"))
    # Extract entities with GLINER
    define_llm_subspace.extract_entities_from_abstracts(input_file, output_file, max_rows=num_rows)
    # Filter out only LLM-captured
    define_llm_subspace.save_papers_with_entities(output_file, output_file_only_llm)

    
    # # # Step 4: Apply semantic filtering on the entities. For instance: GPT, should contain GPT related entities.
    logging.info("Applying semantic filtering...")
    output_filename_only_llm = f"filtered_papers_{today.strftime('%Y-%m-%d')}_with_entities.jsonl" 
    extracted_entities_file = os.path.join(WEEKLY_DATA_PATH, output_filename_only_llm)
    # Define base path dynamically
    base_output_folder = os.path.join(WEEKLY_DATA_PATH, "output")
    # Run the process
    semantic_filtering(
        extracted_entities_file=extracted_entities_file,
        base_output_folder=base_output_folder,
        model_dir=SENTENCE_TRANSFOMERS_PATH,
        threshold=0.5
    )

    # # # Step 5: Assign topics
    logging.info("Assigning topics...")
    topic_assignment.assign_topics()


    # # Step 6: Update database
    base_input_folder = os.path.join(WEEKLY_DATA_PATH, "output")
    input_filename = f"{today.strftime('%Y-%m-%d')}_merged_with_topics.jsonl" 
    updated_data_path = os.path.join(base_input_folder, input_filename)
    print(updated_data_path)
    insert_papers_into_weaviate(updated_data_path)
    logging.info("Updating database with the weekly data...")
    


    logging.info("Weekly update pipeline completed successfully.")

if __name__ == "__main__":
    main()