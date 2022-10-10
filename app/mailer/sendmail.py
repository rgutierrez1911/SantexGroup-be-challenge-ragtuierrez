from typing import List
import smtplib, ssl
# from db_orm_models.data.usuarios import Usuario
from core.config import MAIL_SERVER, MAIL_PORT, IS_SERVER_DUMMY, MAIL_USER, MAIL_PWD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment,FileSystemLoader


def send_mail_notification(template: str,
                           args: dict,
                           target_users: list =[],
                           mails :List[str] =[],
                           from_mail :str= "notification_service@admin.com",
                           subject :str= ""):
    to = mails if mails else [user.mail for user in target_users]
    
    sendmail_base(from_mail=from_mail,
                  to=to,
                  template=template,
                  subject=subject,
                  args_template=args)
    
    
def sendmail_base(
    from_mail: str = "rodrigoga_799@outlook.com",
    to: str = "apizarro@entel.com.pe",
    message: str = "",
    template: str = "",
    args_template: dict = "",
    subject = ""
    ):

    context = ssl.create_default_context()
    try:

        if type(to) == list:
            to = ", ".join(list(set(to)))
            
            

        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.ehlo()

        if not bool(IS_SERVER_DUMMY):
            server.starttls(context=context)

        server.ehlo()
        server.login(MAIL_USER, MAIL_PWD)


        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_mail
        message["To"] = to

        

        if template != "":
            rendered = render_html(
                    template_file=template,
                    args=args_template)
            part = MIMEText(rendered, "html")
            message.attach(part)
            server.sendmail(from_mail, to, message.as_string())
        else:  
            server.sendmail(from_mail, to, message)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print ("#"*50) 
    finally:
        server.quit()
        

def render_html(template_file: str, args: dict) -> str:
    
    file_loader = FileSystemLoader(searchpath= f"app/templates/")
    
    enviroment = Environment(loader=file_loader)
    template = enviroment.get_template(template_file)

    
    return template.render(**args)
