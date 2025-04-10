#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from crew import LeadGenerator
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

MAKE_WEBHOOK = os.getenv('MAKE_WEBHOOK')

def run(prompt: str):
    """
    Run the crew.
    """
    inputs = {
        'file_path': 'icp.txt',
        'leads_path': 'leads.csv',
        "prompt": prompt,
        "MAKE_WEBHOOK": MAKE_WEBHOOK,
        "url_webhook_report": "url_webhook_report.txt",
        'url_path': 'url_path.txt',
        "today": str(datetime.now())
    }
    
    try:
        LeadGenerator().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")



run(prompt='I am a logistics SaaS company helping businesses track their deliveries in real-time, and I need an SDR to get logistics managers on intro calls.')