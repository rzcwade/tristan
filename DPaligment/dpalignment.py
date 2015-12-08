import numpy as np
import matplotlib as mpl
import sys
#from Bio import SeqIO
#for seq_record in SeqIO.parse("/Users/Tristan/Documents/PythonPrograms/AnalyzingSeq_HW4/sample.fasta", "fasta"):


#Take two amino acidic sequences
A, C, G, T = 0, 1, 2, 3
int_to_char = {0:'A', 1:'C', 2:'G', 3:'T'}
s = np.array([A,C,G,G,T,A,G])
t = np.array([C,C,T,A,A,G])
#Calculate the length of each sequence
n = len(s); m = len(t);


#Create a scoring matrix for looking up the scores and penalty
score_mat = np.array([[2, -1, -1, -1], 
                      [-1, 2, -1, -1],
                      [-1, -1, 2, -1],
                      [-1, -1, -1, 2]])
 
#Initialize dynamic matrix
D = np.zeros((m+1,n+1));

#Initialize variables
D[0,0] = 0;
#Set gap_score
gap_score = -2;
#Fill in the gap_score for the first row and col
for j in range(n+1):
    D[0,j] = gap_score*j
for i in range(m+1):
    D[i,0] = gap_score*i
#print (D)

for i in range(1,m+1):
    for j in range(1,n+1):
        match = D[i-1,j-1] + score_mat[t[i-1], s[j-1]];
        gaps  = D[i,j-1]   + gap_score;
        gapt  = D[i-1,j]   + gap_score;
        D[i,j] = max(match,gaps,gapt);
    
print (D)

#Reverse the matrix to back trace the score in order to find alignment
alig1 = [];
alig2 = [];

while i >= 0 and j>=0:
        if D[i-1,j-1] == D[i,j] - score_mat[t[i-1],s[j-1]]:
            t_ = int_to_char[t[i-1]]
            s_ = int_to_char[s[j-1]]
            alig1.append(t_)
            alig2.append(s_)
            i = i-1;
            j = j-1;
        elif D[i,j-1] == D[i,j] - gap_score:
            s_ = int_to_char[s[j-1]]
            t_ = '_'
            alig1.append(t_)
            alig2.append(s_)
            i = i-1;
        elif D[i-1,j] == D[i,j] - gap_score:
            s_ = '_'
            t_ = int_to_char[t[i-1]]
            alig1.append(t_)
            alig2.append(s_)
            j = j-1;
        else:
            s_ = int_to_char[s[j-1]]
            t_ = int_to_char[t[i-1]]
            alig1.append(t_)
            alig2.append(s_)
            i = i-1;
            j = j-1;

print(alig2[::-1])
print(alig1[::-1])



