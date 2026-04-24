from pydantic import BaseModel, Field
from enum import Enum

class BreederType(str, Enum):
    PROFESSIONAL = "professional"
    PRIVATE = "private"

class Breeder(BaseModel):
    name: str = Field(description='Username of the breeder')
    location: str = Field(description='Location of the breeder')
    type: BreederType = Field(description='Type of the breeder')
    notes: str = Field(description='Other relevant information from the breeder, like breeder inscription number, contact details, user tenure on the website, etc')

class PuppyGender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class Puppy(BaseModel):
    ad_url: str = Field(description="URL of the puppy's announcement")
    price: int = Field(description='Price of the puppy')
    picture_url: str = Field(description="URL of the puppy's picture")
    breed: str = Field(description='Breed of the puppy')
    color: str = Field(description='Color of the puppy')
    age: str = Field(description="Age of the puppy (e.g., '8 weeks', '2 months')")
    gender: PuppyGender = Field(description='Gender of the puppy')
    number_puppies_litter: int = Field(description='Number of puppies born in the litter')
    notes: str = Field(description='Other relevant details from the puppy, like documentation, pedigree, health condition, vaccination and deworming, etc')
    breeder: Breeder = Field(description='Breeder details')

class PuppyList(BaseModel):
    puppies: list[Puppy] = Field(description='List of puppies')