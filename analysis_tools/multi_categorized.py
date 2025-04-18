import os
import json
import argparse
from collections import defaultdict

def main(dataset):
    # Load the category information
    with open(f"data/results/{dataset}_categories.json", "r") as f:
        categories_data = json.load(f)

    # Create a mapping from question UUID to its categories
    question_to_categories = {}
    for item in categories_data:
        question_id, uuid, question, category_ids = item
        question_to_categories[uuid] = category_ids

    # Load the text and video data
    with open(f"data/results/{dataset}_single_text.json", "r") as f:
        text_data = json.load(f)

    with open(f"data/results/{dataset}_single_video.json", "r") as f:
        video_data = json.load(f)

    with open(f"data/results/{dataset}_single_graph.json", "r") as f:
        graph_data = json.load(f)

    # Initialize the result dictionary
    result = defaultdict(dict)

    # Process each question in the annotation data
    for video_id, data in text_data.items():
        uuid = video_id
        
        # Skip if the question is not in our categories mapping
        if uuid not in question_to_categories:
            continue
        
        categories = question_to_categories[uuid]
        
        # Determine which data source to use based on the category
        if 0 in categories:
            result[uuid] = graph_data[uuid]
        elif {1, 2, 3} & set(categories):
            if uuid in text_data:
                result[uuid] = text_data[uuid]
        else:
            if uuid in video_data:
                result[uuid] = video_data[uuid]

    # Save the categorized results
    with open(f"data/results/{dataset}_multi_categorized.json", "w") as f:
        json.dump(dict(result), f, indent=4)

    print(f"Processed {len(result)} questions and saved to results/{dataset}_multi_categorized.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process dataset for multi-categorized results")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name (e.g., egoschema_fullset)")
    args = parser.parse_args()
    
    main(args.dataset)
