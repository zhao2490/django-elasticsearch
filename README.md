# django-elasticsearch
A Django + elasticsearch demo  
# 实现功能  
对elasticsearch中的数据进行全文检索  
检索到的数据在页面中高亮显示  
# 使用步骤
请在elasticsearch安装目录下的plugins文件夹下放IK分词器  
utils目录下create_elastic_index.py文件创建elasticsearch的mappings    
utils目录下spider.py文件获取基本数据  
# 数据库字符编码问题
如果使用示例爬虫spider.py获取数据  
需要将数据库Blog表的title和content字段编码改为utf8mb4
