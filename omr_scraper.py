import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def scrape_networks():

    link_urls = []
    names = []    
    rating_list = []
    reviews_list = []
    price_list = []

    base_url = 'https://omr.com'

    for i in range(1,3):
        if i == 1:
            url = 'https://omr.com/de/reviews/category/affiliate-networks?sortby=weighted_score&ratings=better&ratings=best'
        else:
            url = f'https://omr.com/de/reviews/category/affiliate-networks/{i}?sortby=weighted_score&ratings=better&ratings=best'

        response = requests.get(url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            #print(soup)
            links = soup.find_all('span', attrs={'data-testid': 'product-name'})
            ratings = soup.find_all('div', attrs={'data-testid': 'product-rating'})
            prices = soup.find_all('span', attrs={'data-testid': 'product-list-item-widget-pricing-info'})

            if links:
                for link in links:
                    names.append(link.a.text.strip())
                    link_urls.append(base_url+link.a['href'])
                    #print(base_url+link.a['href'])
            
            if ratings:
                for rating in ratings:
                    rating_list.append([s for s in re.findall(r'\b\d+(?:,\d+)*\b', rating.text)][0])
                    reviews_list.append([s for s in re.findall(r'\b\d+(?:,\d+)*\b', rating.text)][1])
                    #print(rating_list)

            if prices:
                
                for price in prices:
                    price_list.append(price.text)
                    #print(price.text)
            
        else:
            return f"Failed to retrieve the webpage. Status code: {response.status_code}"

    # Create the list of dictionaries
    networks = [
        {"url": url, "name": name, "rating": rating, "reviews": reviews, "price": price}
        for url, name, rating, reviews, price in zip(link_urls, names, rating_list, reviews_list, price_list)
    ]

    #print(networks)
    # Create DataFrame
    df = pd.DataFrame(networks)

    return df


def scrape_scores(url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scores = soup.find(attrs={'id':re.compile(r'^scores')})
        if scores:
            ease_of_use = scores.find(attrs={'data-testid': 'product-ease-of-use-score'}).div.text.strip()
            requirements = scores.find(attrs={'data-testid': 'product-requirements-score'}).div.text.strip()
            support = scores.find(attrs={'data-testid': 'product-customer-support-score'}).div.text.strip()
            set_up = scores.find(attrs={'data-testid': 'product-ease-of-setup-score'}).div.text.strip()

            results = {
                'ease_of_use': ease_of_use,
                'requirements': requirements,
                'support': support,
                'set_up': set_up
            }
            return results
        else:
            return "No scores found"
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


def scrape_features(url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        features = soup.find(attrs={'class':'feature-wrapper'})
        if features:
            features_list_raw = [feat.strip() for feat in features.text.split('\n')]
            use_cases = []
            commission = []
            tracking = []
            support = []
            network = []
            control = []
            link_options = []
            utility = []
            
            header = ''
            for feat in features_list_raw:
                if feat == 'Use-Case Affiliate Netzwerke':
                    header = feat
                    continue
                
                if feat == 'Provisionsarten':
                    header = feat
                    continue

                if feat == 'Kontrolle':
                    header = feat
                    continue

                if feat == 'Tracking Arten':
                    header = feat
                    continue

                if feat == 'Tracking Options':
                    header = feat
                    continue

                if feat == 'Support Kanäle':
                    header = feat
                    continue

                if feat == 'Network':
                    header = feat
                    continue

                if feat == 'Link Options':
                    header = feat
                    continue

                if feat == 'Utility':
                    header = feat
                    continue

                if header == 'Use-Case Affiliate Netzwerke':
                    use_cases.append(feat)

                if header == 'Provisionsarten':
                    commission.append(feat)

                if header == 'Tracking Arten' or 'Tracking Options':
                    tracking.append(feat)

                if header == 'Support Kanäle':
                    support.append(feat)

                if header == 'Network':
                    network.append(feat)

                if header == 'Kontrolle':
                    control.append(feat)

                if header == 'Link Options':
                    link_options.append(feat)

                if header == 'Utility':
                    utility.append(feat)

                if header == 'Tracking Options':
                    tracking.append(feat)

            
            
            use_cases = [x for x in use_cases if x and 'Item' not in x]
            commission = [x for x in commission if x and 'Item' not in x]
            tracking = [x for x in tracking if x and 'Item' not in x]
            support = [x for x in support if x and 'Item' not in x]
            network = [x for x in network if x and 'Item' not in x]
            control = [x for x in control if x and 'Item' not in x]
            link_options = [x for x in link_options if x and 'Item' not in x]
            utility = [x for x in utility if x and 'Item' not in x]


            result = {
                'use_cases': list(set(use_cases)),
                'commission': list(set(commission)),
                'tracking': list(set(tracking)),
                'support': list(set(support)),
                'network_type': list(set(network)),
                'control': list(set(control)),
                'link_options': list(set(link_options)),
                'utility': list(set(utility))
            }

            print(result)
            return result
        else:
            return "No features found"
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

def save_dicts_to_json(dict_list, file_path):
    """
    Save a list of dictionaries to a JSON file.

    Parameters:
    dict_list (list): List of dictionaries to be saved.
    file_path (str): Path to the JSON file to save the data.
    """
    try:
        with open(file_path, 'w') as json_file:
            json.dump(dict_list, json_file, indent=4)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving data to JSON file: {e}")


#url = 'https://omr.com/de/reviews/product/awin#overview'

#scores = scrape_scores(url)
#print(scores)

def df_to_dict(df):
    
    networks = []

    for index, row in df.iterrows():

        network = {}

        #print(row)
        url = row['url']
        scores = scrape_scores(url)
        features = scrape_features(url)

        network['name'] = row['name']
        network['rating'] = row['rating']
        network['reviews'] = row['reviews']
        network['scores'] = scores
        network['features'] = features

        networks.append(network)

    return networks



#Loop through all the OMR links and save data to JSON file
df = pd.read_excel('networks_omr.xlsx')
networks = df_to_dict(df)
save_dicts_to_json(networks, 'networks.json')



#df = scrape_networks()

# Write DataFrame to Excel
#excel_file_path = 'networks_omr.xlsx'
#df.to_excel(excel_file_path, index=True)