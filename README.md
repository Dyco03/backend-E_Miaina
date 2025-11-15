# Eaina Backend API

Backend complet pour l'application Eaina, une application de savoir-vivre à Madagascar.

## Structure du projet

Le projet suit une architecture organisée et claire :

```
back_eaina/
├── app/
│   ├── main.py              # Point d'entrée de l'application
│   ├── db/
│   │   ├── database.py      # Configuration de la base de données
│   │   └── models/          # Modèles SQLAlchemy
│   │       ├── users.py
│   │       ├── challenges.py
│   │       ├── community.py
│   │       └── chatbot.py
│   ├── schemas/             # Schémas Pydantic pour validation
│   │   ├── users.py
│   │   ├── challenges.py
│   │   ├── community.py
│   │   └── chatbot.py
│   ├── crud/                # Opérations CRUD
│   │   ├── users.py
│   │   ├── challenges.py
│   │   ├── community.py
│   │   └── chatbot.py
│   ├── routers/             # Routes API
│   │   ├── users.py
│   │   ├── challenges.py
│   │   ├── community.py
│   │   └── chatbot.py
│   └── utils/               # Utilitaires
│       ├── security.py      # Hachage de mots de passe et JWT
│       ├── auth.py          # Authentification
│       └── helpers.py       # Fonctions helper
├── requirements.txt
└── README.md
```

## Installation

1. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
Créer un fichier `.env` à la racine avec :
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/e_aina
SECRET_KEY=your-secret-key-here
```

4. Démarrer le serveur :
```bash
python app/main.py
```

L'API sera accessible sur `http://127.0.0.1:8000`

## Documentation API

Une fois le serveur démarré, la documentation interactive est disponible sur :
- Swagger UI : `http://127.0.0.1:8000/docs`
- ReDoc : `http://127.0.0.1:8000/redoc`

## Endpoints principaux

### variable .env
-dans app creer un .env et ajoute :
   BACKEND_URL = ... ton url mysql ex : mysql+pymysql://user:mdp@ip:port/bd
   SECRET_KEY = ... le secret key pour jwt
### Authentification (`/users`)

- `POST /users/register` - Créer un nouveau compte
- `POST /users/login` - Se connecter et obtenir un token JWT
- `GET /users/me` - Obtenir les informations de l'utilisateur connecté
- `PUT /users/me` - Mettre à jour le profil
- `POST /users/reset-password` - Demander une réinitialisation de mot de passe

### Challenges (`/challenges`)

- `GET /challenges/` - Obtenir tous les challenges avec statut de complétion
- `GET /challenges/daily` - Obtenir le challenge du jour
- `GET /challenges/{challenge_id}` - Obtenir un challenge spécifique
- `POST /challenges/{challenge_id}/complete` - Compléter un challenge
- `GET /challenges/completed/all` - Obtenir tous les challenges complétés
- `GET /challenges/points/total` - Obtenir le total de points

### Communauté (`/community`)

- `GET /community/discussions` - Obtenir toutes les discussions
- `GET /community/discussions/{discussion_id}` - Obtenir une discussion avec ses commentaires
- `POST /community/discussions` - Créer une nouvelle discussion
- `POST /community/comments` - Ajouter un commentaire
- `GET /community/discussions/{discussion_id}/comments` - Obtenir les commentaires d'une discussion

### Chatbot (`/chatbot`)

- `GET /chatbot/messages` - Obtenir l'historique des messages
- `POST /chatbot/messages` - Envoyer un message au chatbot

## Authentification

La plupart des endpoints nécessitent une authentification JWT. Pour utiliser ces endpoints :

1. Se connecter via `POST /users/login` pour obtenir un token
2. Inclure le token dans les headers : `Authorization: Bearer <token>`

## Base de données

Le backend utilise MySQL avec SQLAlchemy. Les tables sont créées automatiquement au démarrage de l'application.

### Modèles principaux

- **User** : Utilisateurs avec profil complet
- **Challenge** : Défis de savoir-vivre
- **UserChallenge** : Relation many-to-many pour suivre les challenges complétés
- **Discussion** : Discussions de la communauté
- **Comment** : Commentaires sur les discussions
- **ChatMessage** : Messages du chatbot

## Notes

- Le système de points est automatiquement mis à jour lorsqu'un challenge est complété
- Les noms d'auteurs sont générés automatiquement à partir des informations utilisateur
- CORS est configuré pour permettre les requêtes depuis le frontend

