FROM python:3.9.18

WORKDIR /app/st_ndos
COPY home.py /app/st_ndos/
COPY .streamlit/ /app/st_ndos/.streamlit/
COPY libs/ /app/st_ndos/libs/ 
COPY files/ /app/st_ndos/files/
COPY requirements.txt /app/st_ndos/
RUN ls

RUN pip install -r requirements.txt
CMD streamlit run home.py
