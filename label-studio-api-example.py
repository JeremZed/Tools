# SCript pour labeliser en masse des images via l'api
# Define the URL where Label Studio is accessible and the API key for your user account
LABEL_STUDIO_URL = 'http://localhost:55000'
API_KEY = 'xxxxxxxxxxxx'

# Import the SDK and the client module
from label_studio_sdk.client import LabelStudio
from label_studio_sdk.data_manager import Filters, Column, Type, Operator
import json



# Connect to the Label Studio API and check the connection
ls = LabelStudio(base_url=LABEL_STUDIO_URL, api_key=API_KEY)

# Récupération d'un projet
project = ls.projects.get(id=1)

# Récupération la vue / onglet (avec filtre)
tab = ls.views.get(id=7)

# Récupération des tâches d'un projet et d'une vue
tasks = ls.tasks.list(project=project.id, view=tab.id, page_size=10000)
print(f"avant : {len(tasks.items)} ")

# Pour chaque tâche on affecte un classe "Courge Amère"
for task in tasks:
    ls.annotations.create( id=task.id, result=[
        {
            "value": {
                "choices": [
                    "Courge Amère"
                ]
            },
            "from_name": "choice",
            "to_name": "image",
            "type": "choices",
        }
    ])

tasks = ls.tasks.list(project=project.id, view=tab.id, page_size=10000)

print(f"après : {len(tasks.items)} ")