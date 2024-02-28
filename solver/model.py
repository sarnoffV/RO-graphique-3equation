from pulp import LpProblem, LpVariable, LpMaximize, LpMinimize, value

def resoudre_probleme(inéquations, équation, analyse):
    # Créez le problème de programmation linéaire
    prob = LpProblem("Probleme de programmation lineaire", LpMaximize if analyse == "MAX" else LpMinimize)

    # Définissez les variables
    variables = []
    for i in range(2):
        variables.append(LpVariable(f"x{i+1}", lowBound=0))

    # Définissez les contraintes (inéquations)
    for inequation in inéquations:
        constraint = sum(coef * var for coef, var in zip(inequation["coefficients"], variables))
        if inequation["operateur"] == "<=":
            prob += constraint <= inequation["constante"]
        elif inequation["operateur"] == ">=":
            prob += constraint >= inequation["constante"]
        elif inequation["operateur"] == "=":
            prob += constraint == inequation["constante"]

    # Définissez l'objectif (équation de Z)
    prob += sum(coef * var for coef, var in zip(équation, variables))

    # Résolvez le problème
    prob.solve()

    # Récupérez les valeurs optimales des variables et de l'objectif
    valeurs_variables = {var.name: value(var) for var in prob.variables()}
    valeur_objectif = value(prob.objective)

    return valeurs_variables, valeur_objectif

