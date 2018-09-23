# -*- coding: utf-8 -*-
from app import create_app
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


app = create_app('default')


if __name__ == '__main__':
	app.run(host=app.config['HOST'],port=app.config['PORT'])