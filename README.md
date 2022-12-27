# Meaning++Maps

Meaning is mapped using language, visuals, etc

AI like Stable Diffusion for image generation, or ChatGPT for chatbot conversation illustrates how this is done, through machine learning

I do this in conversation, as do you, and we try to "communicate", i.e. come to consensus on what meaning we are each 
referring to, or at least figuring out how to work with each other to pursue each of our goals.

This project documents some methods of mapping meaning, through illustrations of two books:
* Christopher Alexander and team's "A Pattern Language"
* Wittgenstein's "Tractatus Logico-Philosophicus"

And an implementation of a short, interactive game:
* Free Association

Explore chords on the helix
* Musical Visualization

# Spinning up

### Make the database available

On a computer with Docker Client running:

``` sh neo4jup.sh```

This will pull the latest docker image and run the container, mapping it to ports 7474 and 7687

### Load the database with the data models used in our three applications

You will need conda installed and configured on your machine to follow the next steps.
If you do not have this, you can also run without conda by running ``` pip install -r requirements.txt```

``` 
conda create -n "meaningMapsDataLoad" python=3.9.15
conda activate meaningMapsDataLoad
pip install -r requirements.txt
```

Run

```
python dataLoad.py [-p] --process 0 (( will NOT process actual node and edge creation ))
python dataLoad.py [-p] --process 1 (( WILL process actual node and edge creation ))
```

### Start react app

#### Update version of npm and install compatible version of node.js
* npm install -g npm
* https://nodejs.org/en/
* nvm install --lts
* nvm use --lts

#### Install and run create-react-app
npm install -g create-react-app
npx create-react-app meaning_maps
cd meaning_maps
npm start

npm audit fix --force


Navigate to localhost:3000 to view app running




### Deploy to AWS

Use CDK

Setup steps for your own, personal AWS account

Setup and Teardown
* Setup with one command
* Teardown with one command