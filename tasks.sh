#!/bin/zsh

# the way to call them is as follows:
# source tasks.sh;
# then any one of this functions

export DB_PORT=5432
export PG_USER=postgres

function app_run(){
    docker-compose run hermes $1
}

function task_up(){
  docker-compose up
}

function task_down(){
  docker-compose down
}

function db_shell(){
    docker-compose run db psql -h db -p$DB_PORT -U $PG_USER 
}

function task_db_create(){
    docker-compose run db psql -h db -p$DB_PORT -U $PG_USER -c "CREATE DATABASE hermes;"
    docker-compose run db psql -h db -p$DB_PORT -U $PG_USER -c "CREATE DATABASE celery;"
}

function db_migrate(){
    app_run "alembic upgrade head"
}


function console(){
    app_run bash
}

function create_migration(){
    app_run "alembic revision --autogenerate"
}


