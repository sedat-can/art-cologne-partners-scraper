import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin

def main():
    print("🌐 Fetching Art Cologne partners page...")
    url = "https://www.artcologne.de/die-messe/art-cologne/partner-der-art-cologne/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"✅ Status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Failed to retrieve page. Status code: {response.status_code}")
            return
            
        soup = BeautifulSoup(response.content, 'html.parser')
        print("🔍 Parsing partner data...")
        teasers = soup.select('div.teaser.col1.corptop.t01')
        print(f"Found {len(teasers)} partner teasers")

        partners_data = []
        for teaser in teasers:
            img = teaser.find('img')
            logo_url = img.get('src', '') if img else ''
            name = img.get('alt', '').strip() if img else 'Unnamed Partner'
            name = re.sub(r'[\n\r\t]+', ' ', name)  # Clean name
            
            website = ''
            if a_tag := teaser.find('a', class_='noline'):
                website = a_tag.get('href', '')
                if website.startswith('/'):
                    website = urljoin(url, website)
            
            partners_data.append({
                "Name": name,
                "Logo URL": logo_url,
                "Website": website
            })

        if partners_data:
            print(f"\n✅ Success! Found {len(partners_data)} partners")
            df = pd.DataFrame(partners_data)
            
            # Save outputs
            df.to_csv("art_cologne_partners.csv", index=False, encoding='utf-8-sig')
            df.to_json("art_cologne_partners.json", orient='records', force_ascii=False, indent=2)
            print("💾 Saved CSV and JSON files")
            
            # Show summary
            print("\n📊 Summary:")
            print(f"Partners with logos: {df['Logo URL'].notnull().sum()}")
            print(f"Partners with websites: {df['Website'].notnull().sum()}")
        else:
            print("\n❌ No partner data extracted")
            
    except Exception as e:
        print(f"⚠️ Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
