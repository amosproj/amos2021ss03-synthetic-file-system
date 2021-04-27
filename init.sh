if [[ ! -d metadata-hub ]] 
  then 
    git clone https://github.com/amos-project2/metadata-hub
fi

cd metadata-hub
docker pull amosproject2/metadatahub:latest
docker volume create --name metadatahub-database -d local
