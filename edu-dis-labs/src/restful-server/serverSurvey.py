from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/odb'
db = SQLAlchemy(app)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isPaused = db.Column(db.Boolean)
    isNamed = db.Column(db.Boolean)
    name = db.Column(db.String(255))
    duration = db.Column(db.Integer)
    account_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<Survey {self.name}>"
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route("/api/survey", methods=["GET", "POST"])
def api_survey():
    if request.method == "GET":
        surveys = Survey.query.all()
        return jsonify([survey.as_dict() for survey in surveys])

    elif request.method == "POST":
        data = request.json
        new_survey = Survey(isPaused=data['isPaused'], isNamed=data['isNamed'], name=data['name'],
                            duration=data['duration'], account_id=data['account_id'])
        db.session.add(new_survey)
        db.session.commit()
        return jsonify({'success': True}), 201

@app.route("/api/survey/<int:survey_id>", methods=["GET", "PUT", "DELETE"])
def api_survey_numbered(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    

    if request.method == "GET":
        return jsonify(survey.as_dict())

    elif request.method == "PUT":
        data = request.json

        survey.isPaused = data['isPaused']
        survey.isNamed = data['isNamed']
        survey.name = data['name']
        survey.duration = data['duration']
        survey.account_id = data['account_id']

        db.session.commit()
        return jsonify({'success': True})

    elif request.method == "DELETE":
        db.session.delete(survey)
        db.session.commit()
        return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
