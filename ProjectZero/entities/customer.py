

class Customer:
    def __init__(self, customer_id: int, first_name: str, last_name: str, phone_number: str, email: str,
                 address: str):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = first_name.lower() +'.'+last_name.lower() +'@' + email
        self.address = address


    def as_json_dic(self): #->dic
        return {'customerId': self.customer_id,
                'firstName': self.first_name,
                'lastName': self.last_name,
                'phoneNumber': self.phone_number,
                'emailAddress': self.email,
                'address': self.address

                }
    @staticmethod
    def json_deserialize(as_json_dic):
        customer = Customer(0, '', '', '', '', '')
        customer.customer_id = as_json_dic['customerId']
        customer.first_name = as_json_dic['firstName']
        customer.last_name = as_json_dic['lastName']
        customer.phone_number = as_json_dic['phoneNumber']
        customer.email = as_json_dic['emailAddress']
        customer.address = as_json_dic['address'] # as_json_dic put dic
        return customer


    def __str__(self):
        return f'ID: {self.customer_id} First Name = {self.first_name} Last Name: {self.last_name}' \
               f'Phone Number: {self.phone_number} Email: {self.email} Adddress: { self.address}'

