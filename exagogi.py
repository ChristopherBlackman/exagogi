import re

class Exagogi:
	def __init__(self,html_doc_path,output_html_doc_path,append_object_path,block,endBlock=""):
		if(endBlock == ""):
			endBlock = "end_"+block
			
		self.html_doc_path = html_doc_path
		self.output_html_doc_path = output_html_doc_path
		self.append_object_path = append_object_path
		self.selector_expression = re.compile(r'\{% *'+block+' *%\}[\s\S]*\{% *'+endBlock+' *%\}')
		self.clean_expression = re.compile(r'{% *'+block+' *%\}|{% *'+endBlock+' *%\}')
		
	def render(self):
	
		append_object = self.__getDoc(self.append_object_path)
		htmlDoc = self.__getDoc(self.html_doc_path)
		contents = self.__getContents(htmlDoc)
		if(len(contents) < 1):
			return
		content = contents[0]
		content = self.__cleanContent(content)
		content += append_object
		newHtmlDoc = self.__addContentBack(htmlDoc,content)
		self.__renderDoc(newHtmlDoc)
		
	def __getDoc(self,path):
		htmlDoc = ""
		with open(path,'r') as htmlDocFile:
			htmlDoc = htmlDocFile.read()
			htmlDocFile.close()
		return str(htmlDoc)
	def __getContents(self,htmlDoc):
		contents = self.selector_expression.findall(htmlDoc)
		return contents
	def __cleanContent(self,content):
		content = self.clean_expression.sub('',content)
		return content
	def __addContentBack(self,htmlDoc,content):
		page = self.selector_expression.sub(content,htmlDoc)
		return page
	def __renderDoc(self,htmlDoc):
		with open(self.output_html_doc_path,'w+') as htmlDocFile:
			htmlDocFile.write(htmlDoc)
			htmlDocFile.close()
		return None