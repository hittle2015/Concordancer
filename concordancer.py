
# coding: utf-8

# In[1]:

import csv
import os
import sys
import re
import itertools
import operator
import ntpath
import codecs
#import string
from collections import defaultdict


# In[13]:

def FileReader (file):
    columns = defaultdict(list)
    corpusTsv={}
    with codecs.open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in enumerate(reader):
            corpusTsv[row[0]]=row[1]
    return corpusTsv



# In[57]:

def query_Handler(query):
    '''
    This function handles queries for multiwords, such as adv + adj + noun structures \\
    for longer than one query, if the query consists of two  expressions (literal or regex)\\
    the handler finds the indexes of both and  return the contex to the left of the first and \\
    to the righ tof the second.\\
    data type : string
    result: a list of two components, the first element is the query type, e.g. token or pos,\\
            the second element is the query expression, normal or regular expressions.
    example:
           query_Hanlder("token=\\bwas\\b")
           querytype = "token"
           query     = "was"
    This functions handles query of different lengths as well.
    '''
    #query = input("""Type in the regular expressions for literal POS tags or Words to Search\n
                    #for multiple words query, use the [pos="v.*"] + [token="cat"] + [pos="V.*"] format:""")
    queries = query.split(' ')# multiple queries should be space separated.
    query_length=len(queries)
    parsed_query=[]
    if query_length==1:
        lregex, rregex = queries[0].split('=')
        #lregex = lregex[1:]
        #rregex = rregex[2:-2]
        parsed_query.append([lregex, rregex])
        return parsed_query
    elif query_length==2:
        left_query = queries[0]
        right_query = queries[query_length-1]
        lregex, rregex = left_query.split('=')
        rlregex, rrregex = right_query.split('=')
      
        parsed_query.append([lregex, rregex])
        parsed_query.append([rlregex, rrregex])
    elif query_length >=3:
        left_query = queries[0]
        right_query = queries[query_length-1]
        lregex, rregex = left_query.split('=')
        rlregex, rrregex = right_query.split('=')
        parsed_query.append([lregex, rregex])
        for l in range(query_length-2):
            middle_query = queries[l+1]
            mlregex, mregex = middle_query.split('=')
            parsed_query.append([mlregex, mregex])
            l +=1
        parsed_query.append([rlregex, rrregex])
        
    else:
        pass
    return parsed_query


# In[16]:

def findKey(mYdict, queryType, regex):
    '''
    In our case there are only two types of queryTypes, i.e. pos or token. thus the input should be either 'pos' or 'token'
    '''    
    pattern=re.compile(regex)
    print("printing out the query regular expression...")
    print(pattern)
    if queryType =='pos':
        trgs=[]
        for value in mYdict.values():
            trg = value['pos']
            trgs.append(trg)
        postags =' '.join(map(str, trgs))
        #print(postags)
        matches = set(re.findall(pattern, postags))
        print("printing out the matched ones...")
        print(matches)
        return list(key for key, value in mYdict.items() for val in matches if value[queryType] == val  )
    elif queryType =='token':
        trgs=[]
        for value in mYdict.values():
            trg =value['token']
            trgs.append(trg)
        tokens =' '.join(map(str, trgs))
        matches = set(re.findall(pattern, tokens))
        return list(key for key, value in mYdict.items() for val in matches if value[queryType] == val  )
    elif queryType =='sem':
        keys=[]
        for key, value in mYdict.items():
            if re.search(pattern,value['sem']):
                keys.append(key)
        return keys
    elif queryType =='stanford-pos':
        trgs=[]
        for value in mYdict.values():
            trg =value['stanford-pos']
            trgs.append(trg)
        tokens =' '.join(map(str, trgs))
        matches = set(re.findall(pattern, tokens))
        return list(key for key, value in mYdict.items() for val in matches if value[queryType] == val  )
    else:
        print("Wrong query type or query expressions! ")
        pass
    


# In[95]:
def ConcordanceIndexFinder(myDic, query):
    parsed_queries=query_Handler(query)
    KeyIndexes=[]
    for query_tuple in parsed_queries:
        querytype=str(query_tuple[0])
        regex=str(query_tuple[1])
        print(querytype)
        print(regex)
        KeyIndexes.append(findKey(myDic, querytype, regex))
        #print(merged.sort())
        #return merged
    l=len(KeyIndexes)
    KeyIndexes=[list(range(s,s+l)) for s in KeyIndexes[0] if all(i in l for i,l in zip(range(s+1,s+l),KeyIndexes[1:]))]
    return KeyIndexes


# In[140]:

#import sys
#from termcolor import colored, cprint
def ConcordanceBuilder(myDictionary, left_offset, right_offset, window):
    '''
    This functions retrieves the running tokens surrounding the query on both sides.\\
    left_offset takes the minimus index returned from the group_consecutives, and\\
    right_offset takes the maximum index returned from the group_conseuctives.\\
    corresponding tokens to inbetween consecutive indexs are also returned to form the query itself.\\
    Thus this function builds on three components: a component retrieving the left context, a component \\
    retrieving the right compnent and the a component to build the inbetween query(from one to n words length)\\
    and finally print out the result.
    
    '''
    w1 = int(left_offset) - int(window)
    w2 = int(right_offset) + int(window)
    if w1 < 0:
        left_context = range(left_offset)
        right_context = range(right_offset+1, w2+1)
        leftconcordance=[]
        rightconcordance=[]
        keywords=[]
        for lft_indx in left_context:
            token = myDictionary[lft_indx]['token']
            leftconcordance.append(token)
        for rgt_indx in right_context:
            token = myDictionary[rgt_indx]['token']
            rightconcordance.append(token)
        for key in range(left_offset, right_offset+1):
            token =myDictionary[key]['token']
            
            keywords.append(token)
        else:
            pass
        left_text = ' '.join(map(str, leftconcordance))
        right_text = ' '.join(map(str, rightconcordance))
        keyword_text = ' '.join(map(str, keywords))
        concordance = ('{0:>70} {1:^10} {2:<70}'.format(left_text + ' ||| ', keyword_text,  ' ||| ' + right_text))
        #print(concordance)
        return concordance
        
    
    elif w1 >0:
        left_context = range(w1, left_offset)
        right_context =range(right_offset+1, w2+1)
        leftconcordance=[]
        rightconcordance=[]
        keywords=[]
        for lft_indx in left_context:
            token = myDictionary[lft_indx]['token']
            leftconcordance.append(token)
        for rgt_indx in right_context:
            token = myDictionary[rgt_indx]['token']
            rightconcordance.append(token)
        for key in range(left_offset, right_offset+1):
            token =myDictionary[key]['token']
            
            keywords.append(token)
        left_text = ' '.join(map(str, leftconcordance))
        right_text = ' '.join(map(str, rightconcordance))
        keyword_text = ' '.join(map(str, keywords))
        #text = colored(keyword_text, 'red', attrs=['reverse', 'blink'])
        #print()
        #print('-'*20)
        concordance = ('{0:>70} {1:^10} {2:<70}'.format(left_text + ' ||| ', keyword_text,  ' ||| ' + right_text))
        #print(concordance)
        #cprint(text, 'green', 'on_red')
        return concordance
    else:
        pass





# In[209]:

def main():
    #### 
    ###Change the line below to where your corpus file(s) is/are located.
    path = "/home/yuyuan/WorkSpace/lancasterTask/data/"
    ### Change here the query expressions in either normal literal froms or regular expressions, \\
    ### for multiple words searching, each expression should be space seperated.
    query = "token=[Aa]s pos=J\w+ token=[Aa]s"
    ### You can supply a window size of surrounding context at the command line or hardcod it here at your own will.
    window = sys.argv[1]
    query_len = len((query).split(' '))
    if os.path.isdir(path):    
        print("\n Reading files in {0}".format(path))
        for subdir, dirs, files in os.walk(path):
            for file in files:
                print("\n Reading  the file : {0}".format(file)) 
                corpusTsv = FileReader(os.path.join(path,file))
                query_index = ConcordanceIndexFinder(corpusTsv, query)
                #merged = list(itertools.chain.from_iterable(query_index)) ## combine all sublist together to get all indexes of key word(s)
                #merged.sort()
                hits=0
                cnt, kwic ="Hits", "Key Words in Context"
                title = ("{0:<5}{1!s:>90}".format(cnt, kwic))
                print (title)
                print("*"*160)
                #for lst in group_consecutives(merged, step=1):
                for lst in query_index:
                        try:
                            if len(lst)==1 and len(lst) == query_len:
                                left_offset = lst[0]
                                right_offset = lst[0]
                                #if len(query_index) == query_len and left_offset in query_index[0]:
                                hits +=1
                                concs = ConcordanceBuilder(corpusTsv, left_offset, right_offset, int(window))
                                concs = ('{0!s:<4} {1!s:<2}'.format(hits, concs))
                                print (concs)
                            elif len(lst) >=2 and len(lst) == query_len:
                                left_offset = min(lst)
                                right_offset = max(lst)
                                #if len(query_index) == query_len and left_offset in query_index[0]:
                                hits +=1
                                concs = ConcordanceBuilder(corpusTsv, left_offset, right_offset, int(window))
                                concs = ('{0!s:<4} {1!s:<2}'.format(hits, concs))
                                print (concs)
                                    
                            else:
                                #print("Your Query Returned 0 hits! Make Sure Your Input the Right Query Expressions (Literal or RegexesS)")
                                pass
                        except KeyError:
                            pass
                print("*"*160)
                print ("Your Query Returned {0}  hits!".format(hits) )
    elif os.path.isfile(path):    
        print("\n Reading  the file : {0}".format(path)) 
        corpusTsv=FileReader(path)
        query_index = ConcordanceIndexFinder(corpusTsv, query)
        merged = list(itertools.chain.from_iterable(query_index)) ## combine all sublist together to get all indexes of key word(s)
        merged.sort()
        hits=0
        cnt, kwic ="Hits", "Key Words in Context"
        title = ("{0!s:<5}{1!s:>90}".format(cnt, kwic))
        print (title)
        print("*"*160)
        for lst in group_consecutives(merged, step=1):
            try:
                if query_len==1 and len(lst)==query_len:
                    left_offset = min(lst)
                    right_offset = min(lst)
                    if len(query_index) == query_len and left_offset in query_index[0]:
                        hits +=1
                        concs = ConcordanceBuilder(corpusTsv, left_offset, right_offset, int(window))
                        concs = ('{0!s:<4} {1!s:<2}'.format(hits, concs))
                        print (concs)
                elif query_len >=2  and len(lst)==query_len:
                    left_offset = min(lst)
                    right_offset = max(lst)
                    if len(query_index) == query_len and left_offset in query_index[0]:
                        hits +=1
                        concs = ConcordanceBuilder(corpusTsv, left_offset, right_offset, int(window))
                        concs = ('{0!s:<4} {1!s:<2}'.format(hits, concs))
                        
                        
                        
                        
                        print (concs)
                        
                else:
                    #print("Your Query Returned 0 hits! Make Sure Your Input the Right Query Expressions (Literal or RegexesS)")
                    pass
            except KeyError:
                    pass
        print("*"*160)
        print ("Your Query Returned {0}  hits!".format(hits) )


# In[184]:

if __name__ == '__main__' :
    # if len(sys.argv) != 4:
    #     print ('usage:python concordancer.py  query <coprus_file/directory> <window> ')
    #     sys.exit(1)
    # else:
    #     main()
    main()


# In[ ]:



