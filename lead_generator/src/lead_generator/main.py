#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from lead_generator.crew import LeadGenerator


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(prompt: str):
    """
    Run the crew.
    """
    inputs = {
        'file_path': 'icp.txt',
        'leads': 'leads.csv',
        "prompt": prompt,
        "today": str(datetime.now())
    }
    
    try:
        LeadGenerator().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")



run(prompt='I am a logistics SaaS company helping businesses track their deliveries in real-time, and I need an SDR to get logistics managers on intro calls.')