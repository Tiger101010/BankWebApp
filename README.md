# BankWebApp
This is a bank website built for SWE266P
___

Use docker
---

1. Run following command to build a image
```bash
docker image build -t bank_docker . 
```

2. Run following command to run the image
```bash
docker run -p 5001:5000 bank_docker 
```

3. Open [127.0.0.1:5001](http://127.0.0.1:5000/) in browser


Install
-------

Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install Flaskr::

    $ pip install -r requirements.txt

Run
---

::

    $ export FLASK_APP=banker
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run

Or on Windows cmd::

    > set FLASK_APP=banker
    > set FLASK_ENV=development
    > flask init-db
    > flask run

Open http://127.0.0.1:5000 in a browser.
