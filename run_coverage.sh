echo Test Started
coverage run manage.py test .

echo REPORT
coverage report -m