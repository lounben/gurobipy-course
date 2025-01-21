import numpy as np
import gurobipy as gp
from gurobipy import GRB

def generate_knapsack(num_items):
    # Fix seed value
    rng = np.random.default_rng(seed=0)
    # Generate item values and weights
    values = rng.uniform(low=1, high=25, size=num_items)
    weights = rng.uniform(low=5, high=100, size=num_items)
    # Set knapsack capacity to 70% of total weight
    capacity = 0.7 * weights.sum()

    return values, weights, capacity

def solve_knapsack_model(values, weights, capacity):
    num_items = len(values)
    
    # Convert numpy arrays to dictionaries for Gurobi
    values_dict = {i: values[i] for i in range(num_items)}
    weights_dict = {i: weights[i] for i in range(num_items)}

    with gp.Env() as env:
        with gp.Model(name="knapsack", env=env) as model:
            # Define decision variables (binary variables)
            x = model.addVars(num_items, vtype=GRB.BINARY, name="x")

            # Set the objective function (maximize total value)
            model.setObjective(gp.quicksum(values_dict[i] * x[i] for i in range(num_items)), GRB.MAXIMIZE)

            # Add the capacity constraint
            model.addConstr(gp.quicksum(weights_dict[i] * x[i] for i in range(num_items)) <= capacity, name="capacity")

            # Optimize the model
            model.optimize()

            # Check the optimization status
            if model.Status == GRB.OPTIMAL:
                selected_items = [i for i in range(num_items) if x[i].x > 0.5]
                total_value = model.objVal
                print(f"Total value: {total_value:.2f}")
                print(f"Selected items: {selected_items}")
                return selected_items, total_value
            else:
                print("No optimal solution found.")
                return [], 0

# Example usage
data = generate_knapsack(10000)
solve_knapsack_model(*data)
