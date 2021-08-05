# mercadolibre-export

Script que exporta los datos de autos usados de mercadolibre utilizando su API REST

Con el csv generado entrenamos un modelo en [Colab](https://colab.research.google.com/drive/1o1Be_zduGx3s2BiV3b4KAlTL6kRuwyxA)

### Como se ejecuta?
1. obtener el SERVER_GENERATED_AUTHORIZATION_CODE
https://auth.mercadolibre.com.ar/authorization?response_type=code&client_id=[client_id]&redirect_uri=https://google.com

2. pones el code en secrets.json

3. ya podes correr download.py