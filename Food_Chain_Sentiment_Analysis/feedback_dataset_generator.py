#!/usr/bin/env python
# coding: utf-8

# In[3]:


import csv
import random
from datetime import datetime, timedelta

# Feedback templates with placeholders
feedback_templates = [
    "The {aspect} was {adjective}, really made my day!",
    "I felt that the {aspect} could be more {adjective}.",
    "The staff were {behavior}, which {effect}.",
    "Having {feature} is great, it {benefit}.",
    "{dish} was {adjective}, just like you'd expect at a good restaurant.",
    "The atmosphere is {adjective}, it {effect} when you dine.",
    "I found the {aspect} to be {adjective}, which is {evaluation}.",
    "A bit disappointed with the {aspect}, was expecting something more {adjective}.",
    "It's {adjective} how the restaurant manages to {achievement}.",
    "{aspect} was top-notch, {compliment}.",
    # Add more templates as needed
]

# Words to fill the placeholders
aspects = ['service', 'food quality', 'ambience', 'price', 'menu variety']
adjectives = ['amazing', 'disappointing', 'excellent', 'mediocre', 'impressive', 'lacking']
behaviors = ['helpful and courteous', 'indifferent', 'rude', 'welcoming']
effects = ['enhances the dining experience', 'puts a damper on the meal', 'leaves a lot to be desired']
features = ['an online reservation system', 'valet parking', 'live music', 'outdoor seating']
benefits = ['adds a lot of convenience', 'makes me want to come back', 'is a unique touch']
dishes = ['The seafood platter', 'The vegan burger', 'The homemade pasta', 'The rib-eye steak']
evaluations = ['commendable', 'something I value', 'disappointing to see', 'worth mentioning']
achievements = ['keep such high standards', 'offer a diverse menu', 'retain a loyal clientele']
compliments = ['I will be coming back again', 'I would recommend to my friends', 'that deserves praise']

# Function to generate random dates
def generate_random_date():
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2023, 1, 1)
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")


# Function to generate a single feedback string
def generate_feedback():
    template = random.choice(feedback_templates)
    feedback = template.format(
        aspect=random.choice(aspects),
        adjective=random.choice(adjectives),
        behavior=random.choice(behaviors),
        effect=random.choice(effects),
        feature=random.choice(features),
        benefit=random.choice(benefits),
        dish=random.choice(dishes),
        evaluation=random.choice(evaluations),
        achievement=random.choice(achievements),
        compliment=random.choice(compliments)
    )
    return feedback


# Function to generate feedback data including additional fields
def generate_feedback_data(num_records):
    feedback_data = []
    for i in range(num_records):
        restaurant_number = f"{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        location = f"{random.choice(['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Barrie', 'Mississauga', 'Hamilton', 'North York', 'Markham', 'Richmond Hill'])}, Canada"
        feedback = generate_feedback()
        date_posted = generate_random_date()
        feedback_data.append({
            'restaurant_number': restaurant_number,
            'location': location,
            'feedback': feedback,
            'date_posted': date_posted
        })
    return feedback_data

# Function to write the dataset to a CSV file
def write_to_csv(file_name, data):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['restaurant_number', 'location', 'feedback', 'date_posted']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)


# Main function to generate feedback dataset and write to CSV
def main():
    num_records = 1000
    file_name = 'feedback_data.csv'
    feedback_dataset = generate_feedback_data(num_records)  # Use the correct function here
    write_to_csv(file_name, feedback_dataset)
    print(f"{num_records} feedback records have been written to {file_name}")

# Run the main function
if __name__ == "__main__":
    main()