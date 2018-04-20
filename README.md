# ML pilot project

This repository is used for project planning and issue tracking for the ML
pilot project at Datalab Amsterdam.

## frontend

To start the frontend locally run:
```
	npm run dev
```

## current_traffic_signs
To download the current traffic signs data:

1. Add the objecstore password to your environment:
```export OBJECTSTORE_PASSWORD=****```

2. Build and run the docker:
```
    cd current_trafic_signs
    docker-compose build
    docker-compose up
```
Or install the packages and run locally:
```
 cd current_trafic_signs
 virtualenv --python=$(which python3) venv
 source venv/bin/activate
 pip install -r requirements.txt
 docker-dev.sh
```

