#! /usr/bin/env zsh

if [ "${#}" -gt 0 ]
then
  case ${1} in

    -h | --help | *)
      echo ""
      echo "NAME"
      echo -e "\t${0} - A script to clean the system."
      echo ""
      echo "SYNOPSIS"
      echo -e "\t${0} [OPTIONS]"
      echo ""
      echo "OPTIONS"
      echo -e "\t-h | --help : Print this help message."
      echo ""

      exit 0
      ;;

  esac
fi

# cleaning script start...
echo 'clean'
