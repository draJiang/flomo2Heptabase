# flomo2Heptabase

将 flomo 的笔记导入 Heptabase

## 支持的效果

- [x]  将 flomo 笔记以 md 格式保存到本地
- [x]  笔记：双向链接
- [x]  笔记：标签
- [x]  笔记：图片

小概率出现链接未被正确识别的情况

## 使用方法

1. 通过浏览器访问 flomo，获取 `cookie` 和 `token`
    
    ![https://jiangzilong-image.oss-cn-beijing.aliyuncs.com/uPic/Company/20220729200303.png](https://jiangzilong-image.oss-cn-beijing.aliyuncs.com/uPic/Company/20220729200303.png)
    
2. 将 `cookie` 和 `token`添加到 `.py` 文件中，设置导出的 md 文件保存的本地路径
3. 安装第三方库
    
    ```css
    pip install html2text
    pip install urlextract
    ```
    
4. 运行脚本
5. 在 Hepta 中选择导入 Obsidian 文件
![image](https://jiangzilong-image.oss-cn-beijing.aliyuncs.com/uPic/Company/20220729202244.png)
6. 选择前面导出的 md 文件即可
