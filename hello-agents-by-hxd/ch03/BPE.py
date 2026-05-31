import re,collections

#统计词表中相邻词元出现的频率
"""
vocab = {
    "l o w": 5,
    "l o w e r": 2,
    "n e w e s t": 6
}
"""
def get_stats(vocab):
    """统计词元对频率"""
    pairs=collections.defaultdict(int) #defaultdict表示如果key不存在，默认值是0
    for word,freq in vocab.items():
        symbols=word.split() #按空格拆开 ["l","o","w"]
        for i in range(len(symbols)-1):
            pairs[symbols[i],symbols[i+1]] +=freq
            #pair[("l","w")]+=5
        return pairs

#把词表v_in中指定的相邻词元对pair合并成一个新词元
#pair=("l","o")
#v_in={"l o w":5,"l o w e r":2}
def merge_vocab(pair,v_in):
    """合并词元对"""
    v_out={}
    bigram=re.escape(' '.join(pair)) #re.escape表示把里面的特殊符号都转义成普通字符
    p=re.compile(r'(?<!\S)'+bigram+r'(?!\S)') #构造正则表达式
    for word in v_in:
        #比如word="l o w"
        w_out=p.sub(''.join(pair),word) #把pair和在一起，把匹配到的"l o"替换成"lo"输出w_out="lo w"
        v_out[w_out]=v_in[word] #v_out["lo w"=5
    return v_out

#准备语料库，每个词末尾加上</w>表示结束，并切分好字符
vocab=vocab = {'h u g </w>': 1, 'p u g </w>': 1, 'p u n </w>': 1, 'b u n </w>': 1}
num_merges=4 #设置合并次数

for i in range(num_merges):
    pairs=get_stats(vocab)
    """
    {
    ('h', 'u'): 1,
    ('u', 'g'): 2,
    ('g', '</w>'): 2,
    ('p', 'u'): 2,
    ('u', 'n'): 2,
    ('n', '</w>'): 2,
    ('b', 'u'): 1
    }"""
    if not pairs:
        break
    best=max(pairs,key=pairs.get) #找到出现最多的词元对,比如('u','g')
    vocab=merge_vocab(best,vocab) #合并成ug
    """
    h u g </w>
    p u g </w> 
    变成
    h ug </w>
    p ug </w>
    """
    print(f"第{i+1}次合并: {best} -> {''.join(best)}")
    print(f"新词表（部分）: {list(vocab.keys())}")
    print("-"*20)

