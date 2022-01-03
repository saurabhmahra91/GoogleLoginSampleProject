import jwt
class User:
    def __init__(self, name, email) -> None:
        self.name = name
        self.email = email
    def parse(self):
        return {"name":self.name, "email":self.email}

new_user = User("saurabh", "saurabhmahra91@gmail.com")
token = jwt.encode(payload=new_user.parse(), key="SECRET", algorithm="HS256")
data = jwt.decode(jwt=token, key="SECRET", algorithms="HS256")
print(data)