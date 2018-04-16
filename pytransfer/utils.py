from .services import TransferSh


def upload_file(file):
    service_provider = TransferSh(file['path'], file['order'])
    link = service_provider.upload_file()

    service_provider.progressbar.finish(link)
