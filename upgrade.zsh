#! /usr/bin/env zsh

if [ "${#}" -gt 0 ]
then
  case ${1} in

    -r | --refresh-mirrors)
      echo ""
      echo "Refreshing pacman's mirrors..."
      echo ""
      sudo pacman-mirrors --fasttrack
      echo ""
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


echo ""
echo "Upgrading pacman's packages..."
echo ""
sudo pacman -Syyu
echo ""
echo ""

echo ""
echo "Upgrading AUR's packages..."
echo ""
yay
echo ""
echo ""

echo ""
echo "Checking pacdiff..."
echo ""
sudo pacdiff
echo ""
echo ""

echo ""
echo "Upgrade complete."
echo ""
echo ""
