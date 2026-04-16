#!/usr/bin/env bash
set -o errexit

# 1. Instalar dependencias de Python
pip install -r requirements.txt

# 2. Construir los estilos de Tailwind
python manage.py tailwind install
python manage.py tailwind build

# 3. Recolectar estáticos
python manage.py collectstatic --noinput

# 4. Migrar la base de datos
python manage.py migrate