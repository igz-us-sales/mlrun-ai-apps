#Download Python from DockerHub and use it
FROM mlrun/mlrun:1.0.2

#Set the working directory in the Docker container
WORKDIR /code

#Copy the dependencies file to the working directory
COPY requirements.txt .

#Install the dependencies
RUN pip install -r requirements.txt

#Copy the Flask app code to the working directory
COPY src/ .

#Run the container
ENTRYPOINT [ "streamlit", "run" ]
CMD [ "app.py" ]
