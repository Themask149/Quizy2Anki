from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions  
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import argparse
from pathlib import Path

note_test="Ceci est une note test pour vérifier que l'importation fonctionnne; elle sert aussi à s'assurer que tous les champs sont bien remplis; vous pouvez la supprimer;1;2;3"

def get_cli_arguments() -> argparse.Namespace:
	parser = argparse.ArgumentParser("Quizy2Anki: Convertissez vos fiches Quizy en notes Anki.")
	parser.add_argument(
		"--file", "-f", help="le chemin de votre fichier contenant les URL des fiches que vous voulez convertir", type=Path, required=True
	)
	parser.add_argument(
		"--output",
		"-o",
		help="le fichier qui sera créé avec toutes vos notes dans un format txt à importer directement dans Anki",
		type=Path,
		required=True,
	)
	parser.add_argument(
		"--driver",
		"-d",
		help="le dossier où se trouve votre driver Chrome",
		type=Path,
		required=True,
	)
	return parser.parse_args()

driver = None

def connection(url):
	driver.get(url)
	wait = WebDriverWait(driver, 10)
	wait.until(EC.presence_of_element_located((By.XPATH, "//html/body")))


def extractFiche():
	el=driver.find_element(By.CLASS_NAME,"themeRow2")
	theme=el.find_element(By.CLASS_NAME,"size24").text.split("(")[0]
	fiche = driver.find_elements(By.CSS_SELECTOR,"[id*=Page_card]:not([id$=buttons])")
	final=[]
	for f in fiche:
		card={}
		titre=f.find_element(By.CLASS_NAME,"cardTitle").get_attribute("innerHTML").split("(")[0]
		table=f.find_element(By.TAG_NAME,"table")
		rows=table.find_elements(By.TAG_NAME,"tr")
		for row in rows:
			try:
				name=row.find_element(By.CLASS_NAME,"nameTd").get_attribute("innerHTML")
				value=row.find_element(By.CLASS_NAME,"valueTd").get_attribute("innerHTML")
				value=value.replace(";",",")
				card[name]=value
			except:
				pass
		try:
			img = f.find_element(By.CLASS_NAME,"myImg")
			img_link = img.get_attribute("src")
			card["Image"]=img_link
		except Exception as e:
			pass
		final.append(card)
	return final,theme

def selectionIndices(keyslist):
	inputUser=input()
	inputUser=inputUser.split(";")
	for i in range(len(inputUser)):
		inputUser[i]=inputUser[i].split("+")
	try:
		inputUser=trueIndices(keyslist,inputUser)
	except Exception as e:
		print(e)
		print("Voici les différents indices: ",keyslist)
		print("Refaites votre choix")
		return selectionIndices(keyslist)

	print("Voici les indices que vous avez choisi: ",inputUser)
	print("Confirmez-vous votre choix? (y/n)")
	confirm=input()
	if confirm=="y" and len(inputUser)<5:
		return inputUser
	else:
		if len(inputUser)>=5:
			print("Vous avez choisi trop d'indices")
		print("Voici les différents indices: ",keyslist)
		print("Refaites votre choix")
		return selectionIndices(keyslist)
	
def trueIndices(keyslist,indices):
	ind=[]
	for liste in indices:
		subind=[]
		for string in liste:
			bool=False
			for key in keyslist:
				if key.lower().startswith(string.lower()) and not bool:
					subind.append(key)
					bool=True
			if not bool:
				raise("L'indice "+string+" n'existe pas")
		ind.append(subind)
	return ind



def conversion(final,theme):
	string=''
	if not final or not theme:
		print("Oh oh! je n'ai pas réussi à extraire les fiches")
		return
	keysList=list(final[0].keys())
	print("Voici les différents indices: ",keysList)
	print("Pour le thème suivant: ",theme)
	print("Quels indices voulez-vous convertir?")
	print("Mettez l'indice majeur en premier puis séparer les indices par des point-virgules, si vous voulez combiner 2 indices, séparez-les par des +")
	indices=selectionIndices(keysList)
	for card in final:
		for i in range(len(indices)):
			if i==1:
				string+=theme+ " ;"
			for indice in indices[i]:
				if indice=="Image":
					if indice in card:
						string+="<img src="+card[indice]+">"
				else:
					if indice in card:
						string+=card[indice]+" "
			string+=";"
		string=string[:-1]
		string+="\n"
	return string

def extractUrl(file):
	with open(file,"r") as f:
		text=f.read()
	link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
	links = re.findall(link_regex, text)
	return [x[0] for x in links]

def fichisator(path_fiches,output_file):
	urlList=extractUrl(path_fiches)
	with open(output_file,"w") as file:
		file.write(note_test)
	for url in urlList:
		connection(url)
		final,theme=extractFiche()
		string=conversion(final,theme)
		with open(output_file,"a") as file:
			file.write(string)

if __name__ == "__main__":
	args = get_cli_arguments()
	Driver_Path = args.driver
	options = ChromeOptions()
	options.add_argument("--headless")

	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
	fichisator(args.file,args.output)
	
	



	



	

