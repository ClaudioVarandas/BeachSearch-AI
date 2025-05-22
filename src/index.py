from langchain_core.documents import Document
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure OpenAI API key is set
if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "":
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Helper function to convert Sim/Não to boolean
def to_boolean(value):
    return str(value).strip().lower() == "sim"

# Helper function to parse coordinates
def parse_coordinates(coord_str):
    try:
        lat, lon = map(float, str(coord_str).split(","))
        return lat, lon
    except (ValueError, AttributeError):
        return None, None  # Handle invalid coordinates gracefully

# Read CSV file using pandas
# Load the CSV file from the data directory
df = pd.read_csv('./data/praias_merged_final.csv')

# Create LangChain Documents
documents = []
for _, row in df.iterrows():
    # Convert fields to metadata
    metadata = {
        "id": int(row["id"]),
        "URL": str(row["URL"]),
        "Nome": str(row["Nome"]),
        "Informação": str(row["Informação"]),
        "Classificação_da_água": str(row["Classificação_da_água"]),
        "Coordenadas": {
            "latitude": parse_coordinates(row["Coordenadas"])[0],
            "longitude": parse_coordinates(row["Coordenadas"])[1]
        },
        "Google Maps": 'https://www.google.com/maps?q=' + row["Coordenadas"],
        "Nome da Praia": str(row["Nome da Praia"]),
        "Região": str(row["Região"]),
        "Concelho": str(row["Concelho"]),
        "Categoria": str(row["Categoria"]),
        "Qualidade da água": str(row["Qualidade da água"]),
        "Vigilancia": to_boolean(row["Vigilancia"]),
        "Posto de socorro": to_boolean(row["Posto de socorro"]),
        "Sanitarios": to_boolean(row["Sanitarios"]),
        "Duche": to_boolean(row["Duche"]),
        "Recolha lixo": to_boolean(row["Recolha lixo"]),
        "Limpeza praia": to_boolean(row["Limpeza praia"]),
        "Painel informativo": to_boolean(row["Painel informativo"]),
        "Apoio balnear": to_boolean(row["Apoio balnear"]),
        "Apoio à praia": to_boolean(row["Apoio à praia"]),
        "Estacionamento": to_boolean(row["Estacionamento"]),
        "Bandeira Azul": to_boolean(row["Bandeira Azul"]),
        "Acessível": to_boolean(row["Acessível"]),
        "Cadeira anfíbia": to_boolean(row["Cadeira anfíbia"]),
        "Ondas especiais": to_boolean(row["Ondas especiais"]),
        "Obras em curso": to_boolean(row["Obras em curso"]),
        "Risco de derrocada": to_boolean(row["Risco de derrocada"])
    }
    
    # Create amenities list for both languages
    amenities_en = []
    amenities_pt = []
    if metadata["Vigilancia"]:
        amenities_en.append("lifeguard supervision")
        amenities_pt.append("vigilância por nadadores-salvadores")
    if metadata["Posto de socorro"]:
        amenities_en.append("first aid post")
        amenities_pt.append("posto de socorro")
    if metadata["Sanitarios"]:
        amenities_en.append("restrooms")
        amenities_pt.append("sanitários")
    if metadata["Duche"]:
        amenities_en.append("showers")
        amenities_pt.append("duches")
    if metadata["Recolha lixo"]:
        amenities_en.append("waste collection")
        amenities_pt.append("recolha de lixo")
    if metadata["Limpeza praia"]:
        amenities_en.append("beach cleaning")
        amenities_pt.append("limpeza da praia")
    if metadata["Painel informativo"]:
        amenities_en.append("information board")
        amenities_pt.append("painel informativo")
    if metadata["Apoio balnear"]:
        amenities_en.append("bathing support")
        amenities_pt.append("apoio balnear")
    if metadata["Apoio à praia"]:
        amenities_en.append("beach support services")
        amenities_pt.append("apoio à praia")
    if metadata["Estacionamento"]:
        amenities_en.append("parking")
        amenities_pt.append("estacionamento")
    if metadata["Bandeira Azul"]:
        amenities_en.append("Blue Flag certification")
        amenities_pt.append("certificação Bandeira Azul")
    if metadata["Acessível"]:
        amenities_en.append("accessibility features")
        amenities_pt.append("acessibilidade")
    if metadata["Cadeira anfíbia"]:
        amenities_en.append("amphibious wheelchair")
        amenities_pt.append("cadeira anfíbia")
    
    # Create safety notes for both languages
    safety_en = []
    safety_pt = []
    if metadata["Obras em curso"]:
        safety_en.append("ongoing construction")
        safety_pt.append("obras em curso")
    if metadata["Risco de derrocada"]:
        safety_en.append("risk of rockfall")
        safety_pt.append("risco de derrocada")
    if metadata["Qualidade da água"] == "Água interdita a banhos":
        safety_en.append("bathing prohibited")
        safety_pt.append("banhos interditados")
    
    amenities_en_str = ", ".join(amenities_en) if amenities_en else "no notable amenities"
    amenities_pt_str = ", ".join(amenities_pt) if amenities_pt else "sem comodidades notáveis"
    safety_en_str = ", ".join(safety_en) if safety_en else "no specific safety concerns"
    safety_pt_str = ", ".join(safety_pt) if safety_pt else "sem preocupações de segurança específicas"
    
    # Create page_content in both languages
    page_content_en = (
        f"{metadata['Nome da Praia']} is a {metadata['Categoria'].lower()} located in {metadata['Concelho']}, "
        f"{metadata['Região']}, Portugal. For the 2025 bathing season ({metadata['Informação'].split('calendario : ')[1]}), "
        f"the water quality is rated as {metadata['Classificação_da_água']} with {metadata['Qualidade da água'].lower()}. "
        f"The beach offers {amenities_en_str}. Safety considerations include {safety_en_str}. "
        f"Located at coordinates {metadata['Coordenadas']['latitude']}, {metadata['Coordenadas']['longitude']}."
    )
    
    page_content_pt = (
        f"{metadata['Nome da Praia']} é uma {metadata['Categoria'].lower()} localizada no concelhos de {metadata['Concelho']}, região "
        f"{metadata['Região']} de Portugal. Para a época balnear de 2025 ({metadata['Informação'].split('calendario : ')[1]}), "
        f"a qualidade da água é classificada como {metadata['Classificação_da_água']} com {metadata['Qualidade da água'].lower()}. "
        f"A praia oferece {amenities_pt_str}. Considerações de segurança incluem {safety_pt_str}. "
        f"Localizada nas coordenadas {metadata['Coordenadas']['latitude']}, {metadata['Coordenadas']['longitude']}."
    )
    
    # Combine both languages in page_content
    page_content = f"{page_content_pt}"
    
    # Create Document
    doc = Document(page_content=page_content, metadata=metadata)
    documents.append(doc)

# Output the documents (for demonstration, print the first document)
#for doc in documents[:3]:  # Limit to first document for brevity
#    print("Page Content:")
#    print(doc.page_content)
#    print("\nMetadata:")
#    print(doc.metadata)
#    print("\n" + "="*50 + "\n")


# Embedding and Vector Store
# Initialize OpenAI embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Create FAISS vector store
vector_store = FAISS.from_documents(
    documents=documents,
    embedding=embedding_model
)

# Save the vector store to disk (optional)
vector_store.save_local("faiss_index")

# Example: Retrieve documents for a query
query = "Find beaches in Algarve with good water quality"
retrieved_docs = vector_store.similarity_search(query, k=2)

# Print retrieved documents
print("Retrieved Documents for Query:", query)
for i, doc in enumerate(retrieved_docs):
    print(f"\nDocument {i+1}:")
    print("Page Content:")
    print(doc.page_content)
    print("\nMetadata:")
    print(doc.metadata)
    print("\n" + "="*50 + "\n")