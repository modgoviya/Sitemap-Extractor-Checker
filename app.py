import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests  # Use requests instead of aiohttp
##
# Set page configuration with an SEO-optimized title and a brief, engaging description
st.set_page_config(page_title="Advanced Sitemap URL Extractor", layout="wide")

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

def fetch_and_parse_sitemap(sitemap_url):
    urls = []
    try:
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "xml")
            if soup.find_all("sitemap"):
                for sitemap in soup.find_all("sitemap"):
                    sitemap_response = requests.get(sitemap.loc.text)
                    sitemap_soup = BeautifulSoup(sitemap_response.content, "xml")
                    urls.extend([url.loc.text for url in sitemap_soup.find_all("url")])
            elif soup.find_all("url"):
                urls.extend([url.loc.text for url in soup.find_all("url")])
        return urls
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch or parse the sitemap: {str(e)}")
        return []

# Extract URLs and display results upon button click
if st.button('Extract URLs'):
    if sitemap_url:
        with st.spinner('Extracting URLs from sitemap...'):
            urls = fetch_and_parse_sitemap(sitemap_url)
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
#tracking
st.markdown("""
<!-- Default Statcounter code for Advanced Sitemap URL
Extractor T
https://advanced-sitemap-url-extractor.streamlit.app/ -->
<script type="text/javascript">
var sc_project=12966452; 
var sc_invisible=1; 
var sc_security="310e178d"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics"
href="https://statcounter.com/" target="_blank"><img
class="statcounter"
src="https://c.statcounter.com/12966452/0/310e178d/1/"
alt="Web Analytics"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->
""", unsafe_allow_html=True)
