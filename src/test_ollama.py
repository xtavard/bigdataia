import ollama

response = ollama.chat(
	model = "qwen2.5:7b",
	messages=[
		{
			"role":"user",
			"content":"""
				tu travailles pour l'entreprise Urban & Co, 
				une chaîne française spécialisée dans l'équipement de la maison. 

				Génère exactement 3 catégorie de produits

				Pour chaque catégorie, donne :
				- categorie_id
				- nom
				- description
	
				Réponds uniquement en json valide
				"""
		}
	],
	format="json"
)

print(response["message"]["content"])