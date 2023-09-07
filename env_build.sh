rm -f django_demo/.env
touch django_demo/.env
echo ENV=$ENV >> django_demo/.env
echo DEBUG=$DEBUG >> django_demo/.env
echo DB_NAME=$DB_NAME >> django_demo/.env
echo DB_USER=$DB_USER >> django_demo/.env
echo DB_PASSWORD=$DB_PASSWORD >> django_demo/.env
echo DB_HOST=$DB_HOST >> django_demo/.env
echo DB_PORT=$DB_PORT >> django_demo/.env
echo SECRET_KEY=$SECRET_KEY >> django_demo/.env