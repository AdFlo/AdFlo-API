# AdFlo-API

# Activate environment
    virtualenv -p /usr/bin/python2.7 venv
    source venv/bin/activate

# Deactivate environment 
    deactivate

# Install package
    pip install package_name && pip freeze > requirements.txt

# Start mongodb on port 27017
    mongod
<!-- # Boto config ( stored in ~/.aws/credentials )
    [default]
    aws_access_key_id = 123example
    aws_secret_access_key = 123example
 -->