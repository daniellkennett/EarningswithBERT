import requests

def call_pull(ticker, year, quarter,key = 'e46f1a303dafb62460de104424a00084'):
    year = int(year)
    quarter = int(quarter)
    try:
        transcript = requests.get(f'https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?quarter={quarter}&year={year}&apikey={key}').json()
        tran = transcript[0]['content']
        date = transcript[0]['date']
        return tran
    except Exception as e:
        print(e)

def get_split(ticker, year, quarter):
  text1 = call_pull(ticker, year, quarter)
  l_total = []
  l_parcial = []
  if len(text1.split())//150 >0:
    n = len(text1.split())//150
  else: 
    n = 1
  for w in range(n):
    if w == 0:
      l_parcial = text1.split()[:200]
      l_total.append(" ".join(l_parcial))
    else:
      l_parcial = text1.split()[w*150:w*150 + 200]
      l_total.append(" ".join(l_parcial))
  return l_total

if __name__ == "__main__" :
    print(call_pull('ACIW', 2020, 1))
