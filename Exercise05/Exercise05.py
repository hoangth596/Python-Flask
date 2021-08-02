from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from flask import Flask, request, jsonify
from sqlalchemy.sql.sqltypes import Date
from datetime import datetime


engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'Customer'

    id = Column(Integer, primary_key=True)
    CustomerName = Column(String(50), nullable=False)
    ContactName = Column(String(50), nullable=False)
    Address = Column(String(200), nullable=False)
    City = Column(String(100), nullable=False)
    PostalCode = Column(String(50))
    Country = Column(String(50), nullable=False)


    def __repr__(self):
        data = {
            'id': self.id,
            'CustomerName': self.CustomerName,
            'ContactName': self.ContactName,
            'Address': self.Address,
            'City': self.City,
            'PostalCode':self.PostalCode,
            'Country': self.Country
        }
        
        return data


class Employee(Base):
    __tablename__ = 'Employee'

    id = Column(Integer, primary_key=True)
    LastName = Column(String(50), nullable=False)
    FirstName = Column(String(50), nullable=False)
    BirthDate = Column(Date, nullable=False)
    Photo = Column(String(50), nullable=False)
    Notes = Column(String(200))

    def __repr__(self):
        data = {
            'id': self.id,
            'LastName': self.LastName,
            'FirstName': self.FirstName,
            'BirthDate': self.BirthDate,
            'Photo': self.Photo,
            'Notes':self.Notes
        }

        return data


Base.metadata.create_all(engine)

app = Flask(__name__)


@app.route("/customer/create", methods=['POST'])
def create_customer():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = request.form
    try:
        customer = Customer(**data)
        session.add(customer)
        output = {
            'message': 'success'
        }
        session.commit()
    except Exception as e:
        output = {
            'message': str(e)
        }
    
    return jsonify(output)


@app.route("/customer/get", methods=['GET'])
def get_customer():
    Session = sessionmaker(bind=engine)
    session = Session()
    param = request.args
    result = session.query(Customer)
    for key, value in param.items():
        result = result.filter(getattr(Customer, key) == value)
    results = [i.__repr__() for i in result]
    
    data = {
        'data': results
    }

    return jsonify(data)


@app.route("/customer/update", methods=['PUT'])
def update_customer():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = request.form
    param = request.args

    try:
        id = param['id']
        result = session.query(Customer).filter_by(id=id)
        result.update(data)
        session.commit()
        output = {
            'message': 'success'
        }
    except Exception as e:
        output = {
            'message': str(e)
        }

    return jsonify(output)


@app.route("/customer/delete", methods=['DELETE'])
def delete_customer():
    Session = sessionmaker(bind=engine)
    session = Session()
    param = request.args
    try:
        id = param['id']
        result = session.query(Customer).filter_by(id=id)
        result.delete()
        session.commit()
        output = {
            'message': 'success'
        }
    except Exception as e:
        output = {
            'message' : str(e)
        }

    return jsonify(output)


@app.route("/employee/create", methods=['POST'])
def create_employee():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = request.form
    insert_data = dict(data)
    try:
        if insert_data.get('BirthDate') is not None:
            insert_data['BirthDate'] = datetime.strptime(insert_data['BirthDate'], '%Y-%m-%d').date()
        employee = Employee(**insert_data)
        session.add(employee)
        output = {
            'message': 'success'
        }
        session.commit()
    except Exception as e:
        output = {
            'message' : str(e)
        }

    return jsonify(output)


@app.route("/employee/get", methods=['GET'])
def get_employee():
    Session = sessionmaker(bind=engine)
    session = Session()
    param = request.args
    param = dict(param)
    
    if param.get('BirthDate') is not None:
        try:
            param['BirthDate'] = datetime.strptime(param['BirthDate'], '%Y-%m-%d').date()
            print(param['BirthDate'])
        except Exception as e:
            response = {
                "message": str(e)
            }
            return jsonify(response)

    result = session.query(Employee)
    for key, value in param.items():
        result = result.filter(getattr(Employee, key) == value)
    results = [i.__repr__() for i in result]
    
    data = {
        'data': results
    }

    return jsonify(data)


@app.route("/employee/update", methods=['PUT'])
def update_employee():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = request.form
    param = request.args
    data = dict(data)
    
    try:
        if data.get('BirthDate') is not None:
            data['BirthDate'] = datetime.strptime(data['BirthDate'], '%Y-%m-%d').date()
        id = param['id']
        result = session.query(Employee).filter_by(id=id)
        result.update(data)
        session.commit()
        output = {
            'message' : 'success'
        }
    except Exception as e:
        output = {
            'message' : str(e)
        }

    return jsonify(output)


@app.route("/employee/delete", methods=['DELETE'])
def delete_employee():
    Session = sessionmaker(bind=engine)
    session = Session()
    param = request.args

    try:
        id = param['id']
        result = session.query(Employee).filter_by(id=id)
        result.delete()
        session.commit()
        output = {
            'message' : 'success'
        }
    except Exception as e:
        output = {
            'message' : str(e)
        }

    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)

