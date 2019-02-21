from flask import render_template, request, redirect, url_for
from app import app
import psycopg2

@app.route('/')
def index():
    dbParams = app.config['DATABASE']
    try:
        conn = psycopg2.connect(host=dbParams['host'], port=dbParams['port'], dbname=dbParams['dbname'], user=dbParams['dbuser'], password=dbParams['password'])
        cur = conn.cursor()

        query = "SELECT * FROM movimientos;"

        cur.execute(query);
        
        fila = cur.fetchone()
        movimientos = []
        while fila != None:
            movimiento = {}

            for ix in range(0, len(fila)):
                columnName = cur.description[ix][0]
                if columnName == 'fecha_hora':
                    dato = str(fila[ix])
                    movimiento['fecha'] = dato[:10]
                    movimiento['hora'] = dato[11:16]
                else:
                    movimiento[columnName] = fila[ix]
            movimientos.append(movimiento)

            fila = cur.fetchone()

        cur.close()
        conn.close()

    except Exception as e:
        print(e.pgerror)
        cur.close()
        conn.close()

    return render_template('index.html', registros=movimientos)


@app.route('/nuevoregistro', methods=['GET', 'POST'])
def nuevoregistro():
    if request.method == 'GET':
        return render_template('nuevoregistro.html')
    else:
        dbParams = app.config['DATABASE']
        try:
            conn = psycopg2.connect(host=dbParams['host'], port=dbParams['port'], dbname=dbParams['dbname'], user=dbParams['dbuser'], password=dbParams['password'])
            cur = conn.cursor()

            query = """INSERT INTO movimientos (fecha_hora, descripcion, moneda_comprada, cantidad_comprada, moneda_pagada, cantidad_pagada)
                    VALUES ('{} {}:00.000000', '{}', '{}', {}, '{}', {});"""
            f = request.form
            query = query.format(f['fecha'], f['hora'], f['descripcion'], f['monedaComprada'], f['cantidadComprada'], f['monedaPagada'], f['cantidadPagada'])

            cur.execute(query)

            conn.commit()
        except Exception as e:
            print(e.pgerror)
            cur.close()
            conn.close()

        return redirect(url_for('index'))
