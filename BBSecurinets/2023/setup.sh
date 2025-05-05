sudo yum update
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo docker run hello-world
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
sudo systemctl start docker.service
