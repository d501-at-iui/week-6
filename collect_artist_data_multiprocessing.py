#!/usr/bin/env python3
"""
Bonus Exercise Script - Multiprocessing Version
Collects artist data using the Genius API with parallel processing for improved performance

This script:
1. Reads artists from artists_list.txt
2. Uses multiprocessing to parallelize API calls
3. Collects data efficiently using worker processes
4. Saves results to a CSV file with performance metrics
"""

import csv
import time
import multiprocessing as mp
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
import os
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

def process_artist_batch(artist_batch: list, env_file: str = 'env-1.env') -> list:
    """
    Process a batch of artists in a single worker process.
    Each worker gets its own Genius client instance.
    """
    try:
        # Initialize Genius client for this worker process
        genius = Genius.from_env_file(env_file)
        
        # Process the batch of artists
        result = genius.get_artists(artist_batch)
        
        # Convert to list of dicts if it's a DataFrame
        if hasattr(result, 'to_dict'):
            return result.to_dict('records')
        else:
            return result
            
    except Exception as e:
        print(f"❌ Error in worker process: {e}")
        # Return empty results for failed batch
        return [{'search_term': artist, 'artist_name': 'N/A', 'artist_id': 'N/A', 'followers_count': 'N/A'} 
                for artist in artist_batch]

def chunk_list(lst: list, chunk_size: int) -> list:
    """Split a list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def save_to_csv(data: list, filename: str):
    """Save the artist data to a CSV file."""
    if not data:
        print("❌ No data to save!")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['search_term', 'artist_name', 'artist_id', 'followers_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(data)
            
        print(f"✅ Data saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")

def main():
    """Main function with multiprocessing optimization."""
    print("🎵 Starting Bonus Exercise - Multiprocessing Artist Data Collection")
    print("=" * 70)
    
    # Load artists from file
    artists = load_artists_from_file('artists_list.txt')
    if not artists:
        return
    
    # Configuration
    num_workers = min(mp.cpu_count(), 4)  # Limit workers to be respectful to API
    batch_size = max(5, len(artists) // (num_workers * 2))  # Dynamic batch size
    
    print(f"📋 Processing {len(artists)} artists...")
    print(f"⚙️  Workers: {num_workers}")
    print(f"📦 Batch size: {batch_size}")
    
    # Test API connection first
    try:
        test_genius = Genius.from_env_file('env-1.env')
        print("✅ Genius API client test successful")
    except Exception as e:
        print(f"❌ Error initializing Genius client: {e}")
        print("💡 Make sure your env-1.env file exists with ACCESS_TOKEN")
        return
    
    # Split artists into batches
    artist_batches = chunk_list(artists, batch_size)
    print(f"🔄 Created {len(artist_batches)} batches for processing")
    
    # Record start time
    start_time = time.time()
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_results = []
    completed_batches = 0
    
    try:
        # Use ProcessPoolExecutor for multiprocessing
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            # Submit all batches
            future_to_batch = {
                executor.submit(process_artist_batch, batch, 'env-1.env'): batch 
                for batch in artist_batches
            }
            
            # Process completed batches
            for future in as_completed(future_to_batch):
                try:
                    batch_result = future.result()
                    all_results.extend(batch_result)
                    completed_batches += 1
                    
                    # Progress update
                    progress = (completed_batches / len(artist_batches)) * 100
                    print(f"📈 Progress: {completed_batches}/{len(artist_batches)} batches ({progress:.1f}%)")
                    
                except Exception as e:
                    print(f"❌ Batch failed: {e}")
        
        # Generate output filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'artist_data_multiprocessing_{timestamp}.csv'
        
        # Save to CSV
        save_to_csv(all_results, output_file)
        
        # Calculate and display statistics
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 70)
        print("📊 MULTIPROCESSING COLLECTION COMPLETE!")
        print(f"⏱️  Total time: {duration:.2f} seconds")
        print(f"🚀 Speed: {len(artists)/duration:.2f} artists/second")
        print(f"📁 Output file: {output_file}")
        print(f"🎯 Artists processed: {len(artists)}")
        print(f"🔧 Workers used: {num_workers}")
        
        if all_results:
            successful = len([row for row in all_results if row.get('artist_name', 'N/A') != 'N/A'])
            print(f"✅ Successful matches: {successful}")
            print(f"❌ Failed matches: {len(all_results) - successful}")
            print(f"📈 Success rate: {(successful/len(all_results)*100):.1f}%")
        
        # Performance comparison note
        estimated_serial_time = len(artists) * 0.2  # Rough estimate
        speedup = estimated_serial_time / duration if duration > 0 else 1
        print(f"⚡ Estimated speedup vs serial: {speedup:.1f}x")
        
    except Exception as e:
        print(f"❌ Error during multiprocessing collection: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ensure proper multiprocessing setup on all platforms
    mp.set_start_method('spawn', force=True)
    main()