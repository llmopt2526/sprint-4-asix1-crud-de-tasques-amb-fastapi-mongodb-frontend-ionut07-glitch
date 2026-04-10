[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ULL36zWV)
### Estructura del projecte

A diferència d’altres projectes més complexos, en aquest cas **treballareu amb una estructura simple**, igual que a l’exemple oficial. Tot el backend s’ubica en un únic fitxer (`app.py`), amb l’objectiu de centrar-se en **aprendre CRUD amb FastAPI i MongoDB** abans de **modularitzar el codi**.

El projecte ha de mantenir una **estructura com aquesta**:

```
project/
├── README.md
├── backend/                # FastAPI + MongoDB
│   ├── app.py              # Fitxer principal (tota la lògica)
│   └── requirements.txt    # Dependències
│
├── frontend/           # Interfície web
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── tests/              # Tests amb Postman
    └── Postman_API_tests.json
```


# ------------------------------------------------------------------------ #
#                         Instalació/Configuració ApiRest                  #
# ------------------------------------------------------------------------ #

Primerament, haurem de fer un git clone a la nostra màquina real del projecte del Sprint4. Una vegada dins, haurem de crear un entorn virtual amb la comanda python3 -m venv venv i source venv/bin/activate per a executar l'entorn virtual de Python. Una vegada dins, haurem d'anar a la carpeta de backend i instal·lar el requirements.txt, però en el meu cas he afegit fastapi==0.104.1, uvicorn[standard]==0.24.0 i pymongo==4.6.0, on fem servir la FastAPI i PyMongo per a configurar i crear la nostra API. Així mateix, fem servir l'Uvicorn per a desplegar la nostra API de manera molt més còmoda i rapida per a fer les nostres comporvacions amb el psotman i el fronted.

<img width="807" height="447" alt="Captura desde 2026-04-09 10-36-20" src="https://github.com/user-attachments/assets/a5ff79bf-5feb-4344-9e91-1b57ff4173dc" />

Seguidament, antes de començar haurem d'anar al nsotre mongodb atlas en el compas on haurem de elegir entre els 5 ejemples de base de dades per a este projecte, en el meu cas he elegit el de gestor de tasques. A més a més, he anat al geminis i li he pasat l'exemple del document del gestor de tasques per  a que hem faigue 30 registros per a un arxiu de json per a després importalo al meu mongodb. He creat el arxiu import.json i l'he importat al meu mongodb atlas en una nova base de dades anomenada Sprint4 i en la colleció GestorDeTasques.

<img width="1106" height="719" alt="Captura desde 2026-04-09 11-38-33" src="https://github.com/user-attachments/assets/349c1513-e5f0-42a3-ba39-898669ed27e0" />

Per altra banda, haurem de tornar a la carpeta del backend, on haurem de modificar el arxiu app.py modificant l'apartat de la conexió de MongoDB atlas haurem de cambiar l'informació del Mongodb_url, el nom de la base de dades per la nostra i la colleció on tenim el gestor de tasques. A més a més haurem de cambiar el pydantic, on haurem de configurar el format del document de la nostra colleció de Gestero de tasques i un exemple. Per ultim, configurarem el @app-get /ver per a tenir ja preparada la part del fronted en la configuració del nostre app.py i definirem diferents endpoints (/, /tasques, /buscar/{titol}, /buscar/{id_tasca}, /crear, /actualitzar/{id_tasca} i /borrar/{id_tasca}). Una vegada fet aixo, haurem de ficar la seguent comanda uvicorn main:app --host 192.168.221.0 --port 8000 --reload per a desplegar la nostra api i poder veurela en un navegador.

<img width="1402" height="674" alt="Captura desde 2026-04-09 12-54-21" src="https://github.com/user-attachments/assets/925c037a-169e-4ca4-bafc-8c5d1fc2ac6e" />




