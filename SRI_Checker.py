import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TIMEOUT = 10

def fetch_page(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=TIMEOUT, verify=False)
        return response.text
    except Exception as e:
        print(f"  Error fetching {url}: {str(e)[:100]}")
        return None

def is_external(resource_url, base_url):
    try:
        base_domain = urlparse(base_url).netloc.replace("www.", "")
        resource_domain = urlparse(resource_url).netloc.replace("www.", "")
        return base_domain != resource_domain
    except:
        return False

def check_sri(url):
    result = {
        "domain": url,
        "sri_missing": [],
        "status": "ok"
    }

    html = fetch_page(url)
    if not html:
        result["status"] = "failed_to_fetch"
        return result

    soup = BeautifulSoup(html, "html.parser")

    seen = set()  # for deduplication

    # Check scripts
    for tag in soup.find_all("script", src=True):
        src = tag.get("src")
        integrity = tag.get("integrity")

        if src and not integrity:
            full_url = urljoin(url, src)

            if is_external(full_url, url):
                key = ("script", full_url)
                if key not in seen:
                    seen.add(key)
                    result["sri_missing"].append({
                        "type": "script",
                        "resource": full_url
                    })

    # Check stylesheets
    for tag in soup.find_all("link", rel="stylesheet"):
        href = tag.get("href")
        integrity = tag.get("integrity")

        if href and not integrity:
            full_url = urljoin(url, href)

            if is_external(full_url, url):
                key = ("stylesheet", full_url)
                if key not in seen:
                    seen.add(key)
                    result["sri_missing"].append({
                        "type": "stylesheet",
                        "resource": full_url
                    })

    # Optional: fonts (external only)
    for tag in soup.find_all("link"):
        href = tag.get("href")
        rel = tag.get("rel")

        if href and rel and "preload" in rel:
            if "font" in tag.get("as", ""):
                integrity = tag.get("integrity")
                full_url = urljoin(url, href)

                if not integrity and is_external(full_url, url):
                    key = ("font", full_url)
                    if key not in seen:
                        seen.add(key)
                        result["sri_missing"].append({
                            "type": "font",
                            "resource": full_url
                        })

    if result["sri_missing"]:
        result["status"] = "vulnerable"

    return result

def normalize_domain(domain):
    domain = domain.strip()

    if not domain.startswith("http"):
        domain = "https://" + domain

    return domain

def main():
    input_file = "domains.txt"
    output_file = "sri_results.json"

    results = []

    with open(input_file, "r") as f:
        domains = f.readlines()

    for domain in domains:
        domain = domain.strip()
        if not domain:
            continue

        url = normalize_domain(domain)

        print(f"Checking: {url}")
        try:
            res = check_sri(url)
            results.append(res)
        except Exception as e:
            print(f"  Error checking {url}: {str(e)[:100]}")
            results.append({
                "domain": url,
                "sri_missing": [],
                "status": f"error: {str(e)[:50]}"
            })

        time.sleep(0.5)

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\nDone. Results saved to {output_file}")

if __name__ == "__main__":
    main()
