# Installing

You will need Python 3.6+. Install efesto with pip:

```
pip3 install efesto
```

Install gunicorn or another wsgi-compliant server:

```
pip install gunicorn
```

Initialize efesto:

```
efesto install
```


Start the server:

```
gunicorn "efesto.App:App.run()"
```


That's all! Normally, you will want to set a number of options so that efesto
is actually useful for your use case: [Configuration](/configuration) has
detailed list of these.
