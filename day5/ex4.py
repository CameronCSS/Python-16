def is_prime(n):
    # Primes must be greater than 1
    if n < 2:
        return False
    # 2 is the only even prime
    if n == 2:
        return True
    # Eliminate all other even numbers
    if n % 2 == 0:
        return False
        
    # Check odd divisors from 3 up to sqrt(n)
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def count_primes(number):
    
    # We start with 1 because 2 is a prime. but we are skipping it below
    prime_count = 1
    prime_numbers = [2]
    for num in range(3,number, 2):
        if is_prime(num):
            prime_count += 1
            prime_numbers.append(num)
    print(prime_numbers)
    return prime_count

print(count_primes(100))   
            
