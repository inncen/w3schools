from pydantic import BaseModel, Field
from faker import Faker


fake = Faker()


class Customer(BaseModel):
    customer_name: str = Field(alias='CustomerName', )
    contact_name: str = Field(alias='ContactName')
    address: str = Field(alias='Address')
    city: str = Field(alias='City')
    postal_code: str = Field(alias='PostalCode')
    country: str = Field(alias='Country')

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def random(cls):
        return Customer(
            customer_name=fake.name(),
            contact_name=fake.name(),
            address=' '.join(fake.address().splitlines()),
            city=fake.city(),
            postal_code=fake.postcode(),
            country=fake.country()
        )

    def values(self):
        return tuple(self.dict().values())

    def columns(self):
        return tuple(self.dict(by_alias=True).keys())

    def columns_with_values(self):
        return ','.join([
            f'{column}="{value}"'
            for column, value in zip(self.columns(), self.values())
        ])
