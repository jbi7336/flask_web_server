from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

_apps = Flask(__name__)
_apps.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rfid.db'
_apps.config['JSON_AS_ASCII'] = False
_db = SQLAlchemy(_apps)

class Rfid(_db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    keyValue = _db.Column(_db.String(20), nullable=False, unique=True)
    x = _db.Column(_db.Integer)
    y = _db.Column(_db.Integer)
    floor = _db.Column(_db.Integer)
    content = _db.Column(_db.String(100), nullable=True)
    date_created = _db.Column(_db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@_apps.route('/', methods=['GET'])
def main_page():
    if request.method == 'GET':
        tasks = Rfid.query.order_by(Rfid.id).all()
        return render_template('index.html', tasks=tasks)
    else:
        pass

@_apps.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        tempKey = request.form['keyValue']
        tempX = request.form['x']
        tempY = request.form['y']
        tempFloor = request.form['floor']
        tempContent = request.form['content']
        
        new_rfid = Rfid(keyValue=tempKey, x=tempX, y=tempY, floor=tempFloor, content=tempContent)

        try:
            _db.session.add(new_rfid)
            _db.session.commit()
            return redirect('/')
        except:
            return redirect(url_for('error', eValue=1))
    else:
        return render_template('add.html')

@_apps.route('/delete/<int:id>')
def delete(id):
    task_do_delete = Rfid.query.get_or_404(id)

    try:
        _db.session.delete(task_do_delete)
        _db.session.commit()
        return redirect('/')
    except:
        return redirect(url_for('error', eValue=2))

@_apps.route('/update/<string:keyValue>', methods=['POST', 'GET'])
def update(keyValue):
    task = Rfid.query.get_or_404(keyValue)

    if request.method == 'POST':
        task.keyValue = request.form['keyValue']
        task.x = request.form['x']
        task.y = request.form['y']
        task.floor = request.form['floor']
        task.content = request.form['content']

        try:
            _db.session.commit()
            return redirect('/')
        except:
            return redirect(url_for('error', eValue=3))
    else:
        return render_template('update.html', task=task)

@_apps.route('/getId/<int:id>')
def get_id(id):
    try:
        task = Rfid.query.get_or_404(id)
        jsonData = {
                        "id": task.id,
                        "keyValue": task.keyValue,
                        "x": task.x,
                        "y": task.y,
                        "floor": task.floor,
                        "content": task.content,
                        "time": task.date_created
                    }

        return jsonify(jsonData)
    except:
        return redirect(url_for('error', eValue=4))

@_apps.route('/postId', methods=['POST'])
def post_id():
    if request.method == 'POST':
        jsonData = request.get_json(silent=True)
        print(jsonData)

        tempKey = jsonData['keyValue']
        tempX = jsonData['x']
        tempY = jsonData['y']
        tempFloor = jsonData['floor']
        tempContent = jsonData['content']

        new_rfid = Rfid(keyValue=tempKey, x=tempX, y=tempY, floor=tempFloor, content=tempContent)

        try:
            _db.session.add(new_rfid)
            _db.session.commit()
            return "POST JSON SUCCESS"
        except:
            return redirect(url_for('error', eValue=5))
    else:
        return redirect('/')

@_apps.route('/findKey/<key>')
def find_key(key):
    try:
        task = Rfid.query.filter_by(keyValue=key).first()
        print(task)
        jsonData = {
                        "id": task.id,
                        "keyValue": task.keyValue,
                        "x": task.x,
                        "y": task.y,
                        "floor": task.floor,
                        "content": task.content,
                        "time": task.date_created
                    }

        return jsonify(jsonData)
    except:
        return redirect(url_for('error', eValue=6))

@_apps.route('/error/<int:eValue>')
def error(eValue):
    return render_template('error.html', task=eValue)

if __name__ == '__main__':
    _apps.run(debug=True, host="0.0.0.0", port="8080")