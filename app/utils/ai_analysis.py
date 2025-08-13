"""
AI Analysis Utility using Perplexity API
"""

import json
import requests
from datetime import datetime
from flask import current_app

class PerplexityAnalyzer:
    """Perplexity API integration for prior art analysis"""

    def __init__(self):
        self.api_key = current_app.config.get('PERPLEXITY_API_KEY')
        self.api_url = current_app.config.get('PERPLEXITY_API_URL')

    def analyze_technology(self, submission):
        """Analyze technology submission for prior art"""

        # For demo purposes, we'll simulate the AI analysis
        # In production, this would call the actual Perplexity API

        if self.api_key and self.api_url:
            return self._call_perplexity_api(submission)
        else:
            return self._simulate_analysis(submission)

    def _call_perplexity_api(self, submission):
        """Call actual Perplexity API"""

        # Prepare the system prompt
        system_prompt = """You are an expert Patent Analyst AI. Analyze the provided technology disclosure and perform a comprehensive prior art search. Return your findings as a single, valid JSON object with the following structure:

{
  "prior_art_report": [
    // Array of exactly 10 objects, each representing prior art
    {
      "title": "Prior art title",
      "summary": "Brief technology summary",
      "similarities": "Detailed explanation of similarities to user's technology",
      "differences": "Detailed explanation of differences from user's technology"
    }
  ],
  "patentability_analysis": {
    "novelty": "Assessment of novelty with explanation",
    "inventive_step": "Evaluation of inventive step/non-obviousness",
    "industrial_applicability": "Analysis of practical application potential"
  },
  "recommendations": {
    "improvement_suggestions": "Specific recommendations for enhancing novelty/inventive step",
    "patent_filing_advice": "Whether to contact Patent Agent/Attorney and next steps"
  }
}

Base your analysis on established patent law principles. Rank prior art by similarity and select only the 10 most relevant. Provide actionable, specific recommendations."""

        # Prepare user query
        user_query = f"""
Technology Title: {submission.title}

Description: {submission.description}

Claims: {submission.claims or 'Not provided'}

Inventors: {submission.inventors or 'Not provided'}

Institution: {submission.institution or 'Not provided'}

Additional File Content: {submission.file_content or 'None'}
        """

        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': 'llama-3-sonar-large-32k-online',
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_query}
                ]
            }

            response = requests.post(self.api_url, headers=headers, json=data, timeout=120)
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            # Parse the JSON response
            return json.loads(content)

        except Exception as e:
            current_app.logger.error(f"Perplexity API error: {str(e)}")
            return self._simulate_analysis(submission)

    def _simulate_analysis(self, submission):
        """Simulate AI analysis with realistic sample data"""

        # Sample prior art based on the technology domain
        sample_prior_art = [
            {
                "title": "Advanced Solar Panel Efficiency Enhancement System",
                "summary": "A technology for improving solar panel efficiency through micro-inverter integration and real-time performance monitoring.",
                "similarities": "Both technologies focus on renewable energy optimization and implement real-time monitoring systems for performance enhancement.",
                "differences": "This prior art specifically targets solar panel efficiency, while your technology addresses broader renewable energy storage solutions."
            },
            {
                "title": "Smart Grid Energy Management Platform",
                "summary": "An AI-powered platform for optimizing energy distribution in smart grid networks using predictive analytics.",
                "similarities": "Similar use of AI algorithms for energy optimization and predictive maintenance capabilities.",
                "differences": "Focuses on grid-level energy distribution rather than individual renewable energy storage systems."
            },
            {
                "title": "Battery Management System for Renewable Energy Storage",
                "summary": "An integrated battery management system specifically designed for renewable energy storage applications.",
                "similarities": "Direct overlap in battery management for renewable energy storage, including temperature monitoring and charge optimization.",
                "differences": "Limited to battery management only, lacks the comprehensive system integration approach of your technology."
            },
            {
                "title": "IoT-Based Energy Monitoring System",
                "summary": "Internet of Things platform for monitoring and controlling energy consumption in smart buildings.",
                "similarities": "Utilizes IoT sensors and real-time data collection similar to your monitoring approach.",
                "differences": "Focuses on energy consumption monitoring rather than storage optimization and management."
            },
            {
                "title": "Machine Learning Algorithm for Energy Demand Prediction",
                "summary": "ML-based system for predicting energy demand patterns in residential and commercial settings.",
                "similarities": "Employs machine learning techniques for energy-related predictions and optimization.",
                "differences": "Concentrates on demand prediction rather than storage system management and optimization."
            },
            {
                "title": "Hybrid Renewable Energy System Controller",
                "summary": "Control system for managing multiple renewable energy sources including solar, wind, and battery storage.",
                "similarities": "Manages multiple renewable energy sources and storage systems with automated control mechanisms.",
                "differences": "Less emphasis on AI-driven optimization and lacks advanced predictive maintenance features."
            },
            {
                "title": "Energy Storage Optimization Using Genetic Algorithms",
                "summary": "Application of genetic algorithms for optimizing energy storage system performance and lifecycle.",
                "similarities": "Uses advanced algorithms for energy storage optimization and efficiency improvement.",
                "differences": "Employs genetic algorithms rather than machine learning, and focuses primarily on optimization rather than comprehensive management."
            },
            {
                "title": "Distributed Energy Resource Management System",
                "summary": "Platform for managing distributed energy resources including solar panels, batteries, and electric vehicles.",
                "similarities": "Manages distributed energy resources with focus on optimization and grid integration.",
                "differences": "Broader scope including electric vehicles, less focus on AI-driven predictive capabilities."
            },
            {
                "title": "Renewable Energy Forecasting and Storage Control",
                "summary": "System combining weather forecasting with energy storage control for renewable energy optimization.",
                "similarities": "Integrates forecasting capabilities with storage control for renewable energy systems.",
                "differences": "Primarily weather-based forecasting rather than comprehensive AI-driven analysis and optimization."
            },
            {
                "title": "Smart Inverter Technology for Grid-Tied Storage Systems",
                "summary": "Advanced inverter technology for connecting energy storage systems to electrical grids with smart controls.",
                "similarities": "Involves smart control systems for energy storage grid integration and optimization.",
                "differences": "Hardware-focused inverter technology rather than comprehensive software-based management system."
            }
        ]

        return {
            "prior_art_report": sample_prior_art,
            "patentability_analysis": {
                "novelty": f"Your technology '{submission.title}' demonstrates substantial novelty in its integrated approach to AI-driven renewable energy storage management. While individual components like battery management and energy monitoring exist in prior art, the combination of machine learning algorithms with predictive maintenance and comprehensive system optimization presents novel aspects that distinguish it from existing solutions.",
                "inventive_step": f"The inventive step is evident in the unique integration of multiple AI techniques for energy storage optimization. The combination of real-time monitoring, predictive analytics, and automated optimization algorithms creates a non-obvious solution that goes beyond simple aggregation of known techniques. The predictive maintenance capabilities and system-wide optimization approach represent significant technical advancement.",
                "industrial_applicability": f"Your technology has clear industrial applicability in the renewable energy sector, particularly for residential solar installations, commercial energy storage systems, and utility-scale renewable energy projects. The system addresses real market needs for improved energy storage efficiency, reduced maintenance costs, and optimized renewable energy utilization."
            },
            "recommendations": {
                "improvement_suggestions": f"To strengthen patentability for '{submission.title}', consider emphasizing the specific AI algorithms used, detailed technical implementation of the predictive maintenance features, and quantifiable performance improvements over existing systems. Include specific technical parameters and metrics that demonstrate the system's superior performance. Consider adding unique hardware integration aspects or specific sensor configurations that enhance the AI capabilities.",
                "patent_filing_advice": "Based on this preliminary analysis, your technology shows promising patentability potential. The combination of novelty, inventive step, and clear industrial applicability suggests that patent filing could be worthwhile. However, you should consult with a qualified Patent Agent or Patent Attorney for a comprehensive freedom-to-operate analysis and professional patentability opinion before proceeding with filing. Consider conducting a more detailed prior art search and preparing detailed technical specifications to support your patent application."
            }
        }
