import asyncio, os
from browser_use import Agent, ChatLiteLLM, Browser, Tools, ActionResult
from dotenv import load_dotenv
import litellm
from models.puppy import PuppyList
from config import BASE_URL, DATABASE_FILENAME
from logs.puppy_logger import puppy_logger
from database.database import create_tables

load_dotenv()
litellm.drop_params = True

tools: Tools = Tools()
logger: puppy_logger = puppy_logger()

@tools.action(description="Export the extracted information into a file", param_model=PuppyList)
def export_puppy_list_to_file(result: PuppyList)->ActionResult:
    """Export the extracted puppies' list to a file."""
    if not result:
        return ActionResult(
            extracted_content='This task failed: no puppies were found!',
            is_done=False,
            success=False
        )
    
    with open(DATABASE_FILENAME, 'w') as file:
        file.write(result.model_dump_json(indent=4, ensure_ascii=False))

    return ActionResult(
        extracted_content='This task was successfully completed!',
        is_done=True,
        success=True
    )

async def run_puppy_web_scraper_agent(breed, top_k):
    """Configure and run the Browser Use agent to web scrape the puppies' information."""
    task_per_puppy = ';\n'.join([f'5.{i} - Navigate to the page for the ad that is position {i} in the ads list. Extract the following values: picture URL of the puppy, the puppy price, puppy breed, puppy color, puppy age, puppy gender, puppy notes, breeder name, breeder location, breeder type, and breeder notes. Skip no found values. Navigate back to the previous page. Await the results to be loaded' for i in range(1, top_k + 1)])
    task = f"""
    1 - Navigate to the source website {BASE_URL};
    2 - Search for what you are looking for as {breed};
    3 - Order the results by the most recent ones;
    4 - Await results to be loaded;
    5 - You will extract the information of the top {top_k} results. So:
    {task_per_puppy}
    6 - Do not make any additional explanations, no validations and no comments.;
    7 - Use the function export_puppy_list_to_file as a tool to export the extracted information into a file; 
    """

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

    agent: Agent = Agent(
        browser=browser,
        llm=llm,
        task=task,
        output_model_schema=PuppyList,
        tools=tools,
        flash_mode=True
    )

    history = await agent.run()
    return history.get_structured_output(output_model=PuppyList)

async def main():
    breed = 'teckel'
    top_k = 3

    logger.info(f'main: initiating puppy web scraping at {BASE_URL}')

    create_tables()

    await run_puppy_web_scraper_agent(breed, top_k)

if __name__ == "__main__":
    asyncio.run(main())