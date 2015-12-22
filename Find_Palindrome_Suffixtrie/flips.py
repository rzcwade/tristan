"""
Goal: find longest palindrome from an input string. Ex., 'aabbaa' or 'aabcbaa'

Approach: Implement a Generalized SuffixTrie and fit the string s and the reverse sr into it. 
Assume s is the original string, and r is s reversed. Let's also assume we've completely built a suffix tree ST using s. Next step is to check all the suffixes of r against ST. With each new suffix of r, we'll maintain a count of the first k charactes we've matched successfully against a preexisting suffix in the tree (ie, one of s's suffixes).

Example: say we're matching the suffix "RAT" from r, and s contained some suffixes beginning with "RA", but none that matched "RAT". k would equal 2 when we finally had to abandon hope for the final characters "T". We matched the first two characters of r's suffix with the first two characters of s's suffix. We'll call this node that we reached n.

Now, how do we know when we've found a palindrome? By checking all leaf nodes under n.

In a traditional suffix tree, the starting index of each suffix is stored at the leaf node of that suffix branch. In our above example, s may have contained a bunch of suffixes starting with "RA", each of which begins at one of the indexes present in the leaf node descendants of n.

Let's use these indices.

What does it mean if we match k characters of one of R's substrings against k characters in ST? Well, it simply means we found some string reversed. But what does it mean if the location where the substring begins in R is equal to the matched substring in S plus k? Yes, it means s[i] through s[i+k] reads the same as s[i+k] through s[i]! And so, be definition we've located a palindrome of size k.

Now, all you have to do is keep a tab on the longest palindrome found so far, and return it at the end of your function.
"""
