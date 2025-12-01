import pandas as pd
import matplotlib.pyplot as plt
import requests

# Chargement des données météo
def charger_csv(path):
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    return df

# Quelques statistiques rapides
def stats_meteo(df):
    return df.describe()

# Recherche des jours extrêmes
def jours_extremes(df):
    chaud = df.loc[df['temperature'].idxmax()]
    froid = df.loc[df['temperature'].idxmin()]
    return chaud, froid

# Graphique simple
def plot_variable(df, colonne, titre):
    plt.figure(figsize=(10,4))
    plt.plot(df['date'], df[colonne], marker='o')
    plt.title(titre)
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Appel API météo
def meteo_actuelle(ville="Montpellier", lat=43.61, lon=3.87):
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,precipitation",
                "timezone": "Europe/Paris",
            }
        )
        data = r.json().get("current", {})
        print(f"\n--- Météo actuelle à {ville} ---")
        print(f"Température : {data.get('temperature_2m')} °C")
        print(f"Humidité    : {data.get('relative_humidity_2m')} %")
        print(f"Pluie       : {data.get('precipitation')} mm\n")
    except Exception as e:
        print("Erreur lors de la récupération de la météo :", e)

# Export simple du rapport
def exporter(df, chaud, froid, fichier="rapport.txt"):
    with open(fichier, "w") as f:
        f.write("Rapport météo\n")
        f.write(str(df.describe()))
        f.write("\n\nJour le plus chaud : "
                f"{chaud['date'].strftime('%Y-%m-%d')} ({chaud['temperature']} °C)")
        f.write("\nJour le plus froid : "
                f"{froid['date'].strftime('%Y-%m-%d')} ({froid['temperature']} °C)\n")

    print(f"Rapport exporté dans {fichier}")

# Programme principal
def main():
    df = charger_csv("meteo.csv")

    print("\n--- Statistiques ---")
    print(df.describe())

    chaud, froid = jours_extremes(df)
    print("\nJour le plus chaud :", chaud['date'].date(), chaud['temperature'], "°C")
    print("Jour le plus froid :", froid['date'].date(), froid['temperature'], "°C")

    plot_variable(df, "temperature", "Évolution de la température")
    plot_variable(df, "humidite", "Évolution de l'humidité")

    meteo_actuelle()

    exporter(df, chaud, froid)

main()
