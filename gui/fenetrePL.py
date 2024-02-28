import tkinter as tk
from tkinter import messagebox, StringVar

import matplotlib.pyplot as plt

from solver.model import resoudre_probleme
from plotter.plotter import plot_inequalities


class Fenetre(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Programmation Linéaire - Résolution graphique")

        def valider_saisie():
            # Vérifier si les coefficients de Z sont renseignés
            if not zone_saisie_z_x1.get() or not zone_saisie_z_x2.get():
                messagebox.showerror("Erreur", "Les coefficients de Z sont requis.")
                return False

            # Vérifier si les opérateurs et les constantes des inéquations sont renseignés
            for i in range(3):
                if not zones_saisie_operateur[i].get() or not zones_saisie_constante[i].get():
                    messagebox.showerror("Erreur", "Les opérateurs et les constantes des inéquations sont requis.")
                    return False

            return True

        # Ajoutez les éléments de l'interface utilisateur (zones de saisie, bouton, etc.) ici

        # Définissez les actions à effectuer lorsque le bouton "Traiter" est cliqué
        def traiter():

            if not valider_saisie():
                return
            # Obtenez les valeurs des coefficients des variables et de l'équation Z à partir des zones de saisie
            coefficient_z_x1 = float(zone_saisie_z_x1.get())
            coefficient_z_x2 = float(zone_saisie_z_x2.get())
            equation = [coefficient_z_x1, coefficient_z_x2]

            # Obtenez les inéquations, les opérateurs et les constantes à partir des zones de saisie
            inéquations = []
            for i in range(3):
                coefficient_ineq_x1 = float(zones_saisie_ineq[i][0].get())
                coefficient_ineq_x2 = float(zones_saisie_ineq[i][1].get())
                operateur = zones_saisie_operateur[i].get()
                constante = float(zones_saisie_constante[i].get())
                inéquations.append({"coefficients": [coefficient_ineq_x1, coefficient_ineq_x2], "operateur": operateur, "constante": constante})

            # Obtenez l'analyse (MAX ou MIN) à partir de la sélection de l'utilisateur
            analyse = var_analyse.get()

            # Utilisez PuLP pour formuler le problème de programmation linéaire
            try:
                valeurs_variables, valeur_objectif = resoudre_probleme(inéquations, equation, analyse)
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
                print(e)
                return

            c_initial = 0 if analyse == "MAX" else 30

            plot_inequalities([ineq["coefficients"] for ineq in inéquations], [ineq["operateur"] for ineq in inéquations],[ineq["constante"] for ineq in inéquations],equation[0], equation[1], c_initial, valeurs_variables)

            plt.show()


        # Créez les zones de saisie pour les coefficients des variables et de l'équation Z
        frame_z = tk.Frame(self)
        frame_z.pack()

        label_z = tk.Label(frame_z, text=" Equation Z(")
        label_z.pack(side=tk.LEFT)

        zone_saisie_z_x1 = tk.Entry(frame_z)
        zone_saisie_z_x1.pack(side=tk.LEFT)

        label_z_plus = tk.Label(frame_z, text="x1 +")
        label_z_plus.pack(side=tk.LEFT)

        zone_saisie_z_x2 = tk.Entry(frame_z)
        zone_saisie_z_x2.pack(side=tk.LEFT)

        label_z_x2 = tk.Label(frame_z, text="x2 )")
        label_z_x2.pack(side=tk.LEFT)

        # Créez les zones de saisie pour les inéquations, les opérateurs et les constantes
        zones_saisie_ineq = []
        zones_saisie_operateur = []
        zones_saisie_constante = []

        for i in range(3):
            frame_ineq = tk.Frame(self)
            frame_ineq.pack()

            label_ineq = tk.Label(frame_ineq, text=f"Inéquation {i+1} = ")
            label_ineq.pack(side=tk.LEFT)

            zone_saisie_ineq_x1 = tk.Entry(frame_ineq)
            zone_saisie_ineq_x1.pack(side=tk.LEFT)

            label_ineq_plus = tk.Label(frame_ineq, text="x1 +")
            label_ineq_plus.pack(side=tk.LEFT)

            zone_saisie_ineq_x2 = tk.Entry(frame_ineq)
            zone_saisie_ineq_x2.pack(side=tk.LEFT)

            label_operateur = tk.Label(frame_ineq, text="x2   Opérateur")
            label_operateur.pack(side=tk.LEFT)

            zone_saisie_operateur = tk.Entry(frame_ineq)
            zone_saisie_operateur.pack(side=tk.LEFT)

            label_constante = tk.Label(frame_ineq, text=" Constante")
            label_constante.pack(side=tk.LEFT)

            zone_saisie_constante = tk.Entry(frame_ineq)
            zone_saisie_constante.pack(side=tk.LEFT)

            zones_saisie_ineq.append((zone_saisie_ineq_x1, zone_saisie_ineq_x2))
            zones_saisie_operateur.append(zone_saisie_operateur)
            zones_saisie_constante.append(zone_saisie_constante)

        # Créez la variable pour l'analyse (MAX ou MIN)
        var_analyse = StringVar()
        var_analyse.set("MAX")  # Par défaut, sélectionnez MAX

        # Créez les boutons radio pour l'analyse (MAX ou MIN)
        frame_analyse = tk.Frame(self)
        frame_analyse.pack()

        label_analyse = tk.Label(frame_analyse, text="Analyse")
        label_analyse.pack(side=tk.LEFT)

        bouton_max = tk.Radiobutton(frame_analyse, text="MAX", variable=var_analyse, value="MAX")
        bouton_max.pack(side=tk.LEFT)

        bouton_min = tk.Radiobutton(frame_analyse, text="MIN", variable=var_analyse, value="MIN")
        bouton_min.pack(side=tk.LEFT)

        # Créez le bouton "Traiter"
        bouton_traiter = tk.Button(self, text="Traiter", command=traiter)
        bouton_traiter.pack()