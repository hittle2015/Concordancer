# Concordancer
1. This script has been only tested on Ubuntu 16.10. At the terminal, 
    you can fire up the programme with the similar command as "python concordancer.py  5 > result.txt" (5 is the window size).
2. The script is able to process a single TSV file or TSV files in a directory.
3. Users need to specify the file path at line 231 and change the content below:
   "/home/yuyuan/WorkSpace/lancasterTask/data/" to path="where_your_corpus" to whatever suits.
4. To query for specific structure use the following format of query
   "expression(1) expression(2) ...expression(n)".
   Note that all sub expressions should be strictly space seperated and they  are input in the form:
   "query_type=query_expression"
   where query_type are preceeding categories from the tsv file, namely "pos", "token", "stanford-pos" and "sem" and
   query_expression can be either literal or regexes.These four types of query can be freely combined to query for any length of
   structure.
   Thus to query a "adj + and +adj" structure, you should use "pos=J\w+ token=and pos=J\w+". Specify this query at line 234.
5. In order to have a certain length of surrounding context (before or after your query), you need to specify the window size 
   while running the script. Thus the above-mentioned command gives you a left-5 and right-5 context.
6. For each sub expression, You can specify And conditions and OR conditions through regular expressions, but you cannot specify 
   AND or OR conditions of different categories. For instance, you cannot specify constraints of Part-of-Speech constraints and
   semantic categories at the same time. (This is the limitation of the current design).
7. Example query and the output may be found at the example_query folder.
   

