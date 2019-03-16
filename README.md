# README

Servicio que convierte de BTC a USD y luego a VES, basado en las tasas que provee localbitcoins

## Instalación

Para facilitar la instalación, se recomienda utilizar [virtualenv](https://virtualenv.pypa.io)

```
    python3 -m venv env
    . env/bin/activate
    pip install -r requirements.txt
```

## Ejecutar localticker

Para iniciar la aplicación se provee un script sencillo `run.sh` que recibe como parámetro la dirección ip:puerto en
la que se desea que la aplicacion escuche. Sin embargo, se puede iniciar utilizando gunicorn directamente

```
    bash run.sh 0.0.0.0:80000
    # También
    gunicorn main:app -b $ADDRESS --log-file -
```

## Visualizar los datos

Se debe visitar `/listing` para ver los datos
