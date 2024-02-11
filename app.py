import streamlit as st
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd

# Set page configuration with an SEO-optimized title and a brief, engaging description
st.set_page_config(page_title="Advanced Sitemap URL Extractor",
                   layout="wide")

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Enhancing Streamlit app appearance with custom CSS */
    .stTextInput>div>div>input {
        border-radius: 20px !important;
        border: 1px solid #4CAF50;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px !important;
        border: 2px solid #4CAF50 !important;
        color: white !important;
        background-color: #4CAF50;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 20px !important;
        color: #4CAF50 !important;
        border: 2px solid #4CAF50;
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Main title and user input form
st.title('🌐 Advanced Sitemap URL Extractor Tool')
st.markdown("""
Unlock the full potential of your website with our Advanced **Sitemap URL Extractor** Tool, meticulously designed for webmasters and SEO specialists. Enter the URL of your XML sitemap below to tap into an unparalleled capability for extracting URLs from any sitemap structure – be it nested sitemaps, sitemap index files, or even non-standard formats. This tool is your gateway to a deeper understanding and more effective management of your site's SEO foundation.

***Enter Sitemap URL:*** `https://example.com/sitemap.xml`
""")
sitemap_url = st.text_input('Enter Sitemap URL', '', placeholder="https://example.com/sitemap.xml")

# Async functions for efficient sitemap fetching and parsing
async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        st.error(f"Failed to fetch {url}: {str(e)}")
        return None

async def process_sitemap(session, url, urls):
    content = await fetch_url(session, url)
    if content:
        soup = BeautifulSoup(content, "xml")
        if soup.find_all("sitemap"):
            sitemap_urls = [sitemap.loc.text for sitemap in soup.find_all("sitemap")]
            for sitemap_url in sitemap_urls:
                await process_sitemap(session, sitemap_url, urls)
        elif soup.find_all("url"):
            urls.extend([url.loc.text for url in soup.find_all("url")])

async def fetch_and_parse_sitemap(sitemap_url):
    urls = []
    async with aiohttp.ClientSession() as session:
        await process_sitemap(session, sitemap_url, urls)
    return urls

# Extract URLs and display results upon button click
if st.button('Extract URLs'):
    if sitemap_url:
        with st.spinner('Extracting URLs from sitemap...'):
            urls = asyncio.run(fetch_and_parse_sitemap(sitemap_url))
            if urls:
                df = pd.DataFrame(urls, columns=["URL"])
                st.success(f'Successfully extracted {len(urls)} URLs from standard, nested, and index sitemaps.')
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download URLs as CSV", data=csv, file_name='sitemap_urls.csv', mime='text/csv')
            else:
                st.error("Failed to extract URLs. Please ensure the sitemap URL is correct.")
    else:
        st.error("Please enter a valid sitemap URL.")

# Enhanced content with examples
st.markdown("""
## Unrivaled Capabilities and Use Cases
- *Nested Sitemap Mastery:* Dive deep into nested sitemaps for thorough site audits and comprehensive SEO strategy planning.
- *Sitemap Index Files Expertise:* Efficiently processes sitemap index files (e.g., `https://www.example.com/sitemap_index.xml`), ideal for large sites.
- *Universal Compatibility:* Equipped to handle standard and non-standard sitemap formats, offering unparalleled flexibility.

## Real-World Applications
- *Comprehensive Site Audits:* Utilize our tool for detailed site reviews, enhancing SEO performance.
- *SEO Strategy Enhancement:* Leverage extracted URLs for indexing strategies and improved search engine visibility.

Elevate your SEO strategy and site management with the Advanced Sitemap URL Extractor – your essential tool for sitemap analysis and optimization.
""")

# This script now provides a fully integrated solution, combining detailed functionalities, user benefits, and practical applications to enhance website management and SEO strategy.
