from cryptography.fernet import Fernet

key = "7LBG7bqMkRqedGjS3h717rgono_TlKbRaxZVBzGCZXM="

ekey_log = "ekey_log.txt"
esys_info = "esys_info.txt"
eclip_info = "eclip_info.txt"

encrypted = [ekey_log, esys_info, eclip_info]
fileCount = 0

for decrypted in encrypted:
    with open(decrypted[fileCount], 'rb') as file:
        data = file.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted[fileCount], 'wb') as file:
        file.write(decrypted)

    fileCount += 1