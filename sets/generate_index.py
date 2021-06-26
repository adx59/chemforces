#!/usr/bin/env python3
import json
import os

def generate(output):
    generated = {}

    for set in os.listdir("."):
        if not os.path.isdir(set):
            continue

        for prob in os.listdir(f"./{set}/probs/"):
            prob_no = int(prob.split(".")[0])
            generated[f"{set}_{prob_no}"] = {"prob": f"sets/{set}/probs/{prob}"}

            for page in os.listdir(f"./{set}/pages/"):
                pageX = page.split(".")[0]
                
                start = int(pageX.split("_")[0]); end = int(pageX.split("_")[1])
                if prob_no <= end and prob_no >= start:
                    generated[f"{set}_{prob_no}"]["page"] = f"sets/{set}/pages/{page}"
                    break

            for half in os.listdir(f"./{set}/halves/"):
                halfX = half.split(".")[0]

                start = int(halfX.split("_")[0]); end = int(halfX.split("_")[1])
                if prob_no <= end and prob_no >= start:
                    generated[f"{set}_{prob_no}"]["half"] = f"sets/{set}/halves/{half}"
                    break
    
    with open(output, "w") as out:
        json.dump(generated, out, indent=4)

if __name__ == "__main__":
    generate("index.json")