#! /usr/bin/env bash

set -e

echo "Sourcing environment variables..."
set -a
source "$(dirname -- "${0}")/.env"
set +a

[ -z "${BACKUP_GPG_ENCRYPTION_PASSPHRASE}" ] && echo "The BACKUP_GPG_ENCRYPTION_PASSPHRASE variable should be set." && exit 1

TEMPORARY_WORKING_DIRECTORY="$(mktemp --directory --tmpdir="/tmp")"

echo "Going into ${TEMPORARY_WORKING_DIRECTORY}..."
pushd "${TEMPORARY_WORKING_DIRECTORY}"

PASSWORD_STORE_PATH="${HOME}/.password-store"
PASSWORDS_BACKUP_FILE="passwords.txt"

echo "Decrypting passwords..."
shopt -s globstar # enable globstar
for ENCRYPTED_PASSWORD_FILE in "${PASSWORD_STORE_PATH}"/**/*.gpg
do
  PASSWORD_PATH="$(echo "${ENCRYPTED_PASSWORD_FILE}" | sed -e "s#${PASSWORD_STORE_PATH}/##g" -e 's#\.gpg##g')"

  echo "${PASSWORD_PATH} $(pass "${PASSWORD_PATH}")" >> ${PASSWORDS_BACKUP_FILE}
done
shopt -u globstar # disable globstar

BACKUP_FILE="$(date '+%Y-%m-%d.%s').tar.bz2"

echo "Backing up files:"
tar --dereference --create --verbose --bzip2 --file "${BACKUP_FILE}" ${PASSWORDS_BACKUP_FILE} "${HOME}"/Documents "${HOME}"/Pictures

echo "Encrypting backup file..."
gpg --sign --symmetric --no-symkey-cache --batch --pinentry-mode loopback --passphrase "${BACKUP_GPG_ENCRYPTION_PASSPHRASE}" "${BACKUP_FILE}"

ENCRYPTED_BACKUP_FILE="${BACKUP_FILE}.gpg"

echo "Going back to the previous working directory..."
popd

echo "Moving ${TEMPORARY_WORKING_DIRECTORY}/${ENCRYPTED_BACKUP_FILE} to $(pwd)..."
mv "${TEMPORARY_WORKING_DIRECTORY}/${ENCRYPTED_BACKUP_FILE}" .

echo "Cleaning up..."
rm -rf "${TEMPORARY_WORKING_DIRECTORY}"

echo "Backup complete."
