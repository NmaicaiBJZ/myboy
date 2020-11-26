from lxml import etree


text = """<div><ul>
        <li class="item-1"><a href="link1.html"></a></li>
        <li class="item-12"><a href="link2.html">second item</a></li>
        <li class="item-1"><a href="link3.html">third item</a></li>
        <li class="item-1"><a href="link4.html">fourth item</a></li>
        <li class="item-10"><a href="link5.html">last item</a></li>
        </ul></div>"""

html = etree.HTML(text)
print(html)

re1 = html.xpath("//li[@class='item-1']/a/@href")
print(re1)

re2 = html.xpath("//li[@class='item-1']/a/text()")
print(re2)

# for her in re1:
#     item = {}
#     item["href"] = her
#     item["item"] = re2[re1.index(her)]
#     print(item)

print("+"* 100)

re3 = html.xpath("//li[@class='item-1']")
for i in re3:
    item = {}
    item["item"] = i.xpath("./a/text()")[0] if len(i.xpath("./a/text()"))>0 else None
    item["href"] = i.xpath("./a/@href")[0] if len(i.xpath("./a/@href"))>0 else None
    print(item)

