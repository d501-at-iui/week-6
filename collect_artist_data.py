#!/usr/bin/env python3
"""
Bonus Exercise Script - Basic Version
Collects artist data using the Genius API and saves to CSV

This script:
1. Reads artists from artists_list.txt
2. Uses the Genius.get_artists() method to fetch data
3. Saves results to a CSV file
"""

import csv
import time
from datetime import datetime
from apputil import Genius

def load_artists_from_file(filename: str) -> list:
    """Load artist names from a text file, filtering out comments and empty lines."""
    artists = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    artists.append(line)
        print(f"✅ Loaded {len(artists)} artists from {filename}")
        return artists
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found!")
        return []

def save_to_csv(data, filename: str):
    """Save the artist data to a CSV file."""
    if not data:
        print("❌ No data to save!")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Get column names from the first row
            fieldnames = data[0].keys() if isinstance(data[0], dict) else ['search_term', 'artist_name', 'artist_id', 'followers_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            if isinstance(data[0], dict):
                # If data is already in dict format
                writer.writerows(data)
            else:
                # If data is a pandas DataFrame, convert to dict
                for row in data:
                    writer.writerow(row)
            
        print(f"✅ Data saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")

def main():
    """Main function to orchestrate the data collection process."""
    print("🎵 Starting Bonus Exercise - Artist Data Collection")
    print("=" * 60)
    
    # Load artists from file
    artists = load_artists_from_file('artists_list.txt')
    if not artists:
        return
    
    print(f"📋 Processing {len(artists)} artists...")
    
    # Initialize Genius API client
    try:
        genius = Genius.from_env_file('env-1.env')
        print("✅ Genius API client initialized")
    except Exception as e:
        print(f"❌ Error initializing Genius client: {e}")
        print("💡 Make sure your env-1.env file exists with ACCESS_TOKEN")
        return
    
    # Record start time
    start_time = time.time()
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Use the get_artists method to process all artists
        print("\n🔄 Fetching artist data from Genius API...")
        result = genius.get_artists(artists)
        
        # Generate output filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'artist_data_{timestamp}.csv'
        
        # Save to CSV
        if hasattr(result, 'to_dict'):
            # If it's a pandas DataFrame
            data = result.to_dict('records')
        else:
            # If it's already a list of dictionaries
            data = result
            
        save_to_csv(data, output_file)
        
        # Calculate and display statistics
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("📊 COLLECTION COMPLETE!")
        print(f"⏱️  Total time: {duration:.2f} seconds")
        print(f"📁 Output file: {output_file}")
        print(f"🎯 Artists processed: {len(artists)}")
        
        if data:
            successful = len([row for row in data if row.get('artist_name', 'N/A') != 'N/A'])
            print(f"✅ Successful matches: {successful}")
            print(f"❌ Failed matches: {len(data) - successful}")
            print(f"📈 Success rate: {(successful/len(data)*100):.1f}%")
        
    except Exception as e:
        print(f"❌ Error during data collection: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()