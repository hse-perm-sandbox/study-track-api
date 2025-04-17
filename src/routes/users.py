from fastapi import APIRouter


router = APIRouter(
    prefix="/api/users",
)

def __init__(self):
    self.name = "NoName"
    self.email = "NoEmail"
    self.hash_password = None
    self.id_user = None

def __init__(self, name: str, email: str, hash_password: int, id_user: int):
    self.name = name
    self.email = email
    self.hash_password = hash_password
    self.id_user = id_user

def print_user(self):
    print(f"Name: {self.name}\n",
          f"Email: {self.email}\n",
          f"Password's hash: {self.hash_password}\n",
          f"ID: {self.id_user}\n")
    
def get_user(self):
    return {"Name": self.name, "Email": self.email, "Password's hash": self.hash_password, "ID": self.id_user}
    
def delete_user(self):
    del self

def update_name(self, name: str):
    self.name = name

def update_email(self, email: str):
    self.email = email

def update_hash(self, hash: int):
    self.hash_password = hash

def update_id(self, id: int):
    self.id_user = id