from .base import BaseModel


class Customer(BaseModel):

    customer_id = None
    email = None
    first_name = None
    last_name = None
    phone = None

    def __init__(self, customer_id, email=None, first_name=None, last_name=None, phone=None, **kwargs):
        super().__init__({
            "customer_id": customer_id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone
        }, **kwargs)

    @property
    def info(self):
        return {
            "id": self.customer_id,
            "email": self.email,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "phone": self.phone
        }

    def build_dict_values(self, key, value):
        return self._data[key]

