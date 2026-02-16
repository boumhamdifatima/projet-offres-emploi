import pandas as pd
import os

def generate_html(csv_path, output_path):
    if not os.path.exists(csv_path):
        print(f"Erreur : {csv_path} introuvable.")
        return False

    # Lecture des données
    df = pd.read_csv(csv_path)

    # Création du HTML avec un style CSS minimaliste (Table responsive)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Veille Offres d'Emploi</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }}
            table {{ width: 100%; border-collapse: collapse; background: white; }}
            th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
            th {{ background-color: #007bff; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
            .container {{ max-width: 1000px; margin: auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Dernières Offres d'Emploi Logiciel</h1>
            <table>
                <thead>
                    <tr>
                        <th>Titre</th>
                        <th>Entreprise</th>
                        <th>Source</th>
                        <th>Lien</th>
                    </tr>
                </thead>
                <tbody>
    """

    for _, row in df.iterrows():
        html_content += f"""
                    <tr>
                        <td>{row['Titre']}</td>
                        <td>{row['Entreprise']}</td>
                        <td>{row['Source']}</td>
                        <td><a href="{row['Lien']}" target="_blank">Voir l'offre</a></td>
                    </tr>
        """

    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    # Création du dossier public s'il n'existe pas
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Rapport HTML généré : {output_path}")
    return True

if __name__ == "__main__":
    generate_html('data/jobs.csv', 'public/index.html')