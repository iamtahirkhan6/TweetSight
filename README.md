# Tweet Sight

docker build --progress=plain --no-cache --tag tweet_sight:latest .

docker run --name tweet_sight -d -p 8000:8000 tweet_sight:latest
