from cryptography.fernet import Fernet
import os

class PasswordManager:

    def __init__(self):
        self.key=None
        self.password_file=None
        self.password_dict={}
        
    def create_key(self,path):
        self.key=Fernet.generate_key();
        with open(path,'wb') as f:
            f.write(self.key)

    def load_key(self,path):
        with open(path,'rb') as f:
            self.key=f.read()

    #will be called only once
    def create_password_file(self,path,initial_values=None):
        self.password_file=path

        if initial_values is not None:
            for key,value in initial_values.items():
                self.add_password(key,value)

    def add_password(self,username,password):
        self.password_dict[username]=password

        if self.password_file is not None:
            with open(self.password_file,"a+") as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(username+":"+encrypted.decode()+"\n")
    
    def load_password_file(self,path):
        self.password_file=path
        
        with open(path,'r') as f:
            for line in f:
                username,encrypted=line.split(':')
                decrypted=Fernet(self.key).decrypt(encrypted.encode())
                self.password_dict[username]=decrypted
    
    def get_password(self,username):
        return self.password_dict[username]


pm=PasswordManager()
pm.create_key("mykey")
pm.load_key("mykey")


dict={
"email": "abcd1234",
"facebook" :"123456789",
"instagram":"19873kaj"
}
pm.create_password_file("password_file",dict)

done =False
while not done:
    print("""Enter your choice: 
    a) get password of an account
    b) add a username and password
    """)

    choice =input("Enter your choice:")
    if choice=="a":
        pm.load_password_file("password_file")
        username=input("Enter username:")
        print("password is "+ str(pm.get_password(username)))
    elif choice=="b":
        username=input("Enter username:")
        password=input("Enter password:")
        pm.add_password(username,password)
    elif choice=='q':
        done=True
    else:
        print("Invalid choice")

path=os.path.join(os.getcwd(),"password_file")
os.remove(path)


