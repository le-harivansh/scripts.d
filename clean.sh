#! /usr/bin/env bash

set -e

# Bleachbit
echo "Cleaning the system-space using bleachbit..."
sudo bleachbit --clean "$(bleachbit --list-cleaners | sed --expression '/system\.memory/d' --expression '/system\.free_disk_space/d')"
echo ""

echo "Cleaning the user-space using bleachbit..."
bleachbit --clean "$(bleachbit --list-cleaners | sed --expression '/system\.memory/d' --expression '/system\.free_disk_space/d')"
echo ""

# System
echo "Cleaning journalctl..."
sudo journalctl --vacuum-time=30days --vacuum-size=50M
echo ""

# Pacman
echo "Removing orphan packages..."
sudo pacman --remove --nosave --recursive "$(pacman --query --unrequired --deps --quiet)"
echo ""

echo "Clearing pacman's cache..."
sudo pacman --sync --clean --clean
echo ""

# Docker
echo "Cleaning docker..."
echo "Stopping all docker containers..."
if [ "$(docker container list --quiet)" ]
then
  docker container kill "$(docker container list --quiet)"
fi
echo ""

echo "Removing all docker containers..."
if [ "$(docker container list --all --quiet)" ]
then
  docker container rm --force --volumes "$(docker container list --all --quiet)"
fi
echo ""

echo "Removing all docker images..."
if [ "$(docker image list --all --quiet)" ]
then
  docker image rm --force "$(docker image list --all --quiet)"
fi
echo ""

echo "Removing all docker volumes..."
if [ "$(docker volume list --quiet)" ]
then
  docker volume rm --force "$(docker volume list --quiet)"
fi
echo ""

echo "Removing all docker networks..."
for docker_network in $(docker network list --format '{{.Name}}')
do
  [ "${docker_network}" != 'host' ] && [ "${docker_network}" != 'bridge' ] && [ "${docker_network}" != 'none' ] && docker network rm "${docker_network}"
done
echo ""
echo "Docker cleanup complete."

echo "Cleanup complete."
