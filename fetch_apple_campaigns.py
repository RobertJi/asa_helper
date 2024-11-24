import requests
from typing import Dict, List, Optional
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AppleSearchAdsAPI:
    BASE_URL = "https://api.searchads.apple.com/api/v4"
    
    def __init__(self, client_id: str, client_secret: str, org_id: str):
        """
        Initialize the Apple Search Ads API client
        
        Args:
            client_id: Apple Search Ads API client ID
            client_secret: Apple Search Ads API client secret
            org_id: Organization ID for the account
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.org_id = org_id
        self.access_token = None
        self.token_expiry = None
    
    def _get_auth_token(self) -> None:
        """Authenticate and get access token"""
        auth_url = f"{self.BASE_URL}/oauth/token"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "searchads.readonly"
        }
        
        response = requests.post(auth_url, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data["access_token"]
        # Store token expiry time
        self.token_expiry = datetime.now().timestamp() + token_data["expires_in"]
    
    def _get_headers(self) -> Dict:
        """Get headers for API requests"""
        if not self.access_token or datetime.now().timestamp() >= self.token_expiry:
            self._get_auth_token()
            
        return {
            "Authorization": f"Bearer {self.access_token}",
            "X-AP-Context": f"orgId={self.org_id}",
            "Content-Type": "application/json"
        }
    
    def get_campaigns(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Fetch all campaigns for the organization
        
        Args:
            limit: Number of campaigns to return per request
            offset: Offset for pagination
            
        Returns:
            List of campaign objects
        """
        url = f"{self.BASE_URL}/campaigns"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        response = requests.get(
            url,
            headers=self._get_headers(),
            params=params
        )
        response.raise_for_status()
        
        return response.json()["data"]
    
    def get_campaign_details(self, campaign_id: int) -> Dict:
        """
        Get detailed information about a specific campaign
        
        Args:
            campaign_id: ID of the campaign to fetch
            
        Returns:
            Campaign details object
        """
        url = f"{self.BASE_URL}/campaigns/{campaign_id}"
        
        response = requests.get(
            url,
            headers=self._get_headers()
        )
        response.raise_for_status()
        
        return response.json()["data"]

def main():
    # Load credentials from environment variables
    client_id = os.getenv("APPLE_ADS_CLIENT_ID")
    client_secret = os.getenv("APPLE_ADS_CLIENT_SECRET")
    org_id = os.getenv("APPLE_ADS_ORG_ID")
    
    if not all([client_id, client_secret, org_id]):
        raise ValueError("Missing required environment variables for Apple Search Ads API")
    
    # Initialize API client
    api_client = AppleSearchAdsAPI(client_id, client_secret, org_id)
    
    try:
        # Fetch all campaigns
        campaigns = api_client.get_campaigns()
        
        # Save campaigns to JSON file
        output_file = "apple_campaigns.json"
        with open(output_file, "w") as f:
            json.dump(campaigns, f, indent=2)
            
        print(f"Successfully fetched {len(campaigns)} campaigns and saved to {output_file}")
        
        # Print basic campaign info
        for campaign in campaigns:
            print(f"Campaign ID: {campaign['id']}")
            print(f"Name: {campaign['name']}")
            print(f"Status: {campaign['status']}")
            print("-" * 50)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching campaigns: {str(e)}")

if __name__ == "__main__":
    main() 