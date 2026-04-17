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


# ------------------------------------------------------------------------ #
#                         Comprovacions ApiRest                            #
# ------------------------------------------------------------------------ #


Així mateix, farem les diferents comprovacions de cada endpoint amb el Swagger (a la carpeta test tens captures de les comprovacions). Una vegada comprovats tots els diferents endpoints, anirem al Postman i crearem una variable d'entorn amb la URL de la nostra API amb el port 8000.

Seguidament, crearem una col·lecció on provarem cada endpoint per a veure si funciona correctament i els guardarem en la col·lecció. Una vegada fet tot l'anterior, anirem als tres punts d'opcions de la col·lecció i li donarem a exportar col·lecció per a exportar-la a JSON. Com a millora de la meva API, en comptes de tenir diferents endpoints per a cada tipus de CRUD, seria tenir un mateix punt (/tasques/) i, des d'allí, gestionar els diversos mètodes per a cada operació (tasques/buscar/{id} per exemple).


<img width="270" height="230" alt="image" src="https://github.com/user-attachments/assets/8bd78527-fe06-4d84-a1b4-cdcc1510c827" />


# ------------------------------------------------------------------------ #
#                      Configuracio/Proves Fronted                         #
# ------------------------------------------------------------------------ #

Finalment, una vegada hem fet l'API correctament perquè funcioni amb l'API conjunta per a veure-la al navegador amb l'Uvicorn i l'aiofiles perquè trobi els arxius del frontend, especificant-ho abans a l'API on creem la carpeta /static, que està vinculada a la carpeta del frontend per a trobar el CSS i el JS. En aquesta part, haurem de crear el nostre propi HTML, el CSS que fa servir el Skeleton i el JS on implementem els diferents CRUD amb l'API i la connexió on fem servir diferents funcions, objectes, variables...

A més a més, en un app.get farem un punt /ver on ens buscarà l'index.html del frontend per a veure'l al nostre navegador posant http://url:8000/ver. Allí podrem veure bàsicament una pàgina senzilla que replica el Kanbanflow simplificat a "pendent" i "fet", amb una barra de cercador i alguns filtres on estan totes les funcions CRUD. Per altra banda, si aneu a la carpeta de tests, he posat un vídeo del frontend fent les diferents funcions CRUD i tinc una carpeta de documentació amb alguns apunts per a entendre de manera més fàcil el meu codi de JavaScript, amb alguna URL amb documentació a banda dels comentaris al mateix JS.

<img width="1851" height="1122" alt="image" src="https://github.com/user-attachments/assets/23501bff-92d3-4a03-b804-8df0c518dbca" />
