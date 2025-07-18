import requests
import xml.etree.ElementTree as ET

def get_recent_sec_filings(num_filings=5):
    """
    Fetches the most recent SEC EDGAR filings from the RSS feed
    and extracts key information.

    Args:
        num_filings (int): The number of recent filings to retrieve.

    Returns:
        list: A list of dictionaries, where each dictionary represents a filing
              with 'company_name', 'form_type', 'filing_date', and 'link'.
              Returns an empty list if an error occurs.
    """
    # SEC EDGAR RSS feed URL for current filings
    # The 'count' parameter can be adjusted, but we'll process up to num_filings
    # from the fetched feed.
    rss_feed_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&output=atom&count={num_filings * 2}" # Fetch a bit more to ensure we get enough

    recent_filings = []

    # Define a User-Agent header and a From header.
    # The SEC's guidelines for automated access often recommend including
    # an email address in the User-Agent or From header to identify the requestor.
    # Replace 'your_email@example.com' with your actual email address.
    headers = {
        'User-Agent': 'MyApp/1.0 (guy@myapp.com)', # Example: 'MySECAlertApp/1.0 (john.doe@example.com)'
        'From': 'guy@myapp.com' # Replace with your email
    }

    try:
        # Send a GET request to the RSS feed URL with the User-Agent and From headers
        response = requests.get(rss_feed_url, headers=headers, timeout=10) # Add a timeout for robustness
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the XML content of the RSS feed
        root = ET.fromstring(response.content)

        # The RSS feed uses Atom format, so we need to use namespaces
        # Find all 'entry' elements which represent individual filings
        # Atom namespace: http://www.w3.org/2005/Atom
        # SEC namespace: http://www.sec.gov/Archives/edgar
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            if len(recent_filings) >= num_filings:
                break # Stop once we have enough filings

            company_name = ''
            form_type = ''
            filing_date = ''
            filing_link = ''

            # Extract company name from 'title' tag
            title_element = entry.find('{http://www.w3.org/2005/Atom}title')
            if title_element is not None:
                # The title typically contains "Company Name - Form Type"
                # We'll try to split it to get the company name
                title_text = title_element.text
                if ' - ' in title_text:
                    company_name = title_text.split(' - ')[0].strip()
                    form_type = title_text.split(' - ')[1].strip()
                else:
                    company_name = title_text.strip() # Fallback if format is different

            # Extract filing date from 'updated' tag
            updated_element = entry.find('{http://www.w3.org/2005/Atom}updated')
            if updated_element is not None:
                # Date format is typically ISO 8601 (e.g., 2023-10-26T16:30:00-04:00)
                # We just want the date part
                filing_date = updated_element.text.split('T')[0] if 'T' in updated_element.text else updated_element.text

            # Extract filing link from 'link' tag where type is 'text/html'
            for link_element in entry.findall('{http://www.w3.org/2005/Atom}link'):
                if link_element.get('type') == 'text/html':
                    filing_link = link_element.get('href')
                    break # Found the main link

            # Only add if we have a link and at least a company name
            if filing_link and company_name:
                recent_filings.append({
                    'company_name': company_name,
                    'form_type': form_type,
                    'filing_date': filing_date,
                    'link': filing_link
                })

    except requests.exceptions.RequestException as e:
        print(f"Error fetching SEC EDGAR RSS feed: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML from SEC EDGAR RSS feed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return recent_filings

if __name__ == "__main__":
    print("Fetching the 5 most recent SEC EDGAR filings...\n")
    filings = get_recent_sec_filings(num_filings=5)

    if filings:
        for i, filing in enumerate(filings):
            print(f"--- Filing {i + 1} ---")
            print(f"Company: {filing.get('company_name', 'N/A')}")
            print(f"Form Type: {filing.get('form_type', 'N/A')}")
            print(f"Date: {filing.get('filing_date', 'N/A')}")
            print(f"Link: {filing.get('link', 'N/A')}\n")
    else:
        print("No filings retrieved or an error occurred.")

