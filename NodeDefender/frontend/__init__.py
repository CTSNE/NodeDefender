import NodeDefender.frontend.views
import NodeDefender.frontend.sockets
import NodeDefender.frontend.api

logger = None

def load(app, socketio, loggHandler):
    global logger
    logger = NodeDefender.logger.getChild("Frontend")
    NodeDefender.frontend.views.load_views(app)
    NodeDefender.frontend.api.load_api(app)
    NodeDefender.frontend.sockets.load_sockets(socketio)
    logger.info("Frontend loaded")
    return True

