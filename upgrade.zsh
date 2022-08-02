#! /usr/bin/env zsh

if [ "${#}" -gt 0 ]
then
  case ${1} in

    -r | --refresh-mirrors)
      echo "Refreshing pacman's mirrors..."
      sudo pacman-mirrors --fasttrack
      echo ""
      ;;

    -h | --help | *)
      echo ""
      echo "NAME"
      echo -e "\t${0} - A script to upgrade packages (pacman & AUR) on the system."
      echo ""
      echo "SYNOPSIS"
      echo -e "\t${0} [OPTIONS]"
      echo ""
      echo "OPTIONS"
      echo -e "\t-r | --refresh-mirrors : Refresh pacman's mirrors."
      echo ""
      echo -e "\t-h | --help : Print this help message."
      echo ""

      exit 0
      ;;

  esac
fi


echo "Upgrading pacman's packages..."
sudo pacman -Syyu
echo ""

echo "Upgrading AUR's packages..."
yay
echo ""

echo "Checking pacdiff..."
sudo pacdiff
echo ""

echo "Upgrade complete."
echo ""
