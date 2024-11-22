This application is hosted on Google Cloud Platform, which implements inserting values into database and fetching all the values from the database. This application is also used to upload the files to the Storage bucket.

The project structure goes as follows:
GCP_Application

frontend: index.html, script.js, config-map.yaml, Dockerfile

backend: app.py, requirements.txt, secrets.yaml, gcp_credentials.json  # Google Cloud service account credentials file, Dockerfile

docker-compose.yaml

README.md

## Frontend

The frontend is a simple static website that communicates with the backend for data operations. It consists of the following files:

- **index.html**: The main HTML file for the UI.
- **script.js**: A JavaScript file that handles frontend logic, including making fetch() requests to the backend.
- **config-map.yaml**: The ConfigMap file is used for configuring the environment, such as setting the backend API URL dynamically.
- **Dockerfile**: The Dockerfile to build and containerize the frontend service.
The Dockerfile for the frontend creates a container to serve the static assets.

The config-map.yaml file is used to store and manage configuration details for the frontend, like the backend service URL.
##Backend
The backend is a Python Flask application that provides a REST API for frontend interaction and integrates with Google Cloud services.

app.py: The main Flask application that contains routes for handling requests such as /insert, /fetch, /upload.
requirements.txt: List of dependencies for the Flask app (e.g., Flask, pyodbc, google-cloud-storage).
secrets.yaml: A YAML file that holds sensitive data like database credentials.
gcp_credentials.json: The service account key file for authenticating with Google Cloud.
Dockerfile: The Dockerfile to build and containerize the backend service.

##Docker Compose
The docker-compose.yaml file orchestrates both the frontend and backend services, allowing them to run together using a network.

To run the application locally:
Clone the repository:
git clone https://github.com/ShravyaPanumati/GCP_Application.git
Navigate to the project directory:
cd my-project
Build and run the containers using Docker Compose:
''''
docker-compose up --build
''''
This will start both the frontend and backend containers. You can access the frontend by navigating to http://localhost:8080 in your web browser. The backend will be running on http://localhost:5000.

Running the application in Google Cloud Platform
create clusters for frontend/backend: 
gcloud container clusters create my-cluster \
    --zone us-central1-a\
    --num-nodes 2

Set the context for the cluster:
gcloud container clusters get-credentials my-cluster --zone us-central1-a

Install "kompose"
check whether it is installed "kompose --version"
Paste the docker-compose.yaml and reuse the images which has been built locally and uploaded to GCR using docker.
Command: kompose convert
This will generate a series of Kubernetes YAML files (like Deployment, Service, etc.) for both your frontend and backend services. These files will be named something like frontend-service.yaml, frontend-deployment.yaml, backend-service.yaml, and backend-deployment.yaml.
kubectl apply -f . will deploy all the services to GKE.

kubectl get services- This will show the services running and the external IP associated with it.

Access the application using http://ExternalIP:8080

The testing of the application can be performed by accessing the link and also using postman with their endpoints.
The output UI page is as follows:
![image](https://github.com/user-attachments/assets/43eead17-471b-4504-b412-6ff71d6536f2)
