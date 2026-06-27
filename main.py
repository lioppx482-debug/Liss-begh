import requests
import random
import time
import json
import string  # Yeh zaroori hai
from faker import Faker
from keep_alive import live

fake = Faker()

# Credit card prefixes for different card types
CARD_PREFIXES = {
    'Visa': ['4'],
    'Mastercard': ['5', '2'],
    'American Express': ['34', '37'],
    'Discover': ['6011', '65'],
    'JCB': ['35'],
    'Diners Club': ['30', '36', '38'],
    'UnionPay': ['62'],
    'Maestro': ['50', '56', '57', '58', '67']
}

#====================================================================#
# YEH RAHA final FIX
#====================================================================#
def generate_card_number(card_type):
    """
    Yeh corrected function hai jo sahi Luhn algorithm use karta hai.
    """
    if card_type not in CARD_PREFIXES:
        card_type = random.choice(list(CARD_PREFIXES.keys()))
    
    prefix = random.choice(CARD_PREFIXES[card_type])
    
    # Determine card length
    if card_type == 'American Express':
        length = 15
    elif card_type == 'Diners Club':
        length = 14
    else:
        length = 16
    
    # Generate the main part of the number
    body = prefix + ''.join([str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1)])
    
    # Calculate check digit using the *correct* Luhn algorithm logic
    digits = [int(d) for d in body]
    # Double every second digit from the right
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
            
    # The check digit is what makes the total sum a multiple of 10
    total_sum = sum(digits)
    check_digit = (10 - (total_sum % 10)) % 10
    
    return body + str(check_digit), card_type
#====================================================================#
# FIX KHATAM
#====================================================================#


def luhn_algorithm(card_number):
    """Validate credit card using Luhn algorithm"""
    digits = [int(digit) for digit in card_number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

def generate_card_details():
    """Generate complete credit card details"""
    card_number, card_type = generate_card_number(random.choice(list(CARD_PREFIXES.keys())))
    
    # Generate expiry date (future dates only)
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(25, 32)).zfill(2)
    
    # Generate CVV based on card type
    if card_type == 'American Express':
        cvv = str(random.randint(1000, 9999)).zfill(4)
    else:
        cvv = str(random.randint(100, 999)).zfill(3)
    
    return f"{card_number}|{month}|{year}|{cvv}", card_type

def send_messages():
    # Bot configuration
bot_token = "8839085501:AAEXfJOfhyrpJZJsf_36Ybf8_ecNFdiYv8c"
chat_id = 5054907656
telegram_api = f"https://api.telegram.org/8839085501:AAEXfJOfhyrpJZJsf_36Ybf8_ecNFdiYv8c
    # Configuration
    requests_limit = 1
    pause_duration = 3
    total_cards = 1000
    max_retries = 2

    # Generate and send credit cards
    for i in range(1, total_cards + 1):
        card_details, card_type = generate_card_details()
        card_number = card_details.split('|')[0]
        
        # Ab yeh check hamesha pass hoga
        if not luhn_algorithm(card_number):
            print(f"Invalid card generated at position {i}: {card_details} - SKIPPING")
            continue

        BIN = card_number[:6]
        try:
            response = requests.get(f"https://bins.antipublic.cc/bins/{BIN}", timeout=5)
            if response.status_code == 200 and response.json().get('brand'):
                req = response.json()
                brand = req.get('brand', card_type).upper()
                country = req.get('country', 'US')
                country_name = req.get('country_name', 'United States')
                country_flag = req.get('country_flag', '🇺🇸')
                bank = req.get('bank', 'Unknown Bank')
                level = req.get('level', 'Standard')
                typea = req.get('type', 'Credit')
                print(f"✅ BIN {BIN}: {brand} - {bank}")
            else:
                brand, country, country_name, country_flag, bank, level, typea = card_type, "US", "United States", "🇺🇸", "Unknown Bank", "Standard", "Credit"
                print(f"⚠️  BIN API fail hua, using defaults")
        
        except Exception as e:
            print(f"⚠️  Error fetching BIN data for {BIN}: {e}")
            brand, country, country_name, country_flag, bank, level, typea = card_type, "US", "United States", "🇺🇸", "Unknown Bank", "Standard", "Credit"

        month, year, cvv = card_details.split('|')[1], card_details.split('|')[2], card_details.split('|')[3]
        full_name = fake.name()

        reply_markup = {
            "inline_keyboard": [[
                {"text": "DEVELOPER", "url": "https://t.me/RDXxxCARDER"},
                {"text": "1ST CHANNEL", "url": "https://t.me/+dAOebtrsWngyYWFl"},
                {"text": "2ND CHANNEL", "url": "https://t.me/+7qn0bs6e6m5jOWY1"}
            ]]
        }
        
        message = (
            f"\n"
            f" 𝙀𝙇𝙄𝙏𝙀  𝙎𝘾𝙍𝘼𝙋𝙋𝙀𝙍! \n"
            f"━━━━━━━━━━━━━━\n"
            f"<b>⌖ 𝗖𝗰 ⤳</b> <code>{card_details}</code>\n"
            f"⌖ 𝗦𝘁𝗮𝘁𝘂𝘀 ⤳ 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿! ✅\n"
            f"⌖ 𝗕𝗶𝗻 ⤳ {BIN}\n"
            f"━━━━━━━━━━━━━━\n"
            f"<b>⌮ 𝗜𝗻𝗳𝗼 ⤳ </b>  <code>{brand}-{typea}-{level}</code>\n"
            f"<b>⌮ 𝘽𝘼𝙉𝙆 ⤳ </b>  <code>{bank}</code>\n"
            f"<b>⌮  𝘾𝙊𝙐𝙉𝙏𝙍𝙔 ⤳ </b>  <code>{country_name} [{country_flag}]</code>\n"
            f"━━━━━━━━━━━━━━\n"
            f"<b>⌮ 𝐄𝐗𝐓𝐑𝐀 𝐁𝐈𝐍 ⤳ </b>  <code>{card_number[:6]}xxxx|{month}|{year}|rnd</code>\n"
            f"<b>⌮ 𝗡𝗮𝗺𝗲 ⤳ </b>  <code>{full_name}</code>\n"
            f"━━━━━━━━━━━━━━\n"
        )

        retry_count, message_sent = 0, False
        
        while retry_count < max_retries and not message_sent:
            try:
                # Yeh photo file tere script ke paas 'attached_assets' folder mein honi chahiye
                with open("attached_assets/IMG_20250709_153403_228_1752056794715.jpg", 'rb') as photo:
                    files = {'photo': photo}
                    data = {
                        'chat_id': chat_id, 'caption': message, 'parse_mode': 'HTML',
                        'reply_markup': json.dumps(reply_markup)
                    }
                    response = requests.post(f'{telegram_api}/sendPhoto', files=files, data=data)
                    
                    if response.status_code == 200:
                        print(f"✅ Sent card {i}: {card_type} - {card_details}")
                        message_sent = True
                    elif response.status_code == 429:
                        retry_after = response.json().get('parameters', {}).get('retry_after', 10)
                        print(f"⚠️  Rate limited. Waiting {retry_after} seconds before retry...")
                        time.sleep(retry_after)
                        retry_count += 1
                    else:
                        print(f"❌ Error sending message: {response.text}")
                        retry_count += 1; time.sleep(2)
                        
            except FileNotFoundError:
                print("🔥 ERROR: Photo file nahi mili! 'attached_assets' folder mein photo daal, ya code se photo wala part hata de.")
                return 
            except Exception as e:
                print(f"❌ Error sending message: {e}")
                retry_count += 1; time.sleep(2)
        
        if not message_sent:
            print(f"❌ Failed to send card {i} after {max_retries} attempts")

        if i % requests_limit == 0 and i != total_cards:
            print(f"Request limit reached. Pausing for {pause_duration} seconds.")
            time.sleep(pause_duration)

#live() # Replit ke liye
if __name__ == '__main__':
    send_messages()
