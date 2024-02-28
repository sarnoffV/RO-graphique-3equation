
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_inequalities(coefficients, operators, constants, aZ, bZ, c_initial,valeurs_variables):
    xP = valeurs_variables["x1"]
    yP = valeurs_variables["x2"]
    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        nonlocal c_initial

        if frame == 0:  # Pause de 1 seconde avant le tracé de la première droite
            plt.pause(1)
            return line,

        if frame == 1:  # Affichage de la droite Z en position initiale
            animation.event_source.stop()
            ax.plot(xP, yP, 'go', markersize=10)
            ax.text(xP + 0.2, yP, f'Point optimal ({xP:.2f}, {yP:.2f})', fontsize=8)
            plt.pause(0.001)
            return line,

        # Calculez la nouvelle valeur de c pour la droite en fonction du frame
        c_current = c_initial - frame * (c_initial - (aZ * xP + bZ * yP))

        # Générer les coordonnées x et y pour la droite
        x = np.linspace(-1000, 1000, 100)
        y = (c_current - aZ * x) / bZ

        # Mettez à jour les données de la droite
        line.set_data(x, y)

        return line,

    # Créer une figure et des axes
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(-50, 200)
    ax.set_ylim(-5,90 )
    # Ajouter le repère orthonormé
    ax.axhline(0, color='black', lw=0.8)
    ax.axvline(0, color='black', lw=0.8)

    # Label des axes
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')

    # Pause de 1 seconde avant le tracé de la première droite
    plt.pause(1)


    # Tracer les inéquations et colorer les zones solution et non solution
    for i in range(len(coefficients)):
        a, b = coefficients[i]
        c = constants[i]
        operator = operators[i]

        # Générer les coordonnées x1 et x2 pour tracer la droite
        x1 = np.linspace(-1000, 1000, 100)

        if b != 0:
            x2 = (c - a * x1) / b

            # Tracer la droite correspondant à l'équation ax1 + bx2 = c
            ax.plot(x1, x2, label=f"{a}x1 + {b}x2 {operator} {c}")

            # Remplir la zone de solution (au-dessus ou en dessous de la droite selon l'opérateur et le signe de b)
            if operator == "<=" or operator == "<":
                if b > 0:
                    ax.fill_between(x1, x2, -10, color='gray', alpha=0.5)
                else:
                    ax.fill_between(x1, x2, 10, color='gray', alpha=0.5)
            elif operator == ">=" or operator == ">":
                if b > 0:
                    ax.fill_between(x1, x2, 10, color='gray', alpha=0.5)
                else:
                    ax.fill_between(x1, x2, -10, color='gray', alpha=0.5)
        else:
            x2 = np.linspace(-1000, 1000, 100)
            x1 = c / a * np.ones(100)
            ax.plot(x1, x2, label=f"{a}x1 + {b}x2 {operator} {c}", color='black')
            # Remplir la zone de solution lorsque b est égal à zéro
            if operator == "<=" or operator == "<":
                ax.fill_betweenx(x2, x1, -10, color='gray', alpha=0.5)
            elif operator == ">=" or operator == ">":
                ax.fill_betweenx(x2, x1, 10, color='gray', alpha=0.5)

        plt.pause(1)

    c_initial_Z = c_initial
    x_Z = np.linspace(-1000, 1000, 100)
    y_Z = (c_initial_Z - aZ * x_Z) / bZ
    ax.plot(x_Z, y_Z, label=f"{aZ}x1 + {bZ}x2 = {c_initial_Z}", color='blue')

    animation = FuncAnimation(fig, update, frames=np.linspace(0, 1, 100), init_func=init, blit=True, interval=50)

    # Légende
    ax.legend()

    plt.show()


