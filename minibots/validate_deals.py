def validate_deal(deal):
    if not (0 <= deal['discount'] <= 100):
        return False
    if not deal['sku'].isdigit():
        return False
    return True

if __name__ == "__main__":
    test_deal = {'sku': '12345', 'discount': 50}
    print(validate_deal(test_deal))
