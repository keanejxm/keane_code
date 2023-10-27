"""

# author: albert
# date: 2021/1/20 10:05
# update: 2021/1/20 10:05
"""
# now = int(time.time() * 1000)
#
# account_data[""] = ""
# account_data["_id"] = self.md5(platformID + str(data["site_id"]))
# account_data["platformAccountID"] = str(data["site_id"])
# account_data["name"] = data["name"]
# account_data["avatar"] = data["indexpic"]["host"] + data["indexpic"]["filename"]
# account_data["url"] = data["content_url"]
# account_data["region"] = ['河北', data["areas"]["name"]]
# account_data["types"] = [7]
# account_data["platformID"] = platformID
# account_data["platformName"] = platformName
# account_data["platformWorksNum"] = int(data["article_click_num"])
# account_data["platformFansNum"] = int(data["article_click_num"])
# account_data["platformFollowsNum"] = int(data["article_click_num"])
# account_data["platformReadsNum"] = int(data["article_click_num"])
# account_data["platformLikesNum"] = int(data["article_click_num"])
# account_data["platformCommentsNum"] = int(data["article_num"])
# account_data["platformForwardsNum"] = int(data["article_num"])
# account_data["weMediaName"] = ""
# account_data["createTime"] = now
# account_data["updateTime"] = now
#
#
# article_data = dict(**)
# article_data["_id"] = self.md5(platformID + article["id"])
# article_data["platformWorksID"] = article["gov_id"]
# article_data["platformID"] = platformID
# article_data["platformName"] = platformName
# article_data["accountID"] = self.md5(platformID + str(article["gov_id"]))
# article_data["accountName"] = article["copyfrom"]
# article_data["url"] = article["share_url"]
# article_data["authors"] = [article["copyfrom"]]
# article_data["title"] = article["title"]
# article_data["titleWordsNum"] = len(article["title"])
# article_data["html"] = detail_content.text
# content = text_remover_html_tag(detail_content_data["frontend"]["contents"])
# article_data["content"] = content
# article_data["contentWordsNum"] = len(content)
# article_data["digest"] = content[:200]
# article_data["images"] = detail_content_data["frontend"]['image']
# article_data["covers"] = cover
# article_data["videos"] = []
# article_data["readNum"] = self.parser_num(article["read_count"])
# article_data["likeNum"] = self.parser_num(article["likes_count"])
# article_data["commentNum"] = self.parser_num(article["comment_count"])
# article_data["forwardNum"] = self.parser_num(article["share_count"])
# article_data["updateParams"] = json.dumps({"article_id": str(article["id"]), "type": str(article["type"])})
# article_data["contentType"] = 1
# if article_data["images"]:
#     article_data["contentType"] = 2
# if article_data["videos"]:
#     article_data["contentType"] = 3
# article_data["pubTime"] = int(article["created_time"]) * 1000
# article_data["createTime"] = now
# article_data["updateTime"] = now






