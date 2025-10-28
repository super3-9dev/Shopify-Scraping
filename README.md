# eCommerce Web Scraper for Shopify

A comprehensive web scraping solution for extracting product data from eCommerce websites and formatting it for Shopify import. This project includes tools for both scraping live websites and processing existing data files.

## 🚀 Features

- **Web Scraping**: Extract product data from eCommerce websites
- **Excel Support**: Full .xlsx file support with formatting
- **Shopify Format**: Data structured to match Shopify product import requirements
- **Multiple Formats**: Export to both Excel (.xlsx) and CSV formats
- **Data Processing**: Convert existing data to Shopify format
- **Error Handling**: Robust error handling and logging
- **Sample Data**: Generate sample data for testing

## 📁 Files Overview

- `index.py` - Main web scraper for live websites
- `excel_utils.py` - Utilities for processing Excel/CSV files
- `create_sample_data.py` - Generate sample Shopify product data
- `requirements.txt` - Python dependencies

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd eCommerce-webscraper-Shopify
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### 1. Web Scraping (Live Websites)

Scrape products from a live website:

```bash
python index.py
```

This will:
- Scrape products from the configured URL
- Extract product details (name, price, description, images)
- Save data in both Excel and CSV formats
- Format data to match Shopify import requirements

### 2. Process Existing Data

Convert your existing data to Shopify format:

```python
from excel_utils import ExcelProcessor

# Load your existing file
processor = ExcelProcessor()
processor.load_excel('your_file.xlsx')  # or .csv

# Standardize to Shopify format
processor.standardize_shopify_format()

# Save formatted data
processor.save_to_excel('formatted_products.xlsx')
```

### 3. Generate Sample Data

Create sample data for testing:

```bash
python create_sample_data.py
```

This creates sample product data matching the format from your image.

## 📊 Data Format

The scraper generates data in the standard Shopify product import format with all required columns:

- **Basic Info**: ID, SKU, Name, Title, Description
- **Product Details**: Type, Vendor, Tags, Status
- **Variants**: Price, Inventory, Weight, Shipping
- **Images**: Image URLs and positioning
- **SEO**: Title, Description, Google Shopping fields
- **Options**: Product variants and options

## 🔧 Configuration

### Customizing the Scraper

Edit `index.py` to change:
- Target website URL
- CSS selectors for product elements
- Data extraction logic
- Output file names

### Customizing Data Processing

Edit `excel_utils.py` to:
- Modify column mappings
- Add custom data transformations
- Change output formatting

## 📋 Example Output

The scraper creates data like this:

| Name | Variant Price | Description | Image Src | Status |
|------|---------------|-------------|-----------|---------|
| Class Ring (Gold) | 100.00 | Beautiful gold class ring | https://... | active |
| Pearl Ring | 100.00 | Elegant pearl ring | https://... | active |

## 🚨 Important Notes

- **Rate Limiting**: The scraper includes delays between requests to be respectful
- **Error Handling**: Failed requests are logged and skipped
- **Data Validation**: Generated data includes required Shopify fields
- **File Formats**: Supports both .xlsx and .csv output

## 📝 Requirements

- Python 3.7+
- requests
- beautifulsoup4
- pandas
- openpyxl
- lxml

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.
