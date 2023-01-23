import customtkinter
import matplotlib.pyplot as plt

import TreeOrderingAlgoritms
position = 0

class TreeNode:
    def __init__(self, val="1"):
        self.left = None
        self.right = None
        self.val = val
        self.position = 0

    def z_to_x(self, x, z):
        temp_z = z[0]
        temp_z_i = 0
        for i in range(len(x)):
            if i != (temp_z-1):
                x[i] = 0
            else:
                x[i] = 1
                temp_z_i += 1
                if temp_z_i < len(z):
                    temp_z = z[temp_z_i]
        return x

    def create_tree_rec_call(self, root, arr, size):
        if self.position > size:
            return
        if arr[self.position] == 1:
            root.left = TreeNode()
            root.right = TreeNode()
            self.position += 1
            self.create_tree_rec_call(root.left, arr, size)
            self.create_tree_rec_call(root.right, arr, size)

        else:
            root.val = "0"
            root.left = root.right = None
            self.position += 1

    def create_tree(self, arr, size):
        self.root = TreeNode()
        self.position = 0
        self.create_tree_rec_call(self.root, arr, size)
        return self.root


    def printTree(self, root):
        if root == None:
            return
        self.printTree(root.left)
        print(root.val)
        self.printTree(root.right)

    # def SequenceToTree(self, codeLenPairs):
    #     root = None
    #     s = list()
    #     root = TreeNode()
    #     s.append(root)
    #     index = 0
    #     level = 1
    #     curr = None
    #     while (len(s) != 0) :
    #         curr = s[len(s)-1]
    #         if (curr.left != None and curr.right != None):
    #             s.pop()
    #             level-=1

    #         else:
    #             if (codeLenPairs[index][1] == level):
    #                 if (curr.left == None):
    #                     curr.left = TreeNode(codeLenPairs[index][0])
    #                 else:
    #                     curr.right = TreeNode(codeLenPairs[index][0])
    #                     s.pop()
    #                     level-=1
    #                 index+=1

    #             elif codeLenPairs[index][1] > level:
    #                 if (curr.left == None):
    #                     curr.left = TreeNode()
    #                     s.append(curr.left)

    #                 else:
    #                     curr.right = TreeNode()
    #                     s.append(curr.right)
    #                 level+=1
    #     return root

    # def SequenceToTree(self, codeLenPairs):
    #     root = TreeNode()
    #     s = [root]
    #     index = 0
    #     level = 1
    #     curr = None
    #     while (len(s) != 0) :
    #         curr = s[-1]
    #         if (curr.left != None and curr.right != None):
    #             s.pop()
    #             level-=1
    #         else:
    #             if (codeLenPairs[index][1] == level):
    #                 if (curr.left == None):
    #                     curr.left = TreeNode(codeLenPairs[index][0])
    #                 else:
    #                     curr.right = TreeNode(codeLenPairs[index][0])
    #                     s.pop()
    #                     level-=1
    #                 index+=1

    #             elif codeLenPairs[index][1] > level:
    #                 if (curr.left == None):
    #                     curr.left = TreeNode()
    #                     s.append(curr.left)
    #                 else:
    #                     curr.right = TreeNode()
    #                     s.append(curr.right)
    #                 level+=1
    #     return root

    def SequenceToTree(self, codeLenPairs):
        root = TreeNode()
        s = [root]
        index = 0
        level = 1
        curr = None
        while (len(s) != 0) :
            curr = s[-1]
            if (curr.left != None and curr.right != None):
                s.pop()
                level-=1
            else:
                if (index >= len(codeLenPairs)):
                    break
                if (codeLenPairs[index][1] == level):
                    if (curr.left == None):
                        curr.left = TreeNode(codeLenPairs[index][0])
                    else:
                        curr.right = TreeNode(codeLenPairs[index][0])
                        s.pop()
                        level-=1
                    index+=1

                elif codeLenPairs[index][1] > level:
                    if (curr.left == None):
                        curr.left = TreeNode()
                        s.append(curr.left)
                    else:
                        curr.right = TreeNode()
                        s.append(curr.right)
                    level+=1
        return root



    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def treeString(self):
        res = ""
        lines, *_ = self._display_aux()
        for line in lines:
            res = "{}\n{}".format(res, line)
        return res

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = chr(0x25cc)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = chr(0x25cc)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = chr(0x25cc)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = chr(0x25cc)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    def visual_display(self):
        scat_x = list()
        scat_y = list()
        self.visual_display_aux(scat_x, scat_y)
        # plot
        fig, ax = plt.subplots()

        ax.scatter(scat_x, scat_y, s=3, vmin=0, vmax=100)


        plt.show()

    def visual_display_aux(self, scat_x, scat_y):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""

        # No child.
        if self.right is None and self.left is None:
            line = '<%s>' % self.val
            width = 4
            height = 1
            middle = 2
            scat_x.append(3)
            scat_y.append(1)
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left.visual_display_aux(scat_x, scat_y)
            s = '<%s>' % self.val
            u = 4
            scat_x.append(n+u+4)
            scat_y.append(p+1)

            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right.visual_display_aux(scat_x, scat_y)
            s = '<%s>' % self.val
            u = len(s)

            scat_x.append(n + u + 3)
            scat_y.append(p+1)

            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left.visual_display_aux(scat_x, scat_y)
        right, m, q, y = self.right.visual_display_aux(scat_x, scat_y)
        s = '<%s>' % self.val
        u = len(s)



        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        scat_x.append(n + u + 3 +n*(q-p))
        scat_y.append(max(p, q) + 1)
        return lines, n + m + u, max(p, q) + 2, n + u // 2


def main():
   # // cout << "111 Hello World!" << endl;
   # // vector<pair<char, int>> codeLenPairs = { {'a',2}, {'b',2}, {'c',3}, {'d',4}, {'e',4}, {'f',3}, {'g',3} };
   # // auto res = buildHuffman(codeLenPairs);
   #  //int arr[] = { '1', '1', '1', '0', '1', '0', '1','1', '1', '0', '0', '0', '0', '0','0' };
   #  z = [1, 2, 3, 5, 7, 8, 9]
    z=[1,3,4,6]
    x = [0]*len(z)*2
    tree = TreeNode()
    tree.z_to_x(x, z)
    print(x)
    arr = x

    alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(subscriber=None)
    next_tree = alg.NextTreeZaks(arr)
    print(next_tree)
    # arr = [1,0,1,1,0,1,0,0]     # [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    res = tree.create_tree(arr, len(arr)-1)


    res.display()
    res.visual_display()


    # tree = TreeNode()
    # sequence = [1,3,4,4,2]
    # letters = []
    # for i in range(len(sequence)):
    #     letters.append(chr(ord("a") + i))
    # seq_set = zip(letters, sequence)
    # seq_set = list(seq_set)
    # res = tree.SequenceToTree(seq_set)
    # res.display()

    print("end")

if __name__ == "__main__":
    main()
