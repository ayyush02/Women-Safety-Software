from twilio.rest import Client
from location import get_location

# Twilio credentials (Replace with actual credentials)
account_sid = "AC19c46641400ab8a137d0a3a3d3cb8455"
auth_token = "b4898723da50d5936c02a80a3d548b01"
twilio_number = "+18122205858"  # Your Twilio phone number
emergency_number = "+919423846741"  # Number to call

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Get location
location = get_location()
print(location)

def make_emergency_call():
    """Function to make an emergency call with a male voice in Hindi"""
    
    twiml_message = f"""
        <Response>
            <Say voice="man" language="hi-IN">
                यह एक आपातकालीन कॉल है। मैं वैष्णवी पुरी बोल रही हूँ। 
                मेरी सुरक्षा खतरे में है। मैं अभी पर मौजूद हूँ। 
                कृपया तुरंत मदद भेजें। 
            </Say>
            <Pause length="3"/>
            <Say voice="man" language="hi-IN">
                हमने आपकी ईमेल पर एक ऑडियो और वीडियो फ़ाइल भी भेज दी है। 
                कृपया तुरंत कार्रवाई करें।
            </Say>
            <Hangup/>
        </Response>
    """
    
    call = client.calls.create(
        to=emergency_number,
        from_=twilio_number,
        twiml=twiml_message
    )
    
    print(f"🚨 आपातकालीन कॉल शुरू! Call SID: {call.sid}")

# Call the function
make_emergency_call()
