
import logging

import connexion

SWAGGER_PATH = ''
logger = logging.getLogger('app')

logger.info('Path of swagger file: {path}'.format(path=SWAGGER_PATH))
app = connexion.App(__name__, specification_dir=SWAGGER_PATH)
app.add_api('employee.yaml')
application = app.app


if __name__ == '__main__':
    application.run(port='3310')