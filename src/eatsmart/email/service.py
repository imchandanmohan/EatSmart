import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.application import MIMEApplication


def send_email(subject: str, body: str, to: list[str], attachments: list[tuple[str, str]] = None):
    pass