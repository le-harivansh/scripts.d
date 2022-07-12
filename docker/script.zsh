#! /usr/bin/env zsh

case ${1} in
  purge)
    echo ""
    echo "Stopping all containers..."

    if [ "$(docker container list --quiet)" ]
    then
      echo ""
      docker container kill $(docker container list --quiet)
      echo ""
      echo ""
    fi


    echo ""
    echo "Removing all containers..."

    if [ "$(docker container list --all --quiet)" ]
    then
      echo ""
      docker container rm --force --volumes $(docker container list --all --quiet)
      echo ""
      echo ""
    fi

    echo ""
    echo "Removing all images..."

    if [ "$(docker image list --all --quiet)" ]
    then
      echo ""
      docker image rm --force $(docker image list --all --quiet)
      echo ""
      echo ""
    fi

    echo ""
    echo "Removing all volumes..."

    if [ "$(docker volume list --quiet)" ]
    then
      echo ""
      docker volume rm --force $(docker volume list --quiet)
      echo ""
      echo ""
    fi

    echo ""
    echo "Removing all networks..."

    if [ "$(docker network list --quiet)" ]
    then
      echo ""
      docker network rm $(docker network list --quiet)
      echo ""
      echo ""
    fi
    ;;

  list)
    echo ""
    echo "*** CONTAINERS ***"
    echo ""
    docker container list --all
    echo ""
    echo ""

    echo ""
    echo "*** IMAGES ***"
    echo ""
    docker image list --all
    echo ""
    echo ""

    echo ""
    echo "*** VOLUMES ***"
    echo ""
    docker volume list
    echo ""
    echo ""

    echo ""
    echo "*** NETWORKS ***"
    echo ""
    docker network list
    echo ""
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
