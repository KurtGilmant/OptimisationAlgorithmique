import json
import math
from score_function import getSolutionScore

def load_dataset(filename):
    with open(f'./datasets/{filename}.json') as f:
        return json.load(f)

def get_max_pop(building):
    return max(building['populationPeakHours'], 
               building['populationOffPeakHours'], 
               building['populationNight'])

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

ANTENNAS = [
    ('Nano', 50, 200, 5000),
    ('Spot', 100, 800, 15000),
    ('Density', 150, 5000, 30000),
    ('MaxRange', 400, 3500, 40000)
]

def simple_greedy(dataset):
    buildings = dataset['buildings']
    uncovered = set(range(len(buildings)))
    antennas = []
    
    while uncovered:
        best = None
        best_ratio = float('inf')
        
        # Pour chaque bâtiment non couvert, essayer chaque type d'antenne
        for bid in list(uncovered)[:50]:  # Limiter pour éviter timeout
            b = buildings[bid]
            
            for ant_name, ant_range, ant_cap, ant_cost in ANTENNAS:
                # Compter combien de bâtiments on peut couvrir
                covered = []
                total_pop = 0
                
                for oid in uncovered:
                    o = buildings[oid]
                    if distance(b['x'], b['y'], o['x'], o['y']) <= ant_range:
                        pop = get_max_pop(o)
                        if total_pop + pop <= ant_cap:
                            covered.append(oid)
                            total_pop += pop
                
                if covered:
                    ratio = ant_cost / len(covered)
                    if ratio < best_ratio:
                        best_ratio = ratio
                        best = {
                            'type': ant_name,
                            'x': b['x'],
                            'y': b['y'],
                            'buildings': covered
                        }
        
        if best:
            antennas.append(best)
            for bid in best['buildings']:
                uncovered.discard(bid)
            print(f"Reste {len(uncovered)} bâtiments")
        else:
            print("Impossible de continuer!")
            break
    
    return {'antennas': antennas}

# Test
dataset = load_dataset('3_suburbia')
print(f"Bâtiments: {len(dataset['buildings'])}")

solution = simple_greedy(dataset)
print(f"Antennes: {len(solution['antennas'])}")

cost, valid, msg = getSolutionScore(json.dumps(solution), json.dumps(dataset))
print(msg)

if valid:
    with open(f'./solutions/solution_3_suburbia_{cost}.json', 'w') as f:
        json.dump(solution, f, indent=2)
