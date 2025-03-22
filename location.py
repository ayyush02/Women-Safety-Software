# location.py

import ipinfo

# Configuration
IPINFO_TOKEN = "cea36824390192"

# Function to get location (without coordinates)
def get_location():
    handler = ipinfo.getHandler(IPINFO_TOKEN)
    details = handler.getDetails()
    return f"{details.city}, {details.region}, {details.country}"

if __name__ == "__main__":
    print(get_location())  # Prints location if run directly
