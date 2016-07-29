import re
'''
Exagogi: 		The greek word for export
Description:	Takes a html document or any other kind of document that you have embeded the syntax of {% name %} into
				and embeds another file that you link into the html document to then be exported
'''
class Exagogi:
	'''
	Parameters:	
		html_doc_path : 		the path of the file you want to edit
		output_html_doc_path :	the path that you want to output the file
		append_object_path	:	the path of the text that you wish to append inside the block quotes
		block : 				the syntax of the block quotes inside {% name %}
		endBlock : 				optional param, ending syntax for the end of the block quotes. default is end_$(block)
	'''
	def __init__(self,html_doc_path,output_html_doc_path,append_object_path,block,endBlock=""):
		if(endBlock == ""):
			endBlock = "end_"+block
			
		self.html_doc_path = html_doc_path
		self.output_html_doc_path = output_html_doc_path
		self.append_object_path = append_object_path
		self.selector_expression = re.compile(r'\{% *'+block+' *%\}[\s\S]*\{% *'+endBlock+' *%\}')
		self.clean_expression = re.compile(r'{% *'+block+' *%\}|{% *'+endBlock+' *%\}')
		
	#renders document with specified options
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
	
	#reads the file in the path
	def __getDoc(self,path):
		htmlDoc = ""
		with open(path,'r') as htmlDocFile:
			htmlDoc = htmlDocFile.read()
			htmlDocFile.close()
		return str(htmlDoc)
	
	#gets the values inside the block quotes
	def __getContents(self,htmlDoc):
		contents = self.selector_expression.findall(htmlDoc)
		return contents
	
	#cleans the content (removes block quotes)
	def __cleanContent(self,content):
		content = self.clean_expression.sub('',content)
		return content
	
	#adds new content to original document
	def __addContentBack(self,htmlDoc,content):
		page = self.selector_expression.sub(content,htmlDoc)
		return page
	
	#outputs the file
	def __renderDoc(self,htmlDoc):
		with open(self.output_html_doc_path,'w+') as htmlDocFile:
			htmlDocFile.write(htmlDoc)
			htmlDocFile.close()
		return None