# Tweet Sight

docker build --progress=plain --no-cache --tag tweet_sight:latest .

docker run --name twitter_sight -d -p 8000:8000 twitter_sight:latest
