def isAnagram(s, t):
        return sorted(s) == sorted(t)



        # dict1 = {k:s.count(k) for k in s}
        # dict2 = {k:t.count(k) for k in t}
        # if dict1 == dict2:
        #     return True
        # return False
        # return Counter(s) == Counter(t)





        # if len(s) != len(t):
        #     return False

        # countS, countT = {}, {}

        # for i in range(len(s)):
        #     countS[s[i]] = 1 + countS.get(s[i], 0)
        #     countT[t[i]] = 1 + countT.get(t[i], 0)

        # for c in countS:
        #     if countS[c] != countT.get(c, 0):
        #         return False
        # return True


        # if countS != countT:
        #     return False
        # return True
