import os
import kaggle

def download_arxiv_data(download_path):
    """
    Downloads and extracts the arXiv dataset from Kaggle.
    
    Args:
        download_path (str): The directory where the dataset will be stored.
    
    Returns:
        str: The path to the downloaded dataset.
    """
    dataset_name = "Cornell-University/arxiv"
    os.makedirs(download_path, exist_ok=True)
    
    kaggle.api.dataset_download_files(dataset_name, path=download_path, unzip=True)
    
    print(f"Dataset downloaded and extracted to {download_path}")
    return download_path

