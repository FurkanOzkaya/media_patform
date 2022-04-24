python manage.py makemigrations --noinput
python manage.py migrate
echo "Generating Admin User" 
python manage.py  create_admin
python manage.py runserver 0.0.0.0:8000