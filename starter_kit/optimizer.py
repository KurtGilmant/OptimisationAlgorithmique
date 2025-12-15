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

ANTENNAS = {
    'Nano': {'range': 50, 'capacity': 200, 'cost_on': 5000, 'cost_off': 6000},
    'Spot': {'range': 100, 'capacity': 800, 'cost_on': 15000, 'cost_off': 20000},
    'Density': {'range': 150, 'capacity': 5000, 'cost_on': 30000, 'cost_off': 50000},
    'MaxRange': {'range': 400, 'capacity': 3500, 'cost_on': 40000, 'cost_off': 50000}
}

def greedy_solution(dataset):
    buildings = dataset['buildings']
    uncovered = set(range(len(buildings)))
    antennas = []
    
    # Calculer population max pour chaque bâtiment
    max_pops = [get_max_pop(b) for b in buildings]
    
    while uncovered:
        best_antenna = None
        best_cost_per_building = float('inf')
        
        # Pour chaque bâtiment non couvert
        for bid in uncovered:
            b = buildings[bid]
            
            # Essayer chaque type d'antenne sur ce bâtiment
            for ant_type, specs in ANTENNAS.items():
                # Trouver tous les bâtiments couverts par cette antenne
                covered = []
                total_pop = 0
                
                for other_id in uncovered:
                    other = buildings[other_id]
                    dist = distance(b['x'], b['y'], other['x'], other['y'])
                    
                    if dist <= specs['range']:
                        new_pop = total_pop + max_pops[other_id]
                        if new_pop <= specs['capacity']:
                            covered.append(other_id)
                            total_pop = new_pop
                
                if covered:
                    cost = specs['cost_on']
                    cost_per_building = cost / len(covered)
                    
                    if cost_per_building < best_cost_per_building:
                        best_cost_per_building = cost_per_building
                        best_antenna = {
                            'type': ant_type,
                            'x': b['x'],
                            'y': b['y'],
                            'buildings': covered
                        }
        
        if best_antenna:
            antennas.append(best_antenna)
            for bid in best_antenna['buildings']:
                uncovered.discard(bid)
        else:
            break
    
    return {'antennas': antennas}

# Test sur suburbia
dataset = load_dataset('3_suburbia')
print(f"Nombre de bâtiments: {len(dataset['buildings'])}")

solution = greedy_solution(dataset)
print(f"Nombre d'antennes: {len(solution['antennas'])}")

cost, valid, msg = getSolutionScore(json.dumps(solution), json.dumps(dataset))
print(msg)

if valid:
    with open(f'./solutions/solution_3_suburbia_{cost}.json', 'w') as f:
        json.dump(solution, f, indent=2)
    print(f"Solution sauvegardée!")
