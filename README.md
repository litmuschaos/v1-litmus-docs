Documentation for the Litmus Project

Additional details on the Docusaurus project can be found [here](https://docusaurus.io/docs/en/installation.html).

## For Developers

### Clone litmus-docs repository

```bash
git clone https://github.com/litmuschaos/litmus-docs.git
cd litmus-docs
```

The website server can be setup manually or through docker and docker compose

## Manual Setup

### Install Node.js

```bash
sudo apt-get install software-properties-common
curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
```

### Get the latest Node.js package

```bash
sudo apt-get install -y nodejs
```

### Install Yarn

```bash
npm install -g yarn
```

### Start the server

```bash
cd litmus-docs/website
npm start
```

## Using Docker compose

### Install docker compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Run the server

```bash
docker-compose up
```


## Browse local documentation
http://localhost:3000/docs/next/getstarted.html

