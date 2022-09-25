#! /usr/bin/env zsh

set -e

echo "Sourcing environment variables..."
set -a
source "${0:a:h}/.env"
set +a

[ -z "${BACKUP_GPG_ENCRYPTION_PASSPHRASE}" ] && echo "The BACKUP_GPG_ENCRYPTION_PASSPHRASE variable should be set." && exit 1

TEMPORARY_WORKING_DIRECTORY="$(mktemp -d)"

echo "Going into ${TEMPORARY_WORKING_DIRECTORY}..."
pushd "${TEMPORARY_WORKING_DIRECTORY}"

PASSWORD_STORE_PATH="${HOME}/.password-store"
PASSWORDS_BACKUP_FILE="passwords.txt"

echo "Decrypting passwords..."
for ENCRYPTED_PASSWORD_FILE in "${PASSWORD_STORE_PATH}"/**/*.gpg
do
  PASSWORD_PATH="$(echo "${ENCRYPTED_PASSWORD_FILE}" | sed --expression "s#${PASSWORD_STORE_PATH}/##g" --expression 's#\.gpg##g')"

  echo "${PASSWORD_PATH} $(pass "${PASSWORD_PATH}")" >> ${PASSWORDS_BACKUP_FILE}
done

BACKUP_FILE="$(date '+%Y-%m-%d.%s').tar.bz2"

echo "Backing up files:"
tar --dereference --create --verbose --bzip2 --exclude '.directory' --file "${BACKUP_FILE}" ${PASSWORDS_BACKUP_FILE} --directory "${HOME}" Documents Pictures

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
