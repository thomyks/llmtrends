import os
import json
import pandas as pd
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# Load Path
from config import WEEKLY_DATA_PATH
from config import SENTENCE_TRANSFOMERS_PATH

def load_extracted_entities(extracted_entities_file):
    """
    Loads extracted entities from a JSONL file and organizes them into a dictionary by label.
    
    Args:
        extracted_entities_file (str): Path to the JSONL file containing extracted entities.
    
    Returns:
        dict: A dictionary mapping entity labels to lists of text values.
    """
    label_to_texts = {}
    records = []
    
    with open(extracted_entities_file, "r") as file:
        for line in file:
            record = json.loads(line)
            records.append(record)  # Store each record for later processing
            if "extracted_entities" in record:
                for entity in record["extracted_entities"]:
                    text = entity.get("text", "").strip()
                    label = entity.get("label", "").strip()
                    if text and label:
                        label_to_texts.setdefault(label, []).append(text)
    
    return label_to_texts, records  # Return both extracted entities and full records

def load_model(model_path):
    """
    Loads a SentenceTransformer model from a local path or downloads it from Hugging Face if needed.
    
    If the model_path does not contain a valid config.json, it will try to download the model
    using the name extracted from the path, and save it locally.

    Args:
        model_path (str): Path to the model directory or HuggingFace model name.

    Returns:
        SentenceTransformer: Loaded model.

    Created by Tomáš 🧠
    """
    config_path = os.path.join(model_path, "config.json")

    # If local path does NOT contain config.json → download and save
    if not os.path.isfile(config_path):
        print(f"⚠️ Model not found at {model_path} – downloading from Hugging Face...")

        # Extract model name from path, fallback to default
        model_name = os.path.basename(model_path.strip("/")) or "all-MiniLM-L6-v2"

        # Download from Hugging Face and save to local path
        model = SentenceTransformer(model_name)
        os.makedirs(model_path, exist_ok=True)
        model.save(model_path)
        print(f"✅ Model saved locally to: {model_path}")
        return model

    # Load from local directory
    print(f"📦 Loading local model from: {model_path}")
    return SentenceTransformer(model_path)


def encode_filter_list(label_to_texts, model):
    """Encodes extracted entity labels (concepts) and their corresponding text into embeddings."""
    return {label: model.encode([label] + texts, convert_to_tensor=True) for label, texts in label_to_texts.items()}

def entity_matches(label, text, embeddings, model):
    """
    Compares the label with the extracted text using semantic similarity.
    
    Args:
        label (str): The label (concept).
        text (str): The extracted text phrase.
        embeddings (torch.Tensor): Precomputed embeddings for comparison.
        model (SentenceTransformer): The sentence transformer model.
    
    Returns:
        float: Cosine similarity score.
    """
    label_embedding = model.encode(label, convert_to_tensor=True)
    text_embedding = model.encode(text, convert_to_tensor=True)
    similarity_score = util.cos_sim(label_embedding, text_embedding)
    return similarity_score.item()

def row_matches(entities, filter_list_embeddings, model, threshold):
    """
    Filters out entities whose similarity with their label is below the threshold.
    
    Args:
        entities (list): List of entity dictionaries.
        filter_list_embeddings (dict): Dictionary of precomputed label-based embeddings.
        model (SentenceTransformer): The sentence transformer model.
        threshold (float): Cosine similarity threshold for filtering.
    
    Returns:
        tuple: (best_concept, best_similarity_score, matched_keyword) if a match is found, otherwise (None, 0, None).
    """
    best_concept = None
    best_similarity_score = 0
    matched_keyword = None

    for entity in entities:
        label = entity.get("label")
        text = entity.get("text")
        
        if label in filter_list_embeddings:
            similarity_score = entity_matches(label, text, filter_list_embeddings[label], model)
            if similarity_score > best_similarity_score and similarity_score > threshold:
                best_concept = label
                best_similarity_score = similarity_score
                matched_keyword = text

    return best_concept, best_similarity_score, matched_keyword

def save_to_date_folder(data, concept, base_output_folder):
    """Saves filtered data to a date-based folder, including similarity scores."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_folder = os.path.join(base_output_folder, date_str)
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, f"{concept}.csv")
    pd.DataFrame(data).to_csv(output_file, index=False)
    print(f"Saved {len(data)} records to {output_file}")

def merge_csvs_to_jsonl(base_output_folder):
    """Merges all CSV files from the date-based folder into a single JSONL while avoiding duplication."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_folder = os.path.join(base_output_folder, date_str)

    all_files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith(".csv")]

    dataframes = [pd.read_csv(f) for f in all_files]
    merged_df = pd.concat(dataframes, ignore_index=True).drop_duplicates()

    # Convert to JSONL format
    final_output_filename = os.path.join(base_output_folder, f"{date_str}_merged.jsonl")
    merged_df.to_json(final_output_filename, orient="records", lines=True)

    print(f"Merged JSONL saved as {final_output_filename}")


def semantic_filtering(extracted_entities_file, base_output_folder, model_dir, threshold=0.8):
    """
    Filters records based on semantic similarity and saves similarity scores.
    
    Args:
        extracted_entities_file (str): Path to the JSONL file containing extracted entities.
        base_output_folder (str): Base directory for output.
        model_dir (str): Path to the sentence transformer model.
        threshold (float): Cosine similarity threshold for filtering.
    """
    label_to_texts, records = load_extracted_entities(extracted_entities_file)
    model = load_model(model_dir)
    filter_list_embeddings = encode_filter_list(label_to_texts, model)
    
    filtered_data_by_concept = {concept: [] for concept in filter_list_embeddings}

    for record in records:
        entities = record.get("extracted_entities", [])
        best_concept, best_similarity_score, matched_keyword = row_matches(entities, filter_list_embeddings, model, threshold)

        if best_concept:
            # Add similarity information to the record before saving
            record["assigned_concept"] = best_concept
            record["matched_keyword"] = matched_keyword
            record["similarity_score"] = best_similarity_score
            filtered_data_by_concept[best_concept].append(record)
    
    # Save results by concept
    for concept, data in filtered_data_by_concept.items():
        if data:
            save_to_date_folder(data, concept, base_output_folder)

    # Merge all saved CSVs
    final_output_filename = os.path.join(base_output_folder, f"merged_{datetime.now().strftime('%Y-%m-%d')}.csv")
    merge_csvs_to_jsonl(base_output_folder)

# Define paths
today = datetime.now()
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
