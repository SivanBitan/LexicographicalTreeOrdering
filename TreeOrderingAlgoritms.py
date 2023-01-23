import math
import operator as op
from math import comb
import TreeBuilder
import pubsub
from pubsub import pub

def T(n, k):
    res = (k/(2*n-k))*comb((2 * n - k), (n - k))
    return res 

def a(i,j):
    x = (j+2)
    y = (2*i-j)
    const = x/y
    x = (2 * i - j)
    y = (i - j-1)
    ncr = comb(x, y)
    return const*ncr


class LexicographicTreeOrdering:

    def __init__(self, subscriber):
        self.tree_node_list = list()
        if subscriber is not None:
            pub.subscribe(subscriber, 'progress')

    def NextTreeZaks(self, tree_node_list):
    # The function for the procedure, where given a feasible sequence it generates the next feasible sequence
    # in our lexicographic order according to S. Zaks
        flag = 0
        n = len(tree_node_list)-1
        for i in range(len(tree_node_list)):
            if flag == 0: 
                if tree_node_list[n-i] < (2*(n-i)-1): # found rightmost z_i such that z_i < 2i-1
                    tree_node_list[n-i] = tree_node_list[n-i]+1 #z_i = z_i +1
                    flag = 1 
                    for j in range((n-i)+1, len(tree_node_list), 1):  #z_j=z_(j-1)+1 for every j>i
                        tree_node_list[j] = tree_node_list[j-1]+1
                        
        return tree_node_list

    def NextTree(self, tree_node_list):  # a_1,a_2,…,a_n ):
        # The function for the procedure, where given a feasible sequence it generates the next feasible sequence
        # in our lexicographic order according to F. Ruskey and T.C Hu
        # This procedure can be easily modified to work on for binary trees instead of sequences.
        
        n = len(tree_node_list) - 1
        k = n
        t = 0

        while tree_node_list[k - 1] != tree_node_list[k]:
            k -= 1
        while (k + t < n and tree_node_list[k + t] == tree_node_list[k + t + 1] + 1):
            t += 1
        tree_node_list[k - 1] = tree_node_list[k - 2] + 1
        tree_node_list[k - 2] += 1
        if(k+t<n): #case where the descending sequence is not at the end of the sequence
            tree_node_list[k] = tree_node_list[k] - t - 1
            if t != 0: #there's a descending sequence
                for j in range((k + 1), (n - t)): #adoption of rightmost pair 
                    tree_node_list[j] = tree_node_list[j + t]
                if (k != (n - 1)): #if after adoption there is a subtree to move to the rightmost child
                    for j in range((n - t), n):
                        tree_node_list[j] = tree_node_list[n] + j - n + t + 1  # a_j←a_n+j-n-t+1;
                    tree_node_list[n] = tree_node_list[n] + t  # a_n←a_n+t;
                else: #no subtree to move
                    tree_node_list[k] = tree_node_list[n]
        else: #case where descending sequence is at the end, therefore only need to reverse its order
            tree_node_list[k] = tree_node_list[k] - 1
            if t != 0:
                i=n
                j=n-t
                while(j<i):
                    temp = tree_node_list[i]
                    tree_node_list[i] = tree_node_list[j]
                    tree_node_list[j] = temp
                    j+=1
                    i-=1
        pub.sendMessage('progress', arg={'progress': tree_node_list})
        return tree_node_list

    def Rank(self, tree_node_list):  # a_1,a_2,…,a_n ):
    #this function calculates the rank of a given tree using F. Ruskey and T.C Hu's method
        rank = 0
        m = 1
        l = 0
        reduced_sequence = list()
        n = len(tree_node_list)

        
        for j in range(1, n-1+1):
            const1 = tree_node_list[j-1]-m-1+1
            for i in range(0,const1):
                rank += T(n - j, m - l + i)
          
            l += 1
            reduced_sequence.append(tree_node_list[j-1])

            while l!=1 and reduced_sequence[l - 2] == reduced_sequence[l-1]: #reduce the sequence
                l -= 1

                reduced_sequence[l-1] -= 1
                reduced_sequence.pop()

                if l-2 == -1:
                    break


            if reduced_sequence[l-1] == l:
                m = l + 1
            else:
                m = reduced_sequence[l-1]
        pub.sendMessage('progress', arg={'progress': tree_node_list})
        return rank

    def Unrank(self, n, rank):
    #this function calculates the tree of given rank using F. Ruskey and T.C Hu's method
        tree_node_list = list()
        reduced_sequence = list()
        m = 1
        l = 0
        for j in range(1,(n - 1+1)):
            i = 0
            tsum = 0
            while True: #calculate the minimal sum of T 
                tsum = tsum + T(n - j, m - l + i)
                i = i + 1

                if rank < tsum:
                    break

            rank = rank - tsum + T(n - j, m - l + i - 1) 
            tree_node_list.append(m + i - 1)  # a_j=m+i-1;
            l = l + 1
            reduced_sequence.append(tree_node_list[j-1])

            while l != 1 and reduced_sequence[l - 2] == reduced_sequence[l - 1]: #reduce the sequence
                l -= 1

                reduced_sequence[l - 1] -= 1
                reduced_sequence.pop()

                if l - 2 == -1:
                    break

            if reduced_sequence[l - 1] == l:
                m = l + 1
            else:
                m = reduced_sequence[l - 1]

        tree_node_list.append(reduced_sequence[l-1])
        return tree_node_list

    def catalan(self, n):
        return (1 / (n + 1)) * math.comb(2 * n, n)

    def a(self, i, j):
        res = (j + 2) / (2 * i - j)
        return res * math.comb(2 * i - j, i - j - 1)

    def init(self, z, n): #calculates init(z) which is the rightmost index where a_(i+1)=i
        for i in range(0, n):
            if (n - i == z[n - i - 1]):
                return n - i

    def z_overbar(self, z, n): # calculates z overbar as in theory
        _z = list()
        j = self.init(z, n)
        for i in range(0, j - 1):
            _z.append(z[i])
        for i in range(j, n):
            _z.append(z[i] - 2)
        return _z

    def rank_zaks_not_complete(self, z, n):
        j = self.init(z, n)
        if (j == n):
            return 1
        else:
            _z = self.z_overbar(z, n)
            res = self.a(n, j) + self.rank_zaks_not_complete(_z, n - 1)
            return res

    def rank_zaks(self, z, n):
    #this function calculates the rank of a given tree using S. Zaks' method
        res = self.catalan(n) - self.rank_zaks_not_complete(z, n)
        pub.sendMessage('progress', arg={'progress': res})
        return res

    def unrank_zaks(self, n, rank):
    #this function calculates the tree of a given rank using S. Zaks' method
        i = 0
        _a = self.catalan(n) - rank
        j = n
        stack = list()
        while (_a > 1):
            for i in range(j - 1, 0, -1):
                if (_a > self.a(j, i) and _a <= self.a(j, i - 1)):
                    break
            _a = _a - self.a(j, i)
            stack.append([j, i]) #append pairs of m,s (as in a_(m,s) ) for future reconstructing of the sequence
            j -= 1
        z = list()
        for i in range(1, j + 1): #init the first j integers in the sequence 
            z.append(i)
        while (stack): #reconstruct the sequence by using the a_(m,s) pairs
            z_tag = list()
            m, s = stack.pop()
            for i in range(1, m + 1):
                z_tag.append(i)
            z_tag[s - 1] = s
            for i in range(m, s, -1):
                z_tag[i - 1] = z[i - 2] + 2
            z = z_tag
        pub.sendMessage('progress', arg={'progress': z})
        return z



def main():
    alg = LexicographicTreeOrdering(subscriber=None)
    # sequence = [1, 2, 3, 4, 6, 6, 5]
    sequence = [3, 5, 5, 6, 6, 2, 1] #3,5,5,4,2,3,3
    print(alg.NextTree(sequence))


if __name__ == "__main__":
    main()
