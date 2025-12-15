import json
from score_function import getSolutionScore

dataset = json.load(open('./datasets/1_peaceful_village.json'))

solutions = [
    # Spot sur 2 pour 1,2,3 + Nano hors bâtiment entre 0 et 4
    {
        "antennas": [
            {"type": "Spot", "x": 200, "y": 0, "buildings": [1, 2, 3]},
            {"type": "Nano", "x": 25, "y": 0, "buildings": [0, 4]}
        ]
    },
    # Spot sur 1 pour 0,1,2 + Nano hors bâtiment pour 3,4
    {
        "antennas": [
            {"type": "Spot", "x": 100, "y": 0, "buildings": [0, 1, 2]},
            {"type": "Nano", "x": 350, "y": 0, "buildings": [3, 4]}
        ]
    },
]

for i, sol in enumerate(solutions):
    cost, valid, msg = getSolutionScore(json.dumps(sol), json.dumps(dataset))
    print(f"Solution {i+1}: {msg}")
