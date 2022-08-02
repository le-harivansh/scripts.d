#! /usr/bin/env zsh

case ${1} in

  purge)
    echo "Stopping all containers..."

    if [ "$(docker container list --quiet)" ]
    then
      docker container kill $(docker container list --quiet)
      echo ""
    fi


    echo "Removing all containers..."

    if [ "$(docker container list --all --quiet)" ]
    then
      docker container rm --force --volumes $(docker container list --all --quiet)
      echo ""
    fi

    echo "Removing all images..."

    if [ "$(docker image list --all --quiet)" ]
    then
      docker image rm --force $(docker image list --all --quiet)
      echo ""
    fi

    echo "Removing all volumes..."

    if [ "$(docker volume list --quiet)" ]
    then
      docker volume rm --force $(docker volume list --quiet)
      echo ""
    fi

    echo "Removing all networks..."

    if [ "$(docker network list --quiet)" ]
    then
      docker network rm $(docker network list --quiet)
      echo ""
    fi

    echo "Docker cleanup complete."
    echo ""
    ;;

  list)
    echo "*** CONTAINERS ***"
    docker container list --all
    echo ""

    echo "*** IMAGES ***"
    docker image list --all
    echo ""

    echo "*** VOLUMES ***"
    docker volume list
    echo ""

    echo "*** NETWORKS ***"
    docker network list
    echo ""
    ;;

  *)
    echo ""
    echo "NAME"
    echo -e "\t${0} - A set of utilities to clean up docker."
    echo ""
    echo "SYNOPSIS"
    echo -e "\t${0} COMMAND"
    echo ""
    echo "COMMANDS"
    echo -e "\tpurge : Removes all docker containers, images, volumes, and networks."
    echo ""
    echo -e "\tlist  : List all docker containers, images, volumes, and networks to remove."
    echo ""
    ;;

esac
