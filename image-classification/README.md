# Image Classification App

### Test locally

    # Build docker image, then create container
    docker build -t image-app .
    docker run -d -p 5000:5000 image-app
    
    # Send sample request
    curl -X POST -F image=@cat.jpg 'http://localhost:5000/predict'
    

    