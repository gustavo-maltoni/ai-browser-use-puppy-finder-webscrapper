import asyncio, os
from browser_use import Agent, ChatLiteLLM, Browser
from dotenv import load_dotenv
import litellm
from pydantic import BaseModel, Field
from enum import Enum

load_dotenv()
litellm.drop_params = True

browser = Browser(
    headless=False,
    proxy={
        'server': os.getenv('HTTPS_PROXY')
    }
)

llm = ChatLiteLLM(
    model='gpt-5-mini',
    api_key=os.getenv('LITELLM_API_KEY'),
    api_base=os.getenv('LITELLM_BASE_URL'),
)

source_website = 'https://olx.pt'
breed = 'teckel'
top_k = 3

task_per_puppy = ';\n'.join([f'5.{i} - Navigate to the page for the ad that is position {i} in the ads list. Extract the following values: picture URL of the puppy, the puppy price, puppy breed, puppy color, puppy age, puppy gender, puppy notes, breeder name, breeder location, breeder type, and breeder notes. Skip no found values. Navigate back to the previous page. Await the results to be loaded' for i in range(1, top_k + 1)])
task = f"""
1 - Navigate to the source website {source_website};
2 - Search for what you are looking for as {breed};
3 - Order the results by the most recent ones;
4 - Await results to be loaded;
5 - You will extract the information of the top {top_k} results. So:
{task_per_puppy}
"""

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
    picture_url: str = Field(description="URL of the puppy's picture")
    price: int = Field(description='Price of the puppy')
    breed: str = Field(description='Breed of the puppy')
    color: str = Field(description='Color of the puppy')
    age: str = Field(description="Age of the puppy (e.g., '8 weeks', '2 months')")
    gender: PuppyGender = Field(description='Gender of the puppy')
    number_puppies_litter: int = Field(description='Number of puppies born in the litter')
    notes: str = Field(description='Other relevant details from the puppy, like documentation, pedigree, health condition, vaccination and deworming, etc')
    breeder: Breeder = Field(description='Breeder details')

class PuppiesList(BaseModel):
    puppies: list[Puppy] = Field(description='List of puppies')

async def run_agent()-> PuppiesList | None:
    agent: Agent = Agent(
        browser=browser,
        llm=llm,
        task=task,
        output_model_schema=PuppiesList
    )

    history = await agent.run()
    return history.get_structured_output(output_model=PuppiesList)

async def main():
    result = await run_agent()

    if not result:
        return;

    for puppy in result.puppies:
        print(f'Price: {puppy.price}')
        print(f'Color: {puppy.color}')
        print(f'Gender: {puppy.gender}')
        print(f'Breeder Name: {puppy.breeder.name}')
        print(f'Breeder Location: {puppy.breeder.location}')

if __name__ == "__main__":
    asyncio.run(main())