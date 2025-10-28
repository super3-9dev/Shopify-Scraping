import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from urllib.parse import urljoin

class ShopifyProductScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.products_data = []
    
    def scrape_data(self, url):
        """Fetch and parse webpage content"""
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def scrape_product_links(self, url):
        """Extract product links from category page"""
        soup = self.scrape_data(url)
        if not soup:
            return []
        
        # Look for product links - adjust selectors based on the actual site structure
        product_links = []
        
        # Common selectors for product links
        selectors = ['a[class*="b-picture__link"]']
        
        for selector in selectors:
            links = soup.select(selector)
            if links:
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(self.base_url, href)
                        if full_url not in product_links:
                            product_links.append(full_url)
                break
        
        print(f"Found {len(product_links)} product links")
        return product_links
    
    def scrape_product_details(self, product_url):
        """Extract detailed product information"""
        soup = self.scrape_data(product_url)
        if not soup:
            return None
        
        try:
            # Extract product information - adjust selectors based on actual site
            product_data = {
                'ID': '',
                'Handle': '',
                'Command': 'MERGE',
                'Title': '',
                'Body HTML': '',
                'Vendor': 'My Store',
                'Status': 'Active',
                'Published': 'TRUE',
                'Image Src': '',
                'Image Command': 'MERGE',
                'Option1 Name': 'Color',
                'Option1 Value': 'White',
                'Option2 Name': '',
                'Option2 Value': '',
                'Option3 Name': '',
                'Option3 Value': '',
                'Variant SKU': '',
                'Variant Image': '',
                'Variant Price': '',
                'Variant Compare At Price': '',
                'Variant Inventory Qty': '',
                # You can change the tags to the appropriate tags for the product
                'Tags': 'men'
            }
            
            # Extract title
            title_selectors = ['.b-product__name-text']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    product_data['Title'] = title_elem.get_text(strip=True)
                    break
            
            # Extract price
            price_selectors = ['.b-price__value']
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Extract numeric price
                    import re
                    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                    if price_match:
                        product_data['Variant Price'] = price_match.group()
                    break

            # Extract Body HTML
            desc_selectors = ['.b-bnr__content-markup-field']
            desc_elem = None
            for selector in desc_selectors:
                possible = soup.select_one(selector)
                if possible:
                    desc_elem = possible
                    break
            if desc_elem:
                product_data['Body HTML'] = desc_elem  # Limit length

            # Extract up to 3 images with the same class name from the product page
            images = []
            img_selector = '.b-product-images__picture-holder .b-picture__image'
            img_elements = soup.select(img_selector)    
            for img in img_elements[:3]:  # Get up to 3 images
                img_url = img.get('src')
                img_url = img_url.split('?')[0]
                images.append(img_url)
            # 
            # Set the first image as the main image
            product_data['Image Src'] = images[0] + '; ' + images[1]

            # Generate Handle and ID
            product_data['Handle'] = title_elem.get_text(strip=True).lower().replace(' ', '-').replace('.', '-')
            product_data['ID'] = f"650000000000{len(self.products_data) + 1}"
            product_data['Variant Inventory Qty'] = random.randint(1, 5)
            
            return product_data
            
        except Exception as e:
            print(f"Error extracting product data from {product_url}: {e}")
            return None
    
    def scrape_all_products(self, category_url):
        """Scrape all products from a category"""
        print("Starting product scraping...")
        
        # Get product links
        product_links = self.scrape_product_links(category_url)
        if not product_links:
            print("No product links found!")
            return
        cnt = 0;
        for product_link in product_links:
            product_data = self.scrape_product_details(product_link)
            if product_data:
                self.products_data.append(product_data)
                cnt += 1;
                print(f"Scraped product ({cnt}/{len(product_links)}): {product_data['Title']}")
            else:
                print(f"Failed to scrape product: {product_link}")
       
        print(f"Scraped {len(self.products_data)} products successfully!")
    
    def save_to_excel(self, filename='shopify_products.xlsx'):
        """Save scraped data to Excel file"""
        if not self.products_data:
            print("No data to save!")
            return
        
        # Create data folder if it doesn't exist
        data_folder = 'Data'
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        
        # Create full path for the file
        file_path = os.path.join(data_folder, filename)

        df = pd.DataFrame(self.products_data)
        df.to_excel(file_path, index=False, engine='openpyxl')
        print(f"Data saved to {file_path}")
def main():
    # Initialize scraper
    base_url = "https://www.graff.com"
    category_url = "https://www.graff.com/international-ar/jewellery-collections/view-by-category/bracelets-bangles/?srsltid=AfmBOophdsSHO0hJneZUY-T_jmj-bmmxB3T2GY7Izylx1xK0jzUEXRSV"
    scraper = ShopifyProductScraper(base_url)
    # Scrape products
    scraper.scrape_all_products(category_url)
    # Save to both Excel and CSV
    # scraper.save_to_excel('amorethica_products.xlsx')

    # Display summary
    if scraper.products_data:
        print(f"\nScraping Summary:")
        print(f"Total products: {len(scraper.products_data)}")

if __name__ == "__main__":
    main()