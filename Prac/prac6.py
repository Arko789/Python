#count freq of a word in a sen using dictionary

sen = input("Enter a sen: ")
sen = sen.lower()
words = sen.split()
freq = {}
for word in words:
    
    if word in freq:
        freq[word] = freq[word] + 1
    
    
    else:
        freq[word] = 1

"""
print("\n------------------------------")
print("   Word freq Count")
print("------------------------------")
print(f"{'Word':<15} {'freq':>10}")
print("------------------------------")
"""
for word, count in freq.items():
    #print(f"{word:<15} {count:>10}")
    print(word,":",count)
"""
print("------------------------------")
print(f"Total unique words: {len(freq)}")
print(f"Total words        : {len(words)}")
"""