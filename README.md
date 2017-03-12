# Concordancer
1. This script has been only tested on Ubuntu 16.10. At the terminal, 
    you can fire up the programme with the similar command as "python Concordancer.py  5 > result.txt" (5 is the window size).
2. The script is able to process a single TSV file or TSV files in a directory.
3. Users need to specify the file path at line 231 and change the content below:
   "/home/yuyuan/WorkSpace/lancasterTask/data/" to path="where_your_corpus" to whatever suits.
4. To query for specific structure use the following format of query
   expression(1)[space]expression(2)[space]...expression(n)
   Note that where expression(n) is in the form "pos=expression" where expression can be either literal or regexes.
   Thus to query a "adj + and +adj" structure, you should use "pos=J\w+ token=and pos=J\w+". Specify this query at line 234.
5. In order to have a certain length of surrounding context (before or after your query), you need to specify the window size 
   while unning the script. Thus the above-mentioned command gives you a left-5 and right-5 context.
6. For each sub expression, You can specify And conditions and OR conditions through regular expressions, but you cannot specify 
   AND or OR conditions of different categories. For instance, you cannot specify constraints of Part-of-Speech constraints and
   semantic categories at the same time. (This is the limitation of the current design).
   

