import requests
from typing import Optional, Dict, List
import json
from bs4 import BeautifulSoup
from datetime import datetime, date
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def parse_diandian_table(html_content: str) -> Optional[Dict]:
    """
    Parse diandian.com table data using BeautifulSoup
    
    Args:
        html_content: HTML content containing the table
        
    Returns:
        Dictionary containing date and keywords data if successful, None if failed
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the table container
        table = soup.find('table', class_='dd-data-table')
        if not table:
            print("Table not found in HTML")
            return None
            
        # Get dates from table headers
        headers = table.find('thead').find_all('th')
        dates = [th.get_text().strip() for th in headers[1:]]  # Skip first header (#)
        
        # Get latest date
        latest_date = dates[-1] if dates else datetime.now().strftime("%Y-%m-%d")
        
        # Parse rows
        keywords = []
        rows = table.find('tbody').find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 2:
                continue
                
            # Get rank from first cell
            rank_cell = cells[0].find('span', class_='rank-value')
            rank_img = cells[0].find('img', class_='ranking-img')
            
            if rank_img:
                if 'first' in rank_img['src']:
                    rank = 1
                elif 'second' in rank_img['src']:
                    rank = 2
                elif 'third' in rank_img['src']:
                    rank = 3
            elif rank_cell:
                rank = int(rank_cell.text.strip())
            else:
                continue
                
            # Get latest keyword data
            latest_cell = cells[-1]
            keyword_div = latest_cell.find('div', class_='table-content-name')
            volume_div = latest_cell.find('div', class_='dd-second-font-color')
            
            if not keyword_div:
                continue
                
            keyword = keyword_div.text.strip()
            volume = 0
            if volume_div:
                try:
                    volume = int(volume_div.text.strip())
                except ValueError:
                    volume = 0
                    
            keywords.append({
                "keyword": keyword,
                "search_volume": volume,
                "rank": rank
            })
            
        # Sort keywords by rank
        keywords.sort(key=lambda x: x["rank"])
        
        return {
            "date": latest_date,
            "keywords": keywords
        }
        
    except Exception as e:
        print(f"Error parsing table: {str(e)}")
        return None


def fetch_diandian_hot_words(keyword: str) -> Optional[Dict]:
    """
    Fetch hot keywords from diandian.com using Selenium
    """
    url = f'https://app.diandian.com/tool/searchIntelligent-1-24-{keyword}'

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        # Initialize the Chrome driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Load the page
        driver.get(url)
        
        # Wait for table to be present (adjust timeout as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dd-data-table"))
        )
        
        # Get the page source after JavaScript has rendered
        html_content = driver.page_source
        
        # Save the response
        save_response_selenium(html_content, keyword)
        
        # Parse the table
        result = parse_diandian_table(html_content)
        
        return result
        
    except Exception as e:
        print(f"Error fetching hot words: {str(e)}")
        return None
        
    finally:
        if 'driver' in locals():
            driver.quit()


def save_response_selenium(html_content, keyword):
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Get today's date in YYYYMMDD format
    today = date.today().strftime('%Y%m%d')
    
    # Create filename
    filename = f'output/diandian_hotwords_{keyword}_{today}.txt'
    
    # Save response content to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Response saved to: {filename}")


# Example usage
if __name__ == "__main__":
    keyword = "coin identifier"
    result = fetch_diandian_hot_words(keyword)
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))