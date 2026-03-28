import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import numpy as np

path = r"C:\Users\ZGARNI\OneDrive\Documents\Bureau\analyse de données\analyse_notes\Notes (1).xlsx"
df = pd.read_excel(path, sheet_name="Feuil2", engine="openpyxl")

print("\n--- Dataset chargé ---")
print("Dimensions du dataset :", df.shape)
print("Colonnes disponibles :", df.columns.tolist())

n_eleves = df.shape[0]
print(f"\nNombre d'élèves ingénieurs : {n_eleves}")

matieres = df.select_dtypes(include='number').columns
n_matieres = len(matieres)
print(f"Nombre de matières évaluées : {n_matieres}")
print("Matières :", list(matieres))

moyennes = df[matieres].mean()
print("\n--- Moyennes par matière ---")
print(moyennes)

ecarts_types = df[matieres].std()
print("\n--- Écarts-types par matière ---")
print(ecarts_types)
print("Interprétation : un écart-type élevé indique une forte dispersion des notes.")

minimum = df[matieres].min()
maximum = df[matieres].max()
print("\n--- Valeurs minimales et maximales par matière ---")
print(pd.DataFrame({"Min": minimum, "Max": maximum}))

nom_col = None
for c in df.columns:
    if 'nom' in c.lower() or 'etudiant' in c.lower():
        nom_col = c
        break

outliers = pd.DataFrame()
for mat in matieres:
    moy = moyennes[mat]
    ecart = ecarts_types[mat]
    if nom_col:
        out = df[(df[mat] < moy - 2*ecart) | (df[mat] > moy + 2*ecart)][[nom_col, mat]].copy()
    else:
        out = df[(df[mat] < moy - 2*ecart) | (df[mat] > moy + 2*ecart)][[mat]].copy()
    out['Matiere'] = mat
    if not out.empty:
        outliers = pd.concat([outliers, out], axis=0)

print("\n--- Valeurs aberrantes détectées ---")
if not outliers.empty:
    print(outliers)
else:
    print("Aucune valeur aberrante détectée.")

corr = df[matieres].corr()
print("\n--- Matrice de corrélation ---")
print(corr)

plt.figure(figsize=(10,6))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Corrélations entre matières")
plt.tight_layout()
plt.show()

print("\n--- Matières fortement corrélées (>0.7 ou <-0.7) ---")
deja_vu = set()
for i in matieres:
    for j in matieres:
        if i != j and (corr.loc[i,j] > 0.7 or corr.loc[i,j] < -0.7):
            if (j,i) not in deja_vu:
                print(f"{i} - {j} : {corr.loc[i,j]:.2f}")
                deja_vu.add((i,j))

matiere_preferee = matieres[0]
print("\nMatière choisie pour distribution :", matiere_preferee)

data = df[matiere_preferee].dropna()

plt.figure(figsize=(8,5))
plt.hist(data, bins=10, density=True)

xmin, xmax = data.min(), data.max()
x = np.linspace(xmin, xmax, 100)
plt.plot(x, norm.pdf(x, data.mean(), data.std()))

plt.title("Distribution des notes : " + matiere_preferee)
plt.xlabel("Note")
plt.ylabel("Densité")
plt.tight_layout()
plt.show()

if 'Groupe' in df.columns:
    print("\nGroupes disponibles :", df['Groupe'].unique())
    groupe = input("Entrez votre groupe (ex: G1) : ")
    df_groupe = df[df['Groupe'] == groupe]
    
    print(f"\n--- Statistiques des notes pour le groupe {groupe} ---")
    print(df_groupe[matieres].describe())
    
    comparaison = pd.DataFrame({
        "Moyenne_Groupe": df_groupe[matieres].mean(),
        "Moyenne_Promotion": df[matieres].mean()
    })
    comparaison["Ecart"] = comparaison["Moyenne_Groupe"] - comparaison["Moyenne_Promotion"]
    
    print("\n--- Comparaison Moyenne Groupe vs Promotion ---")
    print(comparaison)
else:
    print("Pas de colonne 'Groupe' détectée dans le dataset.")
