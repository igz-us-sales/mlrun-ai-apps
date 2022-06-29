# Local Deployment Instructions

## 0. Prerequisites
- This GitHub repo cloned to your local machine
- [docker-compose](https://docs.docker.com/compose/) installed on your local machine

## 1. Deploy via Docker Compose
To deploy this application, run the following command in the repo directory:
```bash
docker-compose up -d --build
```
This will build the image and deploy the `Streamlit` application on your local machine.

## 2. Use the Streamlit App
To use the application:
1. Navigate to http://localhost:8501 in the browser to access the app
    - *Note it may take a minute for the application to start*
2. Select the desired demo on the left sidebar
3. Adjust the sliders for submitting data
4. Press `Predict` to send the data to the model server and receive a prediction

## 3. Delete via Docker Compose
To delete this application, run the following command:
```bash
docker-compose down
```