from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from markupsafe import escape
from datetime import date, datetime
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'thor'
app.config['MYSQL_DB'] = 'systemdeudas'
#app.config['MYSQL_PORT'] = '3306'
#app.config['MYSQL_UNIX_SOCKET'] = 'localhost'
mysql = MySQL(app)


@app.route('/')
def Index():
    return render_template('principal.html')

@app.route('/deudores')
def deudores():
    cur = mysql.connection.cursor()
    cur.execute('select * from deudor')
    data = cur.fetchall()
    return render_template('deudores.html', deudores = data)

@app.route('/deudores/eliminar/<int:post_id>')
def eliminardeudor(post_id):

    cur = mysql.connection.cursor()
    cur.execute('delete  from deudor where idpersona = %d' %post_id)
    mysql.connection.commit()
    #data = cur.fetchall()
    #return render_template('deudores.html', deudores = data)
    return redirect(url_for('deudores'))

@app.route('/deudores/editar', methods= ['POST'])
def editardeudor():
    if request.method == 'POST':
        idpersona = request.form['iddeudor']
        nombres = request.form['nombres']
        fechanacimiento = request.form['fechanacimiento']
        cur = mysql.connection.cursor()
        cur.execute("""
        update deudor set nombres = %s, fechanacimiento = %s where idpersona = %s 
        """,
        ( nombres, fechanacimiento, idpersona))
        mysql.connection.commit()
        
        return redirect(url_for('deudores'))

@app.route('/deudores/nuevodeudor', methods= ['POST'])
def nuevodeudor():
    
    if request.method == 'POST':
        #idpersona = request.form['codigodeudor']
        nombres = request.form['nombres']
        fechanacimiento = request.form['fechanacimiento']
       
        #datefinal = date_time_obj.day + '-' + date_time_obj.month + '-' + date_time_obj.year
        cur = mysql.connection.cursor()
        cur.execute('insert into deudor (nombres, fechanacimiento) values ( %s, %s)',
        ( nombres, fechanacimiento))
        mysql.connection.commit()
        #selected_date = datetime.strptime(fechanacimiento, "%Y-%m-%d").date()
       
        return redirect(url_for('deudores'))



@app.route('/deudas')
def deudas():
    cur = mysql.connection.cursor()
    cur.execute('select iddeuda, cantidaddeuda, motivodeuda, fechacreacion,estado,idpersona, nombres from deuda join deudor on deuda.iddeudor = deudor.idpersona')
    data = cur.fetchall()
    cur.execute('select idpersona, nombres from deudor')
    data2 = cur.fetchall()
    
    datas = [data,data2]
    return render_template('deudas.html', deudas = datas)

@app.route('/abonos')
def abonos():
    cur = mysql.connection.cursor()
    cur.execute('select idpersona,nombres, deuda.iddeuda, cantidad, fechaabono, descripcionabono  from abono join deuda on abono.iddeuda = deuda.iddeuda join deudor  on deuda.iddeudor = deudor.idpersona')
    data = cur.fetchall()
    return render_template('abonos.html', abonos = data)
    

if __name__ == '__main__':
    app.run(port = 80, debug = True)

