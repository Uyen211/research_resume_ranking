import json
import re

def clean_text(text):
    # Remove anything in parenthesis
    text = re.sub(r'\(.*?\)', '', text)
    # Remove trailing hyphenated repeated terms like "good client - client" -> "good client"
    if ' - ' in text:
        parts = text.split(' - ')
        text = parts[0]
    # Trim and clean up whitespace
    return text.strip().lower()

def restructure_taxonomy(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Categories we want to keep for IT/Software Resume Ranking
    target_categories = [
        "Attitudes, communication and social skills",
        "Cognitative skills and languages", 
        "Management, business processes and administration",
        "Digital and technology"
    ]
    
    restructured_data = {}
    
    for top_cat, subcats in data.items():
        if top_cat not in target_categories:
            continue
            
        clean_cat_name = top_cat
        if top_cat == "Cognitative skills and languages":
            clean_cat_name = "Cognitive Skills and Languages" # Fix spelling
            
        restructured_data[clean_cat_name] = {}
        
        for subcat_name, leaf_groups in subcats.items():
            for leaf_name, items in leaf_groups.items():
                
                # To remove the deep arbitrary nesting, we will group items under their leaf_name
                # within the top-level category.
                if leaf_name not in restructured_data[clean_cat_name]:
                    restructured_data[clean_cat_name][leaf_name] = set()
                    
                for id_str, raw_text in items.items():
                    cleaned = clean_text(raw_text)
                    # Simple heuristic against extreme noise
                    if len(cleaned.split()) > 1 and len(cleaned) > 5 and not cleaned.isdigit():
                        restructured_data[clean_cat_name][leaf_name].add(cleaned)

    # Convert sets back to lists for JSON serialization and remove empty categories
    final_output = {}
    for cat, subcats in restructured_data.items():
        final_output[cat] = {}
        for sub, items_set in subcats.items():
            if len(items_set) > 0:
                final_output[cat][sub] = sorted(list(items_set))
                
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully restructured taxonomy into {output_file}")
    
    # Print some stats
    total_nodes_before = sum(len(items) for c in data.values() for g in c.values() for items in g.values())
    total_nodes_after = sum(len(i) for c in final_output.values() for i in c.values())
    print(f"Total phrases before (whole document): {total_nodes_before}")
    print(f"Total phrases after cleaning & filtering: {total_nodes_after}")

if __name__ == "__main__":
    restructure_taxonomy(
        'data/taxonomy/2022.01.21_hierarchy_structure_named.json',
        'data/taxonomy/soft_skills_ontology.json'
    )
