import numpy as np
import matplotlib as mpl
import sys
from Bio import SeqIO

"""another way to extract sequence from fasta
with open(fasta_file) as f:
	   contents = [line.rstrip('\n').rstrip(' ') for line in open(fasta_file)]
"""
#Parse the fssta file and extract mouse and human sequences
for seq_record in SeqIO.parse("sample.fasta", "fasta"):
    if seq_record.id == "mouse":
        mouse = np.array(seq_record)
    else:
        human = np.array(seq_record)

#Take two amino acidic sequences
#create an int array to hold all the index for score_mat
A, R, N, D, C, Q, E, G, H, I, L, K, M, F, P, S, T, W, Y, V, B, Z, X = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22
int_to_char = {0:'A', 1:'R', 2:'N', 3:'D', 4:'C', 5:'Q', 6:'E', 7:'G', 8:'H', 9:'I', 10:'L', 11:'K', 12:'M', 13:'F', 14:'P', 15:'S', 16:'T', 17:'W', 18:'Y', 19:'V', 20:'B', 21:'Z', 22:'x'}
char_to_int = {'A':0, 'R':1, 'N':2, 'D':3, 'C':4, 'Q':5, 'E':6, 'G':7, 'H':8, 'I':9, 'L':10, 'K':11, 'M':12, 'F':13, 'P':14, 'S':15, 'T':16, 'W':17, 'Y':18, 'V':19, 'B':20, 'Z':21, 'x':22}

#initialize two arrays for storing the index
s = []
t = []
for i in range(len(human)):
	s.append(char_to_int[human[i]])
for j in range(len(mouse)):
	t.append(char_to_int[mouse[j]])


#Calculate the length of each sequence
n = len(s);
m = len(t);

#Create a scoring matrix for looking up the scores and penalty
score_mat = np.genfromtxt('blosum62.txt', skip_header=1)[:, 1:]
#print(score_mat)


#Initialize dynamic matrix
D = np.zeros((n+1,m+1));

#Initialize variables
D[0,0] = 0;
#Set gap_score
gap_score = -4;
#Fill in the gap_score for the first row and col
for i in range(n+1):
    D[i,0] = gap_score*i
for j in range(m+1):
    D[0,j] = gap_score*j
#print (D)

for i in range(1,n+1):
    for j in range(1,m+1):
        match = D[i-1,j-1] + score_mat[s[i-1], t[j-1]];
        gaps  = D[i,j-1]   + gap_score;
        gapt  = D[i-1,j]   + gap_score;
        D[i,j] = max(match,gaps,gapt);
    
print (D)

#Reverse the matrix to back trace the score in order to find alignment
alig1 = [];
alig2 = [];

i = n;
j = m;
while i > 0 and j > 0:
        if D[i-1,j-1] == D[i,j] - score_mat[s[i-1],t[j-1]]:
            s_ = int_to_char[s[i-1]]
            t_ = int_to_char[t[j-1]]
            alig1.append(s_)
            alig2.append(t_)
            i -= 1;
            j -= 1;
        elif D[i-1,j] == D[i,j] - gap_score:
            s_ = int_to_char[s[i-1]]
            alig1.append(s_)
            alig2.append('_')
            i -= 1;
        else:
            t_ = int_to_char[t[j-1]]
            alig1.append('_')
            alig2.append(t_)
            j -= 1;

while i > 0:
        s_ = int_to_char[s[i-1]]
        alig1.append(s_)
        alig2.append('_')
        i -= 1;
        
while j > 0:
        t_ = int_to_char[t[j-1]]
        alig1.append('_')   
        alig2.append(t_)
        j -= 1;
        
        
print(alig1[::-1])
print(alig2[::-1])
