from .models import User
from DjangoProject.settings import db_default

def UserDetail(id):
    user = User.objects.using(db_default).get(id=id)
    data = {
        "id" : user.id,
        "name" : str(user.first_name)+' '+str(user.last_name),
        "role" : user.role
    }
    return data