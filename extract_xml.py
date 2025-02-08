import os
import email
from email.header import decode_header
import sys
import zipfile
import gzip
import io

def save_attachments(mail_file):
    with open(mail_file, 'rb') as file:
        msg = email.message_from_binary_file(file)
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            attachment = part.get_payload(decode=True)
            if attachment is None:
                continue
            filename = part.get_filename()
            filetype = part.get_content_type()

            if filetype == 'application/gzip' or (filename is not None and filename.endswith('.gz')):
                with gzip.open(io.BytesIO(attachment), 'rb') as gz_file:
                    extracted_data = gz_file.read()
                    with open(os.path.join(os.path.dirname(mail_file), os.path.splitext(filename)[0]), 'wb') as extracted_file:
                        extracted_file.write(extracted_data)
            elif filetype == 'application/zip' or (filename is not None and filename.endswith('.zip')):
                with zipfile.ZipFile(io.BytesIO(attachment), 'r') as zip_file:
                    zip_file.extractall(os.path.dirname(mail_file))

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        mail_file = sys.argv[i]
        save_attachments(mail_file)

