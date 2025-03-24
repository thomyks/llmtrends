import json
from tqdm import tqdm
from gliner import GLiNER
import os 
from config import WEEKLY_DATA_PATH
import datetime


# Load the GLiNER model
model_path = "/Users/tomasnagy/FastAPI/application/models/ner/gliner_medium_v2.1"
config_file = os.path.join(model_path, "gliner_config.json")


# Load or download the GLiNER model
if os.path.exists(config_file):
    print(f"Loading model from local path: {model_path}")
    model = GLiNER.from_pretrained(model_path)
else:
    print("Model not found locally or config file missing. Downloading from Hugging Face...")
    model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
    os.makedirs(model_path, exist_ok=True)
    model.save_pretrained(model_path)
    print(f"Model downloaded and saved to {model_path}")

# List of entities of interest
labels = [
    "Large Language Model", "Open-source LLMs", "LLM", "Mistral", "LLMs", "LLM-based", "LLM-powered",
    "GPT", "RAG", "GPT-4", "GPT-3", "GPT-2", "ChatGPT", "GPT model", "Llama",
    "Generative Pre-trained Transformer (GPT)", "BERT", "RoBERTa", "DistilBERT",
    "ALBERT", "Knowledge distillation", "Transformer-based model",
    "Neural Language Model", "Transformers", "Attention mechanism", "Prompting",
    "Chain of thought", "Scaling law", "Model Bias and Fairness", "Foundation Model",
    "AI model", "AI language model", "NLP model", "Embedding", "contextual Embedding",
    "quantisation", "Fine-tuning", "Zero-shot Learning", "Few-shot Learning", "AI Ethics"
]

def extract_entities_from_abstracts(input_file, output_file, max_rows):
    """Extracts relevant concepts from the abstracts of filtered papers."""
    processed_papers = []

    with open(input_file, "r", encoding="utf-8") as f:
        for i, line in tqdm(enumerate(f), desc="Extracting entities", total=max_rows):
            if i >= max_rows:
                break  # Stop processing after 500 rows

            paper = json.loads(line.strip())
            abstract = paper.get("abstract", "")

            if abstract:
                # Extract entities using GLiNER
                entities = model.predict_entities(abstract, labels)
                extracted_entities = [{"text": entity["text"], "label": entity["label"]} for entity in entities]
                paper["extracted_entities"] = extracted_entities  # Add entities to the paper
            processed_papers.append(paper)

    # Save results with extracted entities
    with open(output_file, "w", encoding="utf-8") as f_out:
        for paper in processed_papers:
            f_out.write(json.dumps(paper) + "\n")

    print(f"Entity extraction complete. {len(processed_papers)} papers saved to {output_file}.")


def save_papers_with_entities(input_file, output_filtered_file):
    """Filters and saves only rows that have at least one extracted entity."""
    filtered_papers = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            paper = json.loads(line.strip())
            extracted_entities = paper.get("extracted_entities", [])
            if extracted_entities:  # If there's at least one entity, keep it
                filtered_papers.append(paper)

    # Save the filtered papers to a new JSONL file
    with open(output_filtered_file, "w", encoding="utf-8") as f_out:
        for paper in filtered_papers:
            f_out.write(json.dumps(paper) + "\n")

    print(f"Saved {len(filtered_papers)} papers with extracted entities to {output_filtered_file}")


# # Run the function to save filtered papers
# today = datetime.datetime.utcnow().date()
# input_filename = f"filtered_papers_{today.strftime('%Y-%m-%d')}.jsonl"
# input_file = os.path.join(WEEKLY_DATA_PATH, input_filename)
# output_filename = f"filtered_papers_{today.strftime('%Y-%m-%d')}_with_entities.jsonl" 
# output_file = os.path.join(WEEKLY_DATA_PATH, output_filename)
# output_filename_only_llm = f"filtered_papers_{today.strftime('%Y-%m-%d')}_with_entities.jsonl" 
# output_file_only_llm = os.path.join(WEEKLY_DATA_PATH, output_filename)
# # Get the number of rows. This paramater in theory could be later removed. 
# num_rows = sum(1 for _ in open(input_file, "r", encoding="utf-8"))
# # Extract entities with GLINER
# extract_entities_from_abstracts(input_file, output_file, max_rows=num_rows)
# # Filter out only LLM-captured
# save_papers_with_entities(output_file, output_file_only_llm)


