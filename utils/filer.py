import os


def save_file(file, save_path):
    destination = open(os.path.join(save_path, file.name), 'wb+')
    for chunk in destination:
        destination.write(chunk)
    destination.close()
