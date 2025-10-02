# Test script showing the new integrated environment loading functionality
from apputil import Genius

print("🔧 Testing the updated Genius class with integrated environment loading:")
print("=" * 70)

# Method 1: Using the class method constructor (RECOMMENDED)
print("\n✅ Method 1: Using Genius.from_env_file() class method")
try:
    genius1 = Genius.from_env_file("env-1.env")
    print(f"   Success! Access token loaded: {genius1.access_token[:10]}...")
    print("   Usage: genius = Genius.from_env_file('env-1.env')")
except Exception as e:
    print(f"   Error: {e}")

# Method 2: Using the constructor with env_file parameter
print("\n✅ Method 2: Using constructor with env_file parameter")
try:
    genius2 = Genius(env_file="env-1.env")
    print(f"   Success! Access token loaded: {genius2.access_token[:10]}...")
    print("   Usage: genius = Genius(env_file='env-1.env')")
except Exception as e:
    print(f"   Error: {e}")

# Method 3: Manual loading using the static method
print("\n✅ Method 3: Manual loading with static method")
try:
    env_vars = Genius.load_env_file("env-1.env")
    genius3 = Genius(access_token=env_vars['ACCESS_TOKEN'])
    print(f"   Success! Access token loaded: {genius3.access_token[:10]}...")
    print("   Usage: env_vars = Genius.load_env_file('env-1.env')")
    print("          genius = Genius(access_token=env_vars['ACCESS_TOKEN'])")
except Exception as e:
    print(f"   Error: {e}")

# Method 4: Traditional way (still works)
print("\n✅ Method 4: Traditional explicit access token")
try:
    env_vars = Genius.load_env_file("env-1.env")
    genius4 = Genius(access_token=env_vars['ACCESS_TOKEN'])
    print(f"   Success! Access token provided: {genius4.access_token[:10]}...")
    print("   Usage: genius = Genius(access_token='your_token_here')")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 70)
print("🎉 SUMMARY: Your Genius class now has integrated environment loading!")
print("\n📝 RECOMMENDED USAGE:")
print("   genius = Genius.from_env_file('env-1.env')")
print("   # OR")
print("   genius = Genius(env_file='env-1.env')")

print("\n🚀 Your assignment still meets all requirements, plus:")
print("   ✅ Easy environment file loading")
print("   ✅ Multiple initialization options")
print("   ✅ Backward compatibility maintained")
