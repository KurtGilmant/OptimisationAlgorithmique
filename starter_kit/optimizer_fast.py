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

def fast_greedy(dataset):
    buildings = dataset['buildings']
    n = len(buildings)
    uncovered = set(range(n))
    antennas = []
    max_pops = [get_max_pop(b) for b in buildings]
    
    iteration = 0
    while uncovered:
        iteration += 1
        if iteration % 100 == 0:
            print(f"Itération {iteration}, reste {len(uncovered)}")
        
        best = None
        best_ratio = float('inf')
        
        # Échantillonner seulement quelques bâtiments
        sample = list(uncovered)[:min(20, len(uncovered))]
        
        for bid in sample:
            b = buildings[bid]
            
            # Essayer seulement les antennes pertinentes
            for ant_name, ant_range, ant_cap, ant_cost in ANTENNAS:
                covered = []
                total_pop = 0
                
                for oid in uncovered:
                    if len(covered) >= 50:  # Limite pour accélérer
                        break
                    o = buildings[oid]
                    if distance(b['x'], b['y'], o['x'], o['y']) <= ant_range:
                        pop = max_pops[oid]
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
        else:
            break
    
    return {'antennas': antennas}

dataset = load_dataset('3_suburbia')
print(f"Bâtiments: {len(dataset['buildings'])}")

solution = fast_greedy(dataset)
print(f"\nAntennes: {len(solution['antennas'])}")

cost, valid, msg = getSolutionScore(json.dumps(solution), json.dumps(dataset))
print(msg)

if valid:
    with open(f'./solutions/solution_3_suburbia_{cost}.json', 'w') as f:
        json.dump(solution, f, indent=2)
    print("Sauvegardé!")
