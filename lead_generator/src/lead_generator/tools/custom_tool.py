from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List
import requests


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


class PeopleSearchInput(BaseModel):
    """Input schema for the PeopleSearchTool."""
    person_titles: List[str] = Field(..., description="Job titles to search for (e.g., 'marketing manager')")
    person_locations: List[str] = Field(default=[], description="Locations of the people (e.g., 'california')")
    person_seniorities: List[str] = Field(default=[], description="Seniority levels (e.g., 'director', 'vp')")
    organization_locations: List[str] = Field(default=[], description="Headquarter locations of employers")
    q_keywords: str = Field(default="", description="Free-text keyword search")
    page: int = Field(default=1, description="Pagination: Page number")
    per_page: int = Field(default=10, description="Results per page")

class PeopleSearchTool(BaseTool):
    name: str = "People Search Tool"
    description: str = (
        """This tool, named People Search Tool, allows users to search for people based on job titles, \
        locations, seniority levels, and free-text keyword searches. It integrates with the Apollo.io API to fetch relevant data. \

        Parameters:
        - person_titles (List[str]): A list of job titles to search for (e.g., "marketing manager", "software engineer").
        - person_locations (List[str], optional): A list of geographic locations to filter search results (e.g., "california", "new york").
        - person_seniorities (List[str], optional): A list of seniority levels to refine the search (e.g., "director", "vp").
        - organization_locations (List[str], optional): A list of locations where the organizations employing the individuals are headquartered.
        - q_keywords (str, optional): A free-text search term to find relevant people based on specific keywords.
        - page (int, optional, default=1): The page number for paginated search results.
        - per_page (int, optional, default=10): The number of results to return per page.

        Returns:
        - str: A JSON-formatted response containing the search results, which includes details such as names, job titles, company affiliations, and locations.

        Usage:
        This tool is useful for recruiters, sales professionals, and researchers looking to identify potential contacts or leads based on various criteria. 

        Error Handling:
        - If the API request fails, an error message will be returned.
        - Invalid or empty search criteria may lead to no results being found."""
            )
    
    args_schema: Type[BaseModel] = PeopleSearchInput

    def _run(
        self,
        person_titles: List[str],
        person_locations: List[str],
        person_seniorities: List[str],
        organization_locations: List[str],
        q_keywords: str,
        page: int,
        per_page: int
    ) -> str:
        url = "https://api.apollo.io/api/v1/mixed_people/search"
        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Authorization": "Bearer YOUR_API_KEY"
        }
        payload = {
            "person_titles": person_titles,
            "person_locations": person_locations,
            "person_seniorities": person_seniorities,
            "organization_locations": organization_locations,
            "q_keywords": q_keywords,
            "page": page,
            "per_page": per_page
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.text


class OrganizationSearchInput(BaseModel):
    """Input schema for the OrganizationSearchTool."""
    organization_num_employees_ranges: List[str] = Field(default=[], description="Employee count ranges (e.g., '1,10')")
    organization_locations: List[str] = Field(default=[], description="Locations of company HQs")
    organization_not_locations: List[str] = Field(default=[], description="Locations to exclude from search")
    q_organization_keyword_tags: List[str] = Field(default=[], description="Industry or keyword tags (e.g., 'mining')")
    q_organization_name: str = Field(default="", description="Specific name or partial name of the organization")
    revenue_range_min: int = Field(default=None, description="Minimum revenue")
    revenue_range_max: int = Field(default=None, description="Maximum revenue")
    page: int = Field(default=1, description="Pagination: Page number")
    per_page: int = Field(default=10, description="Results per page")

class OrganizationSearchTool(BaseTool):
    name: str = "Organization Search Tool"
    description: str = (
        """
        This tool, named Organization Search Tool, enables users to search for organizations based on employee count, location, industry tags, revenue range, and name. It integrates with the Apollo.io API to fetch relevant data.

        Parameters:
        - organization_num_employees_ranges (List[str], optional): A list of employee count ranges to filter organizations (e.g., "1,10", "50,200").
        - organization_locations (List[str], optional): A list of locations where the organizations are headquartered.
        - organization_not_locations (List[str], optional): A list of locations to exclude from the search.
        - q_organization_keyword_tags (List[str], optional): A list of industry-related keywords or tags (e.g., "mining", "tech").
        - q_organization_name (str, optional): The full or partial name of the organization to search for.
        - revenue_range_min (int, optional): The minimum revenue range for the organization.
        - revenue_range_max (int, optional): The maximum revenue range for the organization.
        - page (int, optional, default=1): The page number for paginated search results.
        - per_page (int, optional, default=10): The number of results to return per page.

        Returns:
        - str: A JSON-formatted response containing the search results, including organization names, locations, industries, and financial data.

        Usage:
        This tool is useful for business intelligence professionals, investors, and marketers looking to find organizations based on specific criteria.

        Error Handling:
        - If the API request fails, an error message will be returned.
        - Invalid or empty search criteria may lead to no results being found.
        """
    )
    args_schema: Type[BaseModel] = OrganizationSearchInput

    def _run(
        self,
        organization_num_employees_ranges: List[str],
        organization_locations: List[str],
        organization_not_locations: List[str],
        q_organization_keyword_tags: List[str],
        q_organization_name: str,
        revenue_range_min: int,
        revenue_range_max: int,
        page: int,
        per_page: int
    ) -> str:
        url = "https://api.apollo.io/api/v1/mixed_companies/search"
        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Authorization": "Bearer YOUR_API_KEY"
        }
        payload = {
            "organization_num_employees_ranges": organization_num_employees_ranges,
            "organization_locations": organization_locations,
            "organization_not_locations": organization_not_locations,
            "q_organization_keyword_tags": q_organization_keyword_tags,
            "q_organization_name": q_organization_name,
            "revenue_range": {
                "min": revenue_range_min,
                "max": revenue_range_max
            },
            "page": page,
            "per_page": per_page
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.text
