export DATABASE_URL='postgres://pctnetuser:tTdkrHSzijCw4JjepJ4u@localhost:5432/pctnet'
if [ $1 = 'coverage' ]; then
	coverage run manage.py test
	coverage run --append -m pytest
	coverage report
else
	python manage.py "$@"
fi;
