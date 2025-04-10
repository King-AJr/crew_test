from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List
import requests
from dotenv import load_dotenv
import os
import httpx
from parsel import Selector
from scrapfly import ScrapeConfig, ScrapflyClient

load_dotenv()

APOLLO_API_KEY=os.getenv('APOLLO_API_KEY')

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    

class ProfileHarvesterInput(BaseModel):
    """Input schema for MyCustomTool."""
    profile_url: str = Field(..., description="The full URL to the LinkedIn profile.")

class ProfileHarvesterTool(BaseTool):
    name: str = "LinkedInProfileScraper"
    description: str = (
        "Scrapes public LinkedIn profile information from a given profile URL. "
        "Useful for retrieving names, job titles, companies, and education background."
    )
    args_schema: Type[BaseModel] = ProfileHarvesterInput

    def _run(self, profile_url: str) -> str:
        try:
            scrapfly = ScrapflyClient(key="Your ScrapFly API key")

            response = scrapfly.scrape(ScrapeConfig(
                url=profile_url,
                asp=True,
                country="US",
                proxy_pool="public_residential_pool",
                render_js=True
            ))

            selector = response.selector
            html = response.scrape_result['content']

            # Example scraping (these selectors may need adjustment)
            name = selector.css('h1.text-heading-xlarge::text').get()
            headline = selector.css('div.text-body-medium.break-words::text').get()
            location = selector.css('span.text-body-small.inline.t-black--light.break-words::text').get()
            current_position = selector.css('div.pv-entity__summary-info h3 span:nth-child(2)::text').get()
            education = selector.css('section#education-section li h3 span:nth-child(2)::text').get()

            data = {
                "name": name,
                "headline": headline,
                "location": location,
                "current_position": current_position,
                "education": education,
            }

            return str(data)
        except Exception as e:
            return f"Failed to scrape profile: {str(e)}"


class BuildApolloPeopleURLInput(BaseModel):
    """Input schema for BuildApolloPeopleURL."""
    personTitles: List[str] = Field(
        ..., 
        description="List of job titles to filter by"
    )
    personLocations: List[str] = Field(
        ..., 
        description="List of locations to filter by"
    )
    sortAscending: bool = Field(
        False,
        description="Whether to sort ascending (true) or descending (false)"
    )
    sortByField: str = Field(
        "recommendations_score",
        description="Which field to sort by (e.g. 'recommendations_score')"
    )

class BuildApolloPeopleURL(BaseTool):
    name: str = "build_apollo_people_url"
    description: str = (
        "Constructs an Apollo people search URL given page number, "
        "personTitles, personLocations, sortAscending, and sortByField."
    )
    args_schema = BuildApolloPeopleURLInput

    def _run(self, personTitles: List[str], personLocations: List[str],
             sortAscending: bool, sortByField: str) -> str:

        base = "https://app.apollo.io/#/people?"

        parts = [f"page=1"]
        for title in personTitles:
            parts.append(f"personTitles[]={title.replace(' ', '%20')}")
        for loc in personLocations:
            parts.append(f"personLocations[]={loc.replace(' ', '%20')}")
        # sort
        parts.append(f"sortAscending={str(sortAscending).lower()}")
        parts.append(f"sortByField={sortByField}")
        return base + "&".join(parts)