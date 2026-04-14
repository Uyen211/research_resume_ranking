import json

def analyze(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print("Top Level Categories:")
    for key in data.keys():
        print(f"- {key}")

    # Let's sample one category to see its depth
    sample_cat = data.get("Attitudes, communication and social skills", {})
    print("\n--- Depth Analysis of 'Attitudes, communication and social skills' ---")
    for subcat_name, subcat_val in list(sample_cat.items())[:3]:
        print(f"  Subcat: {subcat_name}")
        for leaf_name, leaf_val in list(subcat_val.items())[:2]:
            print(f"    Leaf Group: {leaf_name}")
            count = 0
            for id_str, text_val in leaf_val.items():
                if count < 3:
                    print(f"      ID: {id_str} => Text: {text_val}")
                count += 1
            print(f"      ... Total phrases in this group: {len(leaf_val)}")

if __name__ == "__main__":
    analyze('data/taxonomy/2022.01.21_hierarchy_structure_named.json')
