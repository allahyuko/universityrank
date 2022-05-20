import streamlit as st
import networkx as nx
import skimage.io as io

st.title("基于page rank的专业排名——北美cs！！！！")
st.subheader('1. 研究型大学的目标')


st.markdown('大学的办学目标是培养人才，而研究型大学的办学目标则是培养研究型人才。因此一个研究型大学的博士项目最能体现该大学的综合办学能力。当前，研究大学的教职工的主要任务有两个，第一是发表科研论文，第二是培养学生，事实上这两个目标在某种角度是有所重叠的：即主要科研工作是由教职工指导博士生完成的。那么，博士生本身的学术水平就能很好的体现研究型大学的整体办学效果。')


st.subheader('2. 我们得到一个关于大学实力的基本假设：')


st.markdown('大如果A校毕业的博士生，可以在B校找到教职，那么我们可以认为A校的学术水平不小于B。比如，清华经管的博士生可以去山东大学经管学院当助理教授或讲师，那么我们认为清华经管的学术水平不小于山东大学。这不是一个绝对严格的关系，如果清华有3个人去了山大，而山大有1个人去了清华，那么也可以认为清华的学术水平大于山大。')
st.markdown(' 通过检索各个学校，各个学院的主页，获取教职工的简历（主要是博士学位取得学校），可以构建一个“博士——教职”网络，下图给出一个示例：从山东大学到清华大学的箭头和箭头上的5表示，山东大学有5个教职工的博士学位是清华大学授予的。')


figure1 = io.imread('figure1.png')

st.image(figure1, caption='博士学位-教职网络示意图', use_column_width=True)

st.subheader('3. Page Rank——一种利用网络结构的排序方法')

st.markdown('PageRank，网页排名，又称网页级别、Google左侧排名或佩奇排名，是一种由根据网页之间相互的超链接计算的技术，而作为网页排名的要素之一，以Google公司创办人拉里·佩奇（Larry Page）之姓来命名。Google用它来体现网页的相关性和重要性，在搜索引擎优化操作中是经常被用来评估网页优化的成效因素之一。Google的创始人拉里·佩奇和谢尔盖·布林于1998年在斯坦福大学发明了这项技术。')
st.markdown('一个页面的“得票数”由所有链向它的页面的重要性来决定，到一个页面的超链接相当于对该页投一票。一个页面的PageRank是由所有链向它的页面（“链入页面”）的重要性经过递归算法得到的。一个有较多链入的页面会有较高的等级，相反如果一个页面没有任何链入页面，那么它没有等级。')
st.markdown('假设一个由只有4个页面组成的集合：A，B，C和D。如果所有页面都链向A，那么A的PR（PageRank）值将是B，C及D的和。 ')
figure2 = io.imread('figure2.png')
st.image(figure2, caption='', use_column_width=True)
st.markdown('继续假设B也有链接到C，并且D也有链接到包括A的3个页面。一个页面不能投票2次。所以B给每个页面半票。以同样的逻辑，D投出的票只有三分之一算到了A的PageRank上。 ')
figure3 = io.imread('figure3.png')
st.image(figure2, caption='', use_column_width=True)
st.markdown('换句话说，根据链出总数平分一个页面的PR值。')
figure4 = io.imread('figure4.png')
st.image(figure4, caption='', use_column_width=True)
st.markdown('通过迭代算法，可以让PR值收敛。')


st.subheader('4. 利用博士学位-教职网络进行大学排名实例')
figure5 = io.imread('figure5.png')
st.image(figure5, caption='例1. 清华有一名助理教授为深圳大学phd', use_column_width=True)
figure6 = io.imread('figure6.png')
st.image(figure6, caption='例2. 去除清华有一名助理教授为深圳大学phd', use_column_width=True)


st.subheader('5. 北美top 55 大学CS排名（2014年数据）')
st.markdown('')




from pyvis.network import Network
import pandas as pd
import streamlit.components.v1 as components



got_data = pd.read_csv("csfaculty.csv")
targets= got_data['University']
sources= got_data['Doctorate']
weights = got_data['Weight']


nx_graph=nx.empty_graph()



edge_data = zip(sources, targets, weights)

for e in edge_data:
    src = e[0]
    dst = e[1]
    w = e[2]
     
    #往空集合中添加节点和边
    nx_graph.add_node(src,  title=src)
    nx_graph.add_node(dst,title=dst)
    nx_graph.add_edge(src, dst, weight=w)



got_net = Network(notebook=True, height="1000px", width="1000px", bgcolor="#222222", font_color="white")

# 这是pyvis中的文档，但是却没有这个barnes_hut方法的任何说明
# 这里我理解成一个用来存放边数据的特殊空集合
got_net.from_nx(nx_graph)

#对空集合中的数据进行处理，去重
neighbor_map = got_net.get_adj_list()

#让每个节点显示周围的相邻的人物关系 
for node in got_net.nodes:
    node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
    
    node["value"] = len(neighbor_map[node["id"]])

pgRank = nx.algorithms.pagerank(nx_graph)
betweenness = nx.algorithms.betweenness_centrality(nx_graph)
closeness = nx.algorithms.closeness_centrality(nx_graph)

rankings = pd.concat([pd.DataFrame([pgRank]).T,pd.DataFrame([betweenness]).T, pd.DataFrame([closeness]).T],axis = 1)
rankings.columns = ['pgRank','betweenness','closeness']
rankings.sort_values('pgRank', ascending = False).head(20).round(4)
st.write(rankings)

try:
    path = '/tmp'
    got_net.save_graph(f'{path}/pyvis_graph.html')
    HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
except:
    path = '/html_files'
    got_net.save_graph(f'{path}/pyvis_graph.html')
    HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

components.html(HtmlFile.read(), height=435)


