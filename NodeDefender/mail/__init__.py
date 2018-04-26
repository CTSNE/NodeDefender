from flask_mail import Mail
import NodeDefender
import NodeDefender.mail.decorators
import NodeDefender.mail.user
import NodeDefender.mail.group
import NodeDefender.mail.node
import NodeDefender.mail.icpe

logger = None
enabled = False

mail = Mail()

def load(app, loggHandler):
    global enabled
    global logger
    logger = NodeDefender.logger.getChild("mail")
    mail.init_app(app)
    enabled = NodeDefender.config.mail.enabled()
    logger.info("Mail Service Enabled")
    return True

