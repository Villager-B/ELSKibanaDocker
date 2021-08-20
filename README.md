# ELS_Kibana_Docker

ElasticSearch(+ Sudachi:full) + Kibanaの環境をDockerで立ち上げる．

また，オプションとしてTwitterでいいねしたツイートをELSに投入するまでのコードも用意している．

## Eenvironment

- Elastic Search 7.10.1
- Kibana 7.10.1
- sudachi
  - plugin:analysis-sudachi-7.10.1-2.1.0
  - sudachi-dictionary-20210802-core
  - sudachi-dictionary-20210802-full

## How to Use

1. `docker network create elastic`
2. `docker-compose build`
3. `docker-compose up`
   1. or `docker-compose up -d`

## Option

```
1. create config.py
  1.1 input twitter-api keys
2. tweet_collect.py
3. data_to_els.py
```