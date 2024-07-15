Bonds App API

Run App localy:
 - clone repository
 - go to the repository dir (bonds_app)
 - create new conda env with python
   cmd: conda create -n <env_name> python=3.10
 - activate conda env
   cmd: conda activate <env_name>
 - install reqirements
   cmd: pip install -r requirements.txt
 - run django server
   cmd: python manage.py runserver

Ceate docker image and run App in docker container:
  - clone repository
  - go to the repository dir (bonds_app)
  - create image
    cmd: docker-compose build
  - run image
    cmd: docker-compose up

Bonds App API is avaiable on http://127.0.0.1:8000/
  - swagger/     location of API documentation
  - admin/       location of adinistrator entry point
  - bondposts/   location of API entry point
      - view/                   List all bonds.
      - insert/                 Create a new bond instance. Bond is validade by its ISIN.
      - 'manage/<str:isin>/'    Retrieve, update, or delete a bond instance.
      - stat/                   Calculate statistic of whole set of bonds.

