import json
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI


# Load the JSON data
with open('networks.json') as f:
    data = json.load(f)


def visualize(json_data):
    # Convert JSON data to DataFrame
    df = pd.json_normalize(data)

    df = df[20:len(df)]

    # Convert ratings to float by replacing commas and changing the type
    df['rating'] = df['rating'].str.replace(',', '.').astype(float)

    # Convert score columns to float
    score_columns = ['scores.ease_of_use', 'scores.requirements', 'scores.support', 'scores.set_up']
    for col in score_columns:
        df[col] = df[col].astype(float)

    # Plot bar chart for scores
    ax = df.plot(x='name', y=score_columns, kind='bar', figsize=(15, 8))
    plt.title('Comparison of Scores for Affiliate Networks')
    plt.xlabel('Affiliate Network')
    plt.ylabel('Scores')
    plt.ylim(7, 11)
    plt.xticks(rotation=45)

    legend_labels = ['Benutzerfreundlichkeit', 'Erfüllung der Anforderungen', 'Kundensupport', 'Einfache Einrichtung']
    plt.legend(legend_labels, title='Scores')

    plt.tight_layout()

    # Show the plot
    plt.show()

def compare_affiliate_features(data):
    # Format the data into a prompt for GPT-4
    prompt = "Compare the features of the following affiliate networks and generate a comparison table:\n\n"
    
    for network in data:
        name = network.get('name')
        features = network.get('features', {})
        
        if isinstance(features, dict):
            features_str = "\n".join([f"{key}: {', '.join(value)}" if isinstance(value, list) else f"{key}: {value}" for key, value in features.items()])
        else:
            features_str = features  # Handle the case where features is a string
        
        prompt += f"Network: {name}\nFeatures:\n{features_str}\n\n"

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
        )

    # Extract the response text
    result = completion.choices[0].message

    return result

comp_table = compare_affiliate_features(data)
print(comp_table)