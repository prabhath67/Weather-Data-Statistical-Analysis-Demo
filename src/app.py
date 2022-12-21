
import logging

import connexion

from src.stats.data_load import load_data

SWAGGER_PATH = 'src/swagger/'
logger = logging.getLogger('app')

logger.info('Path of swagger file: {path}'.format(path=SWAGGER_PATH))
app = connexion.App(__name__, specification_dir=SWAGGER_PATH)
app.add_api('stats.yaml')
application = app.app


if __name__ == '__main__':
    load_data()
    application.run(port='3310')