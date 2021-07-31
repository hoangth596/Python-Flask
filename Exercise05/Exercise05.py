from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from flask import Flask, request, jsonify


engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'Customer'

    id = Column(Integer, primary_key=True)
    CustomerName = Column(String(50))
    ContactName = Column(String(50))
    Address = Column(String(100))
    City = Column(String(100))
    PostalCode = Column(String(50))
    Country = Column(String(50))


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
    last_name = Column(String(50))
    first_name = Column(String(50))
    birth_date = Column(String(100))
    photo = Column(String(100))
    notes = Column(String(50))

    def __repr__(self):
        data = {
            'id': self.id,
            'LastName': self.last_name,
            'FirstName': self.first_name,
            'BirthDate': self.birth_date,
            'Photo': self.photo,
            'Notes':self.notes
        }

        return data


Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route("/customer/create", methods=['POST'])
def create_customer():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = request.form
    customer = Customer(**data)
    session.add(customer)
    output = {
        'success': True
    }
    session.commit()
    
    return jsonify(output)


@app.route("/customer/update", methods=['PUT'])
def update_customer():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = request.form
    param = request.args

    result = session.query(Customer)
    for key, value in param.items():
        result = result.filter(getattr(Customer, key) == value)
    result.update(data)
    session.commit()
    output = {
        'success': True
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


@app.route("/customer/delete", methods=["POST"])
def delete_customer():
    Session = sessionmaker(bind=engine)
    session = Session()
    param = request.args

    result = session.query(Customer)
    for key, value in param.items():
        result = result.filter(getattr(Customer, key) == value)
    result.delete()
    session.commit()
    output = {
        'success': True
    }

    return jsonify(output)


@app.route("/employee/create", methods=['POST'])
def create_employee():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = request.form
    employee = Employee(**data)
    session.add(employee)
    output = {
        'success': True
    }
    session.commit()

    return jsonify(output)


@app.route("/employee/update", methods=['PUT'])
def update_employee():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = request.form
    param = request.args

    result = session.query(Employee)
    for key, value in param.items():
        result = result.filter(getattr(Employee, key) == value)
    result.update(data)
    session.commit()
    output = {
        'success': True
    }

    return jsonify(output)


@app.route("/employee/get", methods=['GET'])
def get_employee():
    Session = sessionmaker(bind=engine)
    session = Session()
    param = request.args
    result = session.query(Employee)
    for key, value in param.items():
        result = result.filter(getattr(Employee, key) == value)
    results = [i.__repr__() for i in result]
    
    data = {
        'data': results
    }

    return jsonify(data)


@app.route("/employee/delete", methods=["POST"])
def delete_employee():
    Session = sessionmaker(bind=engine)
    session = Session()
    param = request.args

    result = session.query(Employee)
    for key, value in param.items():
        result = result.filter(getattr(Employee, key) == value)
    result.delete()
    session.commit()
    output = {
        'success': True
    }

    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)