import json
from score_function import getSolutionScore
import math

dataset = json.load(open('./datasets/2_small_town.json'))

# Vérifions si Density sur 3 peut couvrir d'autres bâtiments (portée 150)
b3 = dataset['buildings'][3]
print(f"Density sur bâtiment 3 ({b3['x']}, {b3['y']}) - portée 150:")
for b in dataset['buildings']:
    if b['id'] != 3:
        dist = math.sqrt((b3['x'] - b['x'])**2 + (b3['y'] - b['y'])**2)
        print(f"  Bâtiment {b['id']}: {dist:.2f} {'✓' if dist <= 150 else '✗'}")

# Essayons Density sur 3 couvrant aussi 0 ou 1 + Spot pour les autres
solutions = [
    # Density sur 3+0 + Spot sur 1+2
    {
        "antennas": [
            {"type": "Density", "x": 205, "y": 85, "buildings": [3, 0]},
            {"type": "Spot", "x": 250, "y": 180, "buildings": [1, 2]}
        ]
    },
    # Density sur 3+1 + Spot sur 0+2
    {
        "antennas": [
            {"type": "Density", "x": 205, "y": 85, "buildings": [3, 1]},
            {"type": "Spot", "x": 165, "y": 225, "buildings": [0, 2]}
        ]
    },
]

for i, sol in enumerate(solutions):
    cost, valid, msg = getSolutionScore(json.dumps(sol), json.dumps(dataset))
    print(f"\nSolution {i+1}: {msg}")
