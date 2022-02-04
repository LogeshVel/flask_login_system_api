# SQL_over_HTTPS_base_API


To create the requirements.txt file on windows

    py -m pip install pipreqs
    
    py -m pipreqs.pipreqs

For Heroku deployment

Prepare the Procfile
    
    web: gunicorn <file_name>:<flask_app_name>