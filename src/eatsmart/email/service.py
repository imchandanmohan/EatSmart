import os
import mimetypes
import smtplib
from typing import List, Optional, Tuple

from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

from config.settings import get_settings


def _build_message(
    subject: str,
    body: str,
    recipients: List[str],
    subtype: str = "html",
) -> MIMEMultipart:
    message = MIMEMultipart()
    message["Subject"] = subject
    settings = get_settings()
    from_email = settings.email.username or "no-reply@eatsmart.local"
    from_name = settings.email.from_name or "EatSmart Assistant"
    message["From"] = f"{from_name} <{from_email}>"
    message["To"] = ", ".join(recipients)

    message.attach(MIMEText(body, subtype))
    return message


def _attach_file(message: MIMEMultipart, filename: str, filepath: str) -> None:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Attachment not found: {filepath}")

    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    with open(filepath, "rb") as f:
        file_data = f.read()

    if maintype == "image":
        part = MIMEImage(file_data, _subtype=subtype, name=filename)
    else:
        part = MIMEApplication(file_data, _subtype=subtype, Name=filename)
        part.add_header("Content-Disposition", "attachment", filename=filename)

    message.attach(part)


def _send_via_smtp(message: MIMEMultipart, recipients: List[str]) -> None:
    settings = get_settings()
    server = settings.email.smtp_server
    port = settings.email.smtp_port
    use_tls = settings.email.smtp_use_tls
    username = settings.email.username
    password = settings.email.password

    with smtplib.SMTP(server, port) as smtp:
        smtp.ehlo()
        if use_tls:
            smtp.starttls()
            smtp.ehlo()
        if username and password:
            smtp.login(username, password)
        smtp.sendmail(message["From"], recipients, message.as_string())


def send_email(
    subject: str,
    body: str,
    to: List[str],
    attachments: Optional[List[Tuple[str, str]]] = None,
) -> None:
    message = _build_message(subject, body, to)
    if attachments:
        for filename, filepath in attachments:
            _attach_file(message, filename, filepath)
    _send_via_smtp(message, to)


def send_email_with_attachments(
    subject: str,
    body: str,
    to: List[str],
    attachments: List[Tuple[str, str]],
) -> None:
    send_email(subject, body, to, attachments=attachments)


def send_email_with_image(subject: str, body: str, to: List[str], image: str) -> None:
    filename = os.path.basename(image)
    send_email(subject, body, to, attachments=[(filename, image)])


def send_email_with_pdf(subject: str, body: str, to: List[str], pdf: str) -> None:
    filename = os.path.basename(pdf)
    send_email(subject, body, to, attachments=[(filename, pdf)])


def send_email_with_excel(subject: str, body: str, to: List[str], excel: str) -> None:
    filename = os.path.basename(excel)
    send_email(subject, body, to, attachments=[(filename, excel)])