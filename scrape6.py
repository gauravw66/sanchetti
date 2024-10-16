from firecrawl import FirecrawlApp
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firecrawl app with your API key
app = FirecrawlApp(api_key= os.environ.get("FIRECRAWL_API_KEY"))

# Start the crawl on the specified website
crawl_status = app.crawl_url(
    'https://sanchetihospital.org/',
    params={
        'limit': 100,
        'scrapeOptions': {'formats': ['markdown']}
    },
    poll_interval=30
)

# Check the status of the crawl
if crawl_status['status'] == 'completed':
    # Retrieve the scraped data
    scraped_data = crawl_status['data']  # Adjust key according to the actual structure

    # Define the URLs you want to exclude
    excluded_urls = [
        'https://sanchetihospital.org/category/blog/',
        'https://sanchetihospital.org/aoc/',
        'https://sanchetihospital.org/testimonials/',
        'https://sanchetihospital.org/wp-content/uploads/2022/12/Scheme.pdf',
        'https://sanchetihospital.org/blog/',
        'https://sanchetihospital.org/category/news/',
        'https://sanchetihospital.org/2020/02/14/osteoarthritis-patient/',
        'https://sanchetihospital.org/wp-content/uploads/2022/12/List-Of-Charity-Commitee.pdf',
        'https://sanchetihospital.org/wp-content/uploads/2023/10/IPF-Letter-1.pdf',
        'https://sanchetihospital.org/wp-content/uploads/2023/02/career-slider-image1-1024x465.jpg',
        'https://sanchetihospital.org/wp-content/uploads/2023/02/career-slider-image2-1024x465.jpg',
        'https://sanchetihospital.org/wp-content/uploads/2023/02/career-slider-image5-1024x465.jpg',
        'https://sanchetihospital.org/wp-content/uploads/2023/02/career-slider-image3-1024x465.jpg',
        'https://sanchetihospital.org/wp-content/uploads/2023/02/career_slider_image6-1024x465.jpg',
        'https://sanchetihospital.org/wp-content/uploads/2023/02/career-slider-image4-1024x465.jpg',
        'https://sanchetihospital.org/wp-content/uploads/2024/03/white-blue-modern-job-fair-flyer-portrait-1080-x-1350-px-819x1024.png'
    ]

    # Fields to remove
    fields_to_remove = ['robots', 'language', 'ogLocale', 'statusCode']

    # Filter out unwanted URLs, restructure the data, and remove specified fields
    filtered_data = []
    for item in scraped_data:
        if item.get('metadata', {}).get('sourceURL') not in excluded_urls:
            # Create a new dictionary with all metadata fields at the top level
            new_item = {**item.get('metadata', {}), 'markdown': item.get('markdown')}
            # Remove the original metadata field
            new_item.pop('metadata', None)
            # Remove specified fields
            for field in fields_to_remove:
                new_item.pop(field, None)
            filtered_data.append(new_item)

    # Save the filtered, restructured, and cleaned data to a file
    with open('FINAL.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    print("Filtered, restructured, and cleaned data saved to 'scraped_data5.json'")
else:
    print("Crawl not completed or failed. Status:", crawl_status['status'])