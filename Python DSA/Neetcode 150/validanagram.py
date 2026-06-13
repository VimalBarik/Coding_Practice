def isAnagram(s, t):
    return sorted(s) == sorted(t)

s = "anagram"
t = "nagaraa"

print(isAnagram(s, t))