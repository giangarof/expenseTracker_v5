# Code to reuse


def incrementId(data):
    result = data[-1].id + 1
    return result


# change Expense to model (or something better)
# the idea is to reuse this code in diferent schemas
def checkIfExist(db, Expense, id):
    data = db.query(Expense).filter(id == Expense.id).first()
    return data
