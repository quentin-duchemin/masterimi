my3a.enpc.org
=============

## Production
```bash
docker-compose pull
docker-compose up -d
./tools/load_fixtures.sh
docker-compose exec back /venv/bin/python manage.py createsuperuser --username louis.trezzini --email louis.trezzini@eleves.enpc.fr --noinput
docker-compose exec back /venv/bin/python manage.py createsuperuser --username clement.riu --email clement.riu@eleves.enpc.fr --noinput
docker-compose exec back /venv/bin/python manage.py createsuperuser --username sandrine.guillerm --email sandrine.guillerm@enpc.fr --noinput
```

## Development
```bash
# Installation du front
cd front/
npm install

# Lancement via docker
cd ../
python -c 'import os; print("SECRET_KEY=" + os.urandom(16).hex())' >  .env
sudo docker-compose -f docker-compose.yml -f dev.override.yml up --build

# Ajouter à /etc/hosts
127.0.0.1 my3a-dev.enpc.org
```

Se rendre sur http://my3a-dev.enpc.org:4200/
