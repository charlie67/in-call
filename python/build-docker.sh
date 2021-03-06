cd $TRAVIS_BUILD_DIR/python
docker build . -t $DOCKER_USERNAME/in-call-python:$TRAVIS_BRANCH
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push $DOCKER_USERNAME/in-call-python:$TRAVIS_BRANCH
