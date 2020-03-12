Documentation for the Litmus Project

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Flitmuschaos%2Flitmus-docs.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Flitmuschaos%2Flitmus-docs?ref=badge_shield)

Additional details on the Docusaurus project can be found [here](https://docusaurus.io/docs/en/installation.html).

## For Developers

### Clone litmus-docs repository

```bash
git clone https://github.com/litmuschaos/litmus-docs.git
cd litmus-docs
```

The website server can be setup manually or through docker and docker compose

## Use embedmd command before commiting changes

The embedded code will be extracted from the file at `URL`, which can either be a relative path to a file in the local file system (using always forward slashes as directory separator) or a URL starting with `http://` or `https://.`

 Flags (needs to be done before commiting the changes): 

-w: Executing `embedmd -w docs.md` will modify docs.md and add the corresponding code snippets, as shown in sample/result.md.

-d: Executing `embedmd -d docs.md` will display the difference between the contents of docs.md and the output of embedmd docs.md.


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
cd website
yarn install
yarn start
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

## License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Flitmuschaos%2Flitmus-docs.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Flitmuschaos%2Flitmus-docs?ref=badge_large)
