# base image  
FROM python:3.11.2

# set work directory  
WORKDIR /home/app/webapp

# install dependencies  
COPY requirements.txt /home/app/webapp/  
RUN pip install --upgrade pip && pip install -r requirements.txt  

# copy whole project to your docker home directory. 
COPY . /home/app/webapp/  

# port where the Django app runs  
EXPOSE 8000  

# start server  
RUN python manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]