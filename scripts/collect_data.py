#!/usr/bin/env python3
"""
Oracle Biblico PRO - Data Collection Script
Collects Bible texts and resources for training
"""

import json
import os
from pathlib import Path

def collect_bible_texts():
    """
    Collects Bible texts from various sources
    Stores in JSON format for processing
    """
    print("Collecting Bible texts...")
    
    # Create data directories
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    
    # Sample Bible texts structure
    bible_data = {
        "testament": "Old Testament",
        "books": [
            {
                "name": "Genesis",
                "chapters": 50,
                "verses": 1533,
                "languages": ["Hebrew", "English", "Portuguese"]
            },
            {
                "name": "Exodus",
                "chapters": 40,
                "verses": 1213,
                "languages": ["Hebrew", "English", "Portuguese"]
            }
        ]
    }
    
    # Save Bible metadata
    with open("data/raw/bible_metadata.json", "w", encoding="utf-8") as f:
        json.dump(bible_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Collected metadata for {len(bible_data['books'])} books")

def collect_reference_texts():
    """
    Collects reference texts for context
    - Hebrew grammar references
    - Aramaic references  
    - Greek references
    """
    print("Collecting reference texts...")
    
    references = {
        "linguistic_resources": {
            "hebrew_grammar": "data/references/hebrew_grammar.txt",
            "aramaic_references": "data/references/aramaic.txt",
            "greek_references": "data/references/greek.txt"
        },
        "theological_references": {
            "commentary_collection": "data/references/commentaries.json",
            "historical_context": "data/references/history.json"
        }
    }
    
    print(f"✓ Catalogued {len(references)} reference collections")
    return references

def main():
    print("="*50)
    print("Oracle Biblico PRO - Data Collection")
    print("="*50)
    
    try:
        collect_bible_texts()
        refs = collect_reference_texts()
        
        print("\n✅ Data collection completed successfully!")
        print(f"References: {refs}")
        
    except Exception as e:
        print(f"❌ Error during collection: {e}")
        raise

if __name__ == "__main__":
    main()
