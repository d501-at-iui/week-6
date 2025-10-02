#!/usr/bin/env python3
"""
Test script for the bonus exercise
Tests both the basic and multiprocessing versions with a small sample
"""

from apputil import Genius
import os

def test_basic_functionality():
    """Test basic functionality with a small sample."""
    print("🧪 Testing Basic Functionality")
    print("=" * 40)
    
    # Test loading artists
    if os.path.exists('artists_list.txt'):
        with open('artists_list.txt', 'r') as f:
            lines = f.readlines()
            artists_count = len([line.strip() for line in lines if line.strip() and not line.startswith('#')])
        print(f"✅ Artists file contains {artists_count} artists")
    else:
        print("❌ artists_list.txt not found")
        return False
    
    # Test Genius API
    try:
        genius = Genius.from_env_file('env-1.env')
        print("✅ Genius API client initialized")
        
        # Test with a small sample
        test_artists = ['The Beatles', 'Radiohead', 'Beyoncé']
        print(f"\n🔄 Testing with sample artists: {test_artists}")
        
        result = genius.get_artists(test_artists)
        
        # Handle both DataFrame and list results
        if hasattr(result, 'empty'):
            # It's a pandas DataFrame
            result_len = len(result)
            print(f"✅ API call successful, got {result_len} results")
            if not result.empty:
                sample = result.iloc[0].to_dict()
                print(f"📋 Sample result: search_term='{sample.get('search_term')}', artist_name='{sample.get('artist_name')}'")
        else:
            # It's a list
            result_len = len(result) if result else 0
            print(f"✅ API call successful, got {result_len} results")
            if result:
                sample = result[0]
                print(f"📋 Sample result: search_term='{sample.get('search_term')}', artist_name='{sample.get('artist_name')}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def main():
    """Run tests and provide usage instructions."""
    print("🎵 Bonus Exercise Test & Usage Guide")
    print("=" * 50)
    
    # Test basic functionality
    if test_basic_functionality():
        print("\n✅ All tests passed!")
        
        print("\n📖 USAGE INSTRUCTIONS:")
        print("=" * 50)
        
        print("\n1️⃣  BASIC VERSION (Sequential):")
        print("   python collect_artist_data.py")
        print("   • Processes artists one by one")
        print("   • Safer for API rate limits")
        print("   • Good for smaller lists")
        
        print("\n2️⃣  MULTIPROCESSING VERSION (Parallel):")
        print("   python collect_artist_data_multiprocessing.py")
        print("   • Processes artists in parallel")
        print("   • Faster for large lists")
        print("   • Uses multiple CPU cores")
        
        print("\n📁 FILES CREATED:")
        print("   • artists_list.txt - List of 100+ artists")
        print("   • artist_data_[timestamp].csv - Results from basic version")
        print("   • artist_data_multiprocessing_[timestamp].csv - Results from MP version")
        
        print("\n⚠️  IMPORTANT NOTES:")
        print("   • Make sure env-1.env exists with your ACCESS_TOKEN")
        print("   • API calls require internet connection")
        print("   • Be respectful of API rate limits")
        print("   • Multiprocessing version is faster but uses more resources")
        
    else:
        print("\n❌ Tests failed. Please check your setup:")
        print("   • Ensure env-1.env file exists")
        print("   • Verify ACCESS_TOKEN is valid")
        print("   • Check internet connection")

if __name__ == "__main__":
    main()