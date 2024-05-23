import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

collum_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ']

SPREADSHEET_ID = "1i_JeHpE22mBIFqDfKQ-IqE8qBNxysKhBOde77HjC7oY"

def main():
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "data_secret.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()

    with open("valores_dolares.json", "r") as file:
        valores_dolares = json.load(file)
    with open("dump_nome_dolares.json", "r") as file:
        dolares = json.load(file)
    dados_adicionar = [[""]]
    dados_adicionar[0].extend(dolares)
    linha_adicionadas = 2

    for data in valores_dolares.keys():
        linha = [data]
        for valor_dolar_data in valores_dolares[data]:

            linha.append(list(valor_dolar_data.values())[0])
        dados_adicionar.append(linha)
        linha_adicionadas += 1

    qte_dolares = len(dolares)
    media = ["Média"]
    for i in range(qte_dolares):
        media.append(f"=MÉDIA({collum_names[i+1]}2:{collum_names[i+1]}{linha_adicionadas-1})")
    dados_adicionar.append(media)

    result = (
        sheet.values()
        .update(spreadsheetId=SPREADSHEET_ID, 
             range="Diario!A1", 
             valueInputOption="USER_ENTERED", 
             body={"values": dados_adicionar})
        .execute()
    )
    

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()