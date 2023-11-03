from phonenumbers import is_valid_number, parse


# import re
# def is_valid_zip_code_format(zip_code):
#     # Define a regular expression pattern for a valid zip code format
#     # This is a simplified example; you should adjust it to your specific requirements
#     pattern = r"^\d{5}$" # Example: A valid format is 5 digits (e.g., 12345)

#     # Use the re module to match the zip code against the pattern
#     return re.match(pattern, zip_code) is not None


def is_valid_phone_number(phone_number):
    # Check if the phone number contains only numeric characters
    if not phone_number.isdigit():
        return False

    # Implement custom phone number validation logic here
    # Example: Check if the phone number is valid for a specific country code
    try:
        parsed_number = parse(phone_number, None)
        return is_valid_number(parsed_number)
    except ValueError:
        return False
