# -*- coding: utf-8 -*-
from app import create_app
 
app = create_app('default')
app.run(host=app.config['HOST'],port=app.config['PORT'])