#!/usr/bin/env python3
"""
Oracle Biblico PRO - Training Data Preparation
Processes Bible texts into training dataset format
"""

import json
from pathlib import Path
from typing import List, Dict

class TrainingDataPreparator:
    """Prepares biblical texts for fine-tuning Llama3.1"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.processed_dir = self.data_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def load_raw_data(self) -> Dict:
        """Loads raw Bible texts from data/raw/"""
        print("Loading raw Bible data...")
        raw_file = self.data_dir / "raw" / "bible_metadata.json"
        
        if raw_file.exists():
            with open(raw_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"books": []}
    
    def create_training_samples(self, data: Dict) -> List[str]:
        """Creates training samples from Bible texts"""
        print("Creating training samples...")
        samples = []
        
        for book in data.get("books", []):
            sample = {
                "text": f"{book['name']} - {book['chapters']} chapters",
                "languages": book.get("languages", []),
                "metadata": {
                    "book_name": book['name'],
                    "chapter_count": book['chapters'],
                    "verse_count": book['verses']
                }
            }
            samples.append(json.dumps(sample, ensure_ascii=False))
        
        return samples
    
    def save_training_data(self, samples: List[str]):
        """Saves training data to processed directory"""
        output_file = self.processed_dir / "training_data.jsonl"
        
        with open(output_file, "w", encoding="utf-8") as f:
            for sample in samples:
                f.write(sample + "\n")
        
        print(f"✓ Saved {len(samples)} training samples to {output_file}")
    
    def prepare(self):
        """Main preparation pipeline"""
        data = self.load_raw_data()
        samples = self.create_training_samples(data)
        self.save_training_data(samples)
        print("\n✅ Training data preparation complete!")

def main():
    print("="*50)
    print("Oracle Biblico PRO - Training Data Preparation")
    print("="*50)
    
    preparator = TrainingDataPreparator()
    preparator.prepare()

if __name__ == "__main__":
    main()
